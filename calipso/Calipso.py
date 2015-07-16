##########################
#
#
#   @Author: Grant Mercer
#   @Author: Nathan Qian
##########################
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, HORIZONTAL, BOTH, VERTICAL, Message, TOP, LEFT, \
    SUNKEN, StringVar
import logging
from sys import platform as _platform
import tkFileDialog
import tkMessageBox
import webbrowser
import matplotlib.image as mpimg
import matplotlib
matplotlib.use('tkAgg')

from bokeh.colors import white
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from plot.plot_depolar_ratio import drawDepolar
from plot.plot_uniform_alt_lidar_dev import render_backscattered
from polygon.manager import ShapeManager
from attributesdialog import AttributesDialog
from constants import Plot
import constants
from importdialog import ImportDialog
from log import logger
from tools.linearalgebra import distance
from tools.navigationtoolbar import NavigationToolbar2CALIPSO
from tools.tools import Catcher
from toolswindow import ToolsWindow
from tkColorChooser import askcolor
from exctractdialog import ExtractDialog

class Calipso(object):
    """
    Main class of the application, handles all GUI related events as well as
    creating other GUI windows such as the toolbar or import dialog
    """

    def __init__(self, r):
        self.__root = r                         # Root of program
        self.__file = ''                        # Current file in use
        self.xrange = self.yrange = (0, 1000)   # X and Y range for scrolling plot
        self.panx = self.pany = 0               # Pan values for shifting map
        self.plot = Plot.baseplot               # Current selected plot
        self.__label_file_dialog = None
        self.new_file_flag = False

        # TODO: Add icon for window an task bar
        # Create three paned windows, two which split the screen vertically upon a single pane
        base_pane = PanedWindow()
        base_pane.pack(fill=BOTH, expand=1)
        sectioned_pane = PanedWindow(orient=VERTICAL)
        base_pane.add(sectioned_pane)
        top_paned_window = PanedWindow(sectioned_pane, orient=HORIZONTAL)
        sectioned_pane.add(top_paned_window)

        # Frame to hold dialog for browsing files
        self.__dialog_frame = Frame(top_paned_window)
        self.__dialog_frame.pack(side=LEFT)

        # Bottom half the screen
        bottom_paned_window = PanedWindow(sectioned_pane)
        sectioned_pane.add(bottom_paned_window)

        # The frame on which we will set out canvas for drawing etc.
        self.__drawplot_frame = Frame(bottom_paned_window,
                                      width=constants.WIDTH,
                                      height=constants.HEIGHT)

        # Matplotlib backend objects
        self.__parent_fig = Figure(figsize=(16, 11))
        self.__fig = self.__parent_fig.add_subplot(1, 1, 1)
        self.__parent_fig.set_tight_layout(True)
        self.__drawplot_canvas = FigureCanvasTkAgg(self.__parent_fig,
                                                   master=self.__drawplot_frame)
        # Create ToolsWindow class and pass itself + the root
        logger.info('Creating ToolsWindow')
        self.__child = ToolsWindow(self.__drawplot_canvas, self, r)
        logger.info('Creating ShapeManager')
        self.__shapemanager = ShapeManager(self.__fig, self.__drawplot_canvas,
                                           self)
        logger.info('Binding matplotlib backend to canvas and frame')
        self.__toolbar = NavigationToolbar2CALIPSO(self.__drawplot_canvas,
                                                   self.__child.coordinate_frame)

        # pack and display canvas
        self.__drawplot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.__drawplot_frame.pack()
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

    def setup_window(self):
        """
        Sets the title of root and invokes py:meth:`centerWindow`
        """
        self.__root.title("CALIPSO Visualization Tool (VOCAL)")
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        x = (sw - constants.WIDTH) / 2
        y = (sh - constants.HEIGHT) / 2
        self.__root.geometry('%dx%d+%d+%d' % (constants.WIDTH, constants.HEIGHT, x, y))
        # the child is designed to appear off to the right of the parent window, so the x location
        # is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        # plus a fourth the distance of the window
        if _platform == "linux" or _platform == "linux2":
            logger.info("Linux system detected")
            self.__child.geometry('%dx%d+%d+%d' % (
                constants.CHILDWIDTH + 50, constants.CHILDHEIGHT, x + constants.WIDTH,
                y + constants.HEIGHT / 4))
        else:
            self.__child.geometry('%dx%d+%d+%d' % (
                constants.CHILDWIDTH, constants.CHILDHEIGHT, x + constants.WIDTH + 50, y + constants.HEIGHT / 4))
        self.__root.wm_iconbitmap(r'ico/broadcasting.ico')
        self.__child.wm_iconbitmap(r'ico/broadcasting.ico')

    def setup_menu(self):
        """
        Creates a drop down menu bar
        """
        menu_bar = Menu(self.__root)

        # File Menu
        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label='Import file', command=self.import_file)
        menu_file.add_command(label='Save all shapes', command=lambda: self.save_as_json(save_all=True))
        menu_file.add_command(label='Save as shapes', command=self.save_as_json)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.close)
        menu_bar.add_cascade(label='File', menu=menu_file)

        # Polygon Menu
        menu_polygon = Menu(menu_bar, tearoff=0)
        menu_polygon.add_command(label='Import from Database',
                                 command=lambda: ImportDialog(self.__root, self))
        menu_polygon.add_command(label='Export to Database', command=self.notify_save_db)
        menu_bar.add_cascade(label='Polygon', menu=menu_polygon)

        # Help Menu
        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label='Documentation', command=lambda: webbrowser.open_new(
            constants.HELP_PAGE))
        menu_help.add_command(label='About', command=self.about)
        menu_bar.add_cascade(label='Help', menu=menu_help)

        # configure menu to screen
        self.__root.config(menu=menu_bar)

    def set_plot(self, plot_type, xrange_=(0, 1000), yrange=(0, 20)):
        """
        Draws to the canvas according to the *plot_type* specified in the arguments. Accepts one of
        the attributes below

        .. py:attribute:: BASE_PLOT
        .. py:attribute:: BACKSCATTERED
        .. py:attribute:: DEPOLARIZED
        .. py:attribute:: VFM

        :param :py:class:`int` plot_type: accepts ``BASE_PLOT, BACKSCATTERED, DEPOLARIZED, VFM``
        :param (:py:class:`int`,:py:class:`int`) xrange_: accepts a range of time to plot
        :param (:py:class:`int`,:py:class:`int`) yrange: accepts a range of altitude to plot
        """
        self.xrange = xrange_
        self.yrange = yrange
        if plot_type == Plot.baseplot:
            # Hide the axis and print an image
            self.__shapemanager.set_plot(Plot.baseplot)
            im = mpimg.imread('dat/CALIPSO.jpg')
            self.__fig.get_yaxis().set_visible(False)
            self.__fig.get_xaxis().set_visible(False)
            self.__fig.imshow(im)
        elif plot_type == Plot.backscattered:
            try:
                # Clear any references to the current figure, construct a new figure
                # and render the backscattered plot to it
                logger.info('Setting plot to backscattered xrange: ' +
                            str(xrange_) + ' yrange: ' + str(yrange))
                self.__shapemanager.clear_refs()
                self.__parent_fig.clear()
                self.__fig = self.__parent_fig.add_subplot(1, 1, 1)
                render_backscattered(self.__file, xrange_, yrange, self.__fig, self.__parent_fig)
                self.__shapemanager.set_current(Plot.backscattered, self.__fig)
                self.__drawplot_canvas.show()                            # show canvas
                self.__toolbar.update()                                  # update toolbar
                self.plot = Plot.backscattered
            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', 'No File Exists')
        # TODO: Reimplement with new plotting technique (like backscatter)
        elif plot_type == Plot.depolarized:
            try:
                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.error('Needs to be reimplemented')
                self.__shapemanager.clear_refs()
                self.__parent_fig.clear()
                self.__fig = self.__parent_fig.add_subplot(1, 1, 1)
                drawDepolar(self.__file, xrange_, yrange, self.__fig, self.__parent_fig)
                self.__shapemanager.set_current(Plot.depolarized, self.__fig)
                self.__drawplot_canvas.show()
                self.__toolbar.update()
                self.plot = Plot.depolarized
            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")
        elif plot_type == Plot.vfm:
            logger.error('Accessing unimplemented VFM plot')
            tkMessageBox.showerror("TODO", 'Sorry, this plot is currently not implemented')

    def reset(self):
        """
        Reset all objects on the screen, move pan to original
        """
        logger.info("Resetting plot")
        self.__shapemanager.reset()      # reset all buttons
        self.__toolbar.home()           # proc toolbar function to reset plot to home

    def pan(self, event):
        """
        Saves initial coordinates of mouse press when the user begins to pan

        :param event: Tkinter passed event object
        """
        logger.info("Pan point 1")
        self.panx = event.x
        self.pany = event.y

    def render_pan(self, event):
        """
        Saves ending coordinates of mouse press and proceeds to find the distance
        between the two points, scrolls the map accordingly

        :param event: Tkinter passed event object
        """
        logger.info("Pan point 2, finding distance and panning...")
        # Find distance and add an amplifier of 1.5
        dst = int(distance(self.panx, self.pany, event.x, event.y) * 1.5)
        # If the user is scrolling backwards
        if self.panx < event.x:
            # Already at beginning
            if self.xrange[0] == 0:
                logger.warning(
                    "Attempting to pan backwards, already at beginning nothing to be done")
                return
            # The end position would be negative
            if self.xrange[0] - dst < 0:
                logger.warning("Attempting to pan past beginning, setting to beginning")
                # Set both xrange and dst to zero and simply reload beginning range
                self.xrange = (0, self.xrange[1])
                dst = 0
            self.set_plot(self.plot, (self.xrange[0] - dst, self.xrange[1] - dst))
            logger.info("Panning backwards")
        else:
            logger.info("Panning forwards")
            self.set_plot(self.plot, (self.xrange[0] + dst, self.xrange[1] + dst))
        pass

    def create_top_gui(self):
        """
        Initializes and creates the *File: label*, *file dialog*, and *browse button* that appear
        at the top of the screen
        """
        logger.info("Creating top screen GUI")
        # Create label , entry box and browse button
        label_file = Label(self.__dialog_frame, text="File:")
        self.__label_file_dialog = Label(self.__dialog_frame, width=50, justify=LEFT,
                                         bg=white, relief=SUNKEN)
        browse_button = Button(self.__dialog_frame, text='Browse', width=10,
                               command=self.import_file)
        label_file.grid(row=1, column=0)
        self.__label_file_dialog.grid(row=1, column=1, padx=10)
        browse_button.grid(row=1, column=3)

    def notify_save_db(self):
        """
        Notify the database that a save is taking place, the
        db will then save all polygons present on the screen
        """
        logger.info('Notified database to save')
        success = self.__shapemanager.save_db()
        if success:
            logger.info('Success, saved to db')
            tkMessageBox.showinfo('database', 'All objects saved to database')
        else:
            logger.error('No objects to be saved')
            tkMessageBox.showerror('database', 'No objects to be saved')

    def save_json(self):
        """
        Save all shapes on the map inside a JSON object given a previously
        saved file. If no file exists prompt for file
        """
        logger.info('Notify JSON to save')
        # Save to last saved file, if no file exists prompt to a new file
        if self.__shapemanager.get_count() > 0:
            if self.__shapemanager.get_filename() == '':
                self.save_as_json()  # Still prompt for a file name if none currently exists
            else:
                self.__shapemanager.save_json()  # Else do a normal save with internal file
            tkMessageBox.showinfo('save', 'Shapes saved successfully')
        else:
            tkMessageBox.showerror('save as JSON', 'No objects to be saved')

    def save_as_json(self, save_all=False):
        """
        Save all shapes on the map given a file specified by the user
        """
        logger.info('Notify JSON to save as')
        # Save to a file entered by user, saveAll saves ALL objects across canvas
        # and cannot be called as a normal save(must always be save as)
        if self.__shapemanager.get_count() > 0:
            options = dict()
            options['defaultextension'] = '.json'
            options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
            f = tkFileDialog.asksaveasfilename(**options)
            if f is "":
                return
            if save_all:
                self.__shapemanager.save_all_json(f)
            else:
                self.__shapemanager.save_json(f)
        else:
            tkMessageBox.showerror('save as JSON', 'No objects to be saved')
            
    def transient_save(self):
        """
        Function to save the file before closing the application. If the user
        decides they wish to save before closing, transient_save is called to
        save to JSON then proceeds to exit the application.
        """
        self.save_json()
        self.__root.destroy()

    def import_file(self):
        """
        Load an HDF file for use with displaying backscatter and depolarized images
        """
        logger.info("Importing HDF file")
        # function to import HDF file used my open and browse
        file_types = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes=file_types)
        fl = dlg.show()
        if fl != '':
            if self.__file is not None and fl is not self.__file:
                self.__new_file_flag = True
            self.__file = fl
            segments = self.__file.rpartition('/')
            self.__label_file_dialog.config(width=50, bg=white, relief=SUNKEN, justify=LEFT,
                                            text=segments[2])
            self.__shapemanager.set_hdf(self.__file)

    def load(self):
        """
        load JSON objects from file by calling :py:meth:`polygonlist.readPlot(f)`
        """
        logger.info("Loading JSON")
        # loads JSON object by calling the polygonList internal readPlot method
        options = dict()
        options['defaultextension'] = '.json'
        options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
        f = tkFileDialog.askopenfilename(**options)
        if f is '':
            return
        self.__shapemanager.read_plot(f)

    def attribute_window(self, event):
        """
        Open attribute window for specifying attributes on objects

        :param event: A Tkinter passed event object
        """
        logger.info("Grabbing shape object")
        shape = self.__shapemanager.find_shape(event)
        logger.info("Opening attributes dialog")
        AttributesDialog(self.__root, shape)
        
    def paint_window(self, event):
        """
        Opens the paint window for specifying the shape's color
        
        :param event: A Tkinter passed event object
        """
        shape = self.__shapemanager.find_shape(event)
        logger.info("Painting shape")
        color = askcolor()
        if color[0] is not None:
            red = format(color[0][0], '02x')
            green = format(color[0][1], '02x')
            blue = format(color[0][2], '02x')
            color = '#' + red + green + blue
            shape.get_itemhandler().set_facecolor(color)
            self.__drawplot_canvas.show()
            
    def extract_window(self, event):
        """
        Opens a subwindow that displays the data bounded by the shape
        
        :param event: A Tkinter passed event object
        """
        shape = self.__shapemanager.find_shape(event)
        logger.info("Extracting data for %s" % shape.get_tag())
        ExtractDialog(self.__root, shape, self.__file, self.xrange, self.yrange)

    def get_root(self):
        """
        Return the root of the application

        :rtype: A Tkinter root
        """
        return self.__root

    def get_shapemanager(self):
        """
        Returns the internal :py:class:`polygonList` object

        :rtype: :py:class:`polygon.manager.ShapeManager`
        """
        return self.__shapemanager  # get functions for private variables

    def get_toolbar(self):
        """
        Returns the internal :py:class:`toolbar` object

        :rtype: :py:class:`tools.navigationtoolbar.NavigationToolbar2CALIPSO`
        """
        return self.__toolbar

    def get_fig(self):
        """
        Returns the figure that is plotted to the canvas

        :rtype: :py:class:`matplotlib.figure.Figure`
        """
        if self.__fig:
            return self.__fig
        logger.error("Fig does not exist")

    def get_file(self):
        """
        Return the current HDF file being displayed

        :type: :py:class:`str`
        """
        return self.__file

    def about(self):
        """
        Simple TopLevel window displaying the authors
        """
        logger.info('Opening about window')
        file_window = Toplevel(self.__root)
        file_window.title('About')
        message = Message(file_window, text='NASA DEVELOP\n \nLaRC Spring 2015 Term \nJordan Vaa '
                                            '(Team Lead) \nCourtney Duquette \nAshna Aggarwal \
                                            \n\nLaRC Summer 2015 Term \nGrant Mercer (Team Lead) '
                                            '\nNathan Qian')
        message.pack()

        button_close = Button(file_window, text='Close', command=file_window.destroy)
        button_close.pack()

    def setup_main_screen(self):
        """
        Setup the top GUI, initialize toolbar window and set the plot to a blank image
        """
        logger.info('Setting up GUI')
        self.create_top_gui()
        self.__child.setup_toolbar_buttons()
        logger.info('Setting initial plot')
        self.set_plot(Plot.baseplot)

    def close(self):
        """
        Checks if the all the shapes are saved. If a shape is unsaved, the
        program will ask the user whether save or not, and then close the 
        program
        """
        if not self.__shapemanager.is_all_saved():
            logger.warning("Unsaved shapes found")
            answer = tkMessageBox.\
                askyesnocancel('Close Without Saving',
                               'There are unsaved shapes on the plot. Save these shapes?')
            if answer is True:
                logger.info("Saving shapes")
                self.transient_save()
            elif answer is False:
                logger.info("Dumping unsaved shapes")
                self.__root.destroy()
            elif answer is None:
                pass
        else:
            self.__root.destroy()
            
    def new_file_save(self):
        """
        Checks if all the shapes are saved before loading the new file. If a
        shape is unsaved, the program will ask the user to save or not before
        continuing
        """
        save_window = Toplevel(self.__root)
        save_window.transient(self.__root)
        save_window.title('Close Without Saving')
        

def main():
    # Create Tkinter root and initialize Calipso
    logging.info('Starting CALIPSO program')
    Tk.CallWrapper = Catcher
    rt = Tk()
    logging.info('Instantiate CALIPSO program')
    program = Calipso(rt)

    # Setup Calipso window
    logger.info('Setting up window')
    program.setup_window()
    logger.info('Setting up menu')
    program.setup_menu()
    logger.info('Setting up main screen')
    program.setup_main_screen()

    # Begin program
    rt.mainloop()
    logging.info('Terminated CALIPSO program')

if __name__ == "__main__":
    main()
