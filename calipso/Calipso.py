##########################
#
#
#   @Author: Grant Mercer
#   @Author: Nathan Qian
##########################
from tools.vocalDataBlock import VocalDataBlock, MetaData

import matplotlib

matplotlib.use('tkAgg')
from Tkconstants import RIGHT, END, DISABLED
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, HORIZONTAL, BOTH, VERTICAL, TOP, LEFT, \
    SUNKEN, StringVar, Text, IntVar, BooleanVar
import ttk
import logging
from sys import platform as _platform
from tkColorChooser import askcolor
import tkFileDialog
import tkMessageBox
import webbrowser
import ccplot.utils

from attributesdialog import AttributesDialog
from bokeh.colors import white
from constants import Plot, PATH, ICO
import constants
from exctractdialog import ExtractDialog
from importdialog import ImportDialog
from log.log import logger, error_check
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
from plot.plot_depolar_ratio import render_depolarized
from plot.plot_backscattered import render_backscattered
from plot.plot_vfm import render_vfm
from plot.plot_iwp import render_iwp
from polygon.manager import ShapeManager
from tools.linearalgebra import distance
from tools.navigationtoolbar import NavigationToolbar2CALIPSO
from tools.optionmenu import ShapeOptionMenu
from tools.tools import Catcher, center
from toolswindow import ToolsWindow
from db import db
from PIL import ImageTk
from tools.tooltip import create_tool_tip
import matplotlib.image as mpimg


class Calipso(object):
    """
    Main class of the application, handles all GUI related events as well as
    creating other GUI windows such as the toolbar or import dialog
    """

    ############################################################
    #   Initialization functions

    def __init__(self, r):
        self.load_img = ImageTk.PhotoImage(file=PATH + '/ico/load.png')
        self.save_img = ImageTk.PhotoImage(file=PATH + '/ico/save.png')
        self.dot_shp_img = ImageTk.PhotoImage(file=PATH + '/ico/save.png')
        #self.dot_shp_img = ImageTk.PhotoImage(file=PATH + '/ico/dot_shp.png')
        self.__root = r  # Root of program
        self.__file = ''  # Current file in use
        self.xrange = self.yrange = (0, 100)  # X and Y range for scrolling plot
        self.panx = self.pany = 0  # Pan values for shifting map
        self.plot = Plot.baseplot  # Current selected plot
        #self.plot2 = Plot.baseplot  # Current selected plot
        self.__label_file_dialog = None
        self.new_file_flag = False
        self.option_menu = None
        self.shape_var = StringVar()
        self.__data_block = VocalDataBlock('Empty')
        self.__my_meta_data = MetaData()
        self.__p_figs = [None]*10
        self.__figs = [None]*10
        self.__shapemanagers = [None]*10
        self.__drawplot_canvases = [None]*10
        self.__tab_buttons = [BooleanVar()]*10
        #for i in [0,10]:
            #self.__tab_buttons.append(BooleanVar())
        self.__plots = [None]*10
        self.data_block_iterator = [-99]*10

        self.width = self.__root.winfo_screenwidth()
        self.height = self.__root.winfo_screenheight()

        logger.info('Screen resolution: ' + str(self.width) + 'x' + str(self.height))

        # TODO: Add icon for window and task bar
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
        self.__dialog_shape_frame = Frame(top_paned_window)
        self.__dialog_shape_frame.pack(side=RIGHT)

        # Bottom half the screen
        bottom_paned_window = PanedWindow(sectioned_pane)
        sectioned_pane.add(bottom_paned_window)

        # Create the ttk notebook object to hold the tabs.
        self.__drawplot_notebook = ttk.Notebook(bottom_paned_window,
                                                width=constants.WIDTH,
                                                height=constants.HEIGHT)

        # Matplotlib backend objects
        for i in range(0, 10):
            self.__p_figs[i] = Figure(figsize=(11, 16))
            self.__figs[i] = self.__p_figs[i].add_subplot(1, 1, 1)
            self.__p_figs[i].set_tight_layout(True)
            self.__plots[i] = Plot.baseplot

        # The frames on which we will set out canvases for drawing
        self.create_tab_frames()

        #self.__drawplot_canvases[0] = FigureCanvasTkAgg(self.__p_figs[0], master=self.__baseplot_frame)
        self.__drawplot_canvases[1] = FigureCanvasTkAgg(self.__p_figs[1], master=self.__backscattered532_frame)
        self.__drawplot_canvases[2] = FigureCanvasTkAgg(self.__p_figs[2], master=self.__depolarized_frame)
        self.__drawplot_canvases[3] = FigureCanvasTkAgg(self.__p_figs[3], master=self.__vfm_frame)
        self.__drawplot_canvases[4] = FigureCanvasTkAgg(self.__p_figs[4], master=self.__ice_water_frame)
        self.__drawplot_canvases[5] = FigureCanvasTkAgg(self.__p_figs[5], master=self.__blend_frame)
        self.__drawplot_canvases[6] = FigureCanvasTkAgg(self.__p_figs[6], master=self.__parallel_frame)
        self.__drawplot_canvases[7] = FigureCanvasTkAgg(self.__p_figs[7], master=self.__backscattered1064_frame)
        self.__drawplot_canvases[8] = FigureCanvasTkAgg(self.__p_figs[8], master=self.__color_ratio_frame)
        self.__drawplot_canvases[9] = FigureCanvasTkAgg(self.__p_figs[9], master=self.__aerosol_subtype_frame)

        self.__parent_fig = Figure(figsize=(16, 11))
        self.__fig = self.__parent_fig.add_subplot(1, 1, 1)
        self.__parent_fig.set_tight_layout(True)
        self.__drawplot_canvas = FigureCanvasTkAgg(self.__parent_fig,
                                                   master=self.__drawplot_notebook)

        # Create ToolsWindow class and pass itself + the root
        logger.info('Creating ToolsWindow')
        self.__child = ToolsWindow(self.__drawplot_canvas, self, r)
        logger.info('Creating ShapeManager')
        self.__shapemanager = ShapeManager(self.__fig, self.__drawplot_canvas,
                                           self)
        for i in range(1, 10):
            self.__shapemanagers[i] = ShapeManager(self.__figs[i], self.__drawplot_canvases[i], self)

        logger.info('Binding matplotlib backend to canvas and frame')
        self.__toolbar = NavigationToolbar2CALIPSO(self,
                                                   self.__drawplot_canvas,
                                                   self.__child.coordinate_frame)

        # pack and display canvas
        for i in range(1, 10):
            self.__drawplot_canvases[i].get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.__drawplot_notebook.pack()
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

    def setup_menu(self):
        """
        Creates a drop down menu bar at the top of the tool
        """
        menu_bar = Menu(self.__root)

        # File Menu
        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label='Import file', command=self.import_file)
        menu_file.add_command(label='Save all shapes', command=lambda: self.save_as_json(save_all=True))
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.close)
        menu_bar.add_cascade(label='File', menu=menu_file)

        # Edit Menu
        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label='Select all shapes', command=self.__shapemanager.select_all)
        menu_edit.add_command(label='Deselect all shapes', command=self.__shapemanager.deselect_all)
        menu_bar.add_cascade(label='Edit', menu=menu_edit)

        # Polygon Menu
        menu_polygon = Menu(menu_bar, tearoff=0)
        menu_polygon.add_command(label='Import from Database', command=self.import_dialog)
        menu_polygon.add_command(label='Export all to Database', command=self.export_db)
        menu_polygon.add_command(label='Export selected to Database', command=lambda: self.export_db(only_selected=True))
        menu_polygon.add_separator()
        menu_polygon.add_command(label='Import archive to database',
                                 command=Calipso.import_json_db)
        menu_polygon.add_command(label='Export database to archive',
                                 command=Calipso.export_json_db)
        menu_bar.add_cascade(label='Polygon', menu=menu_polygon)

        # Tabs Menu

        menu_tabs = Menu(menu_bar,tearoff=0)
        self.__tab_buttons[0].set(True)
        menu_tabs.add_checkbutton(label='Meta Data', variable=self.__tab_buttons[0],
                                  command=lambda: self.toggle_tabs_menu_item(0, self.__baseplot_frame))
        self.__tab_buttons[1].set(True)
        menu_tabs.add_checkbutton(label='Backscatter 532', variable=self.__tab_buttons[1],
                                  command=lambda: self.toggle_tabs_menu_item(1, self.__backscattered532_frame))
        self.__tab_buttons[2].set(True)
        menu_tabs.add_checkbutton(label='Depolarization', variable=self.__tab_buttons[2],
                                  command=lambda: self.toggle_tabs_menu_item(2, self.__vfm_frame))
        self.__tab_buttons[3].set(True)
        menu_tabs.add_checkbutton(label='Vertical Feature Mask', variable=self.__tab_buttons[3],
                                  command=lambda: self.toggle_tabs_menu_item(3, self.__vfm_frame))
        self.__tab_buttons[4].set(True)
        menu_tabs.add_checkbutton(label='Ice Water Phase', variable=self.__tab_buttons[4],
                                  command=lambda: self.toggle_tabs_menu_item(4, self.__ice_water_frame))
        self.__tab_buttons[5].set(False)
        menu_tabs.add_checkbutton(label='Blend', variable= self.__tab_buttons[5],
                                  command=lambda: self.toggle_tabs_menu_item(5, self.__blend_frame))
        self.__tab_buttons[6].set(False)
        menu_tabs.add_checkbutton(label='Parallel', variable= self.__tab_buttons[6],
                                  command=lambda: self.toggle_tabs_menu_item(6, self.__parallel_frame))
        self.__tab_buttons[7].set(False)
        menu_tabs.add_checkbutton(label='Backscatter 1064', variable= self.__tab_buttons[7],
                                  command=lambda: self.toggle_tabs_menu_item(7, self.__backscattered1064_frame))
        self.__tab_buttons[8].set(False)
        menu_tabs.add_checkbutton(label='Color Ratio', variable=self.__tab_buttons[8],
                                  command=lambda: self.toggle_tabs_menu_item(8, self.__color_ratio_frame))
        self.__tab_buttons[9].set(False)
        menu_tabs.add_checkbutton(label='Aerosol Subtypes', variable=self.__tab_buttons[9],
                                  command=lambda: self.toggle_tabs_menu_item(9, self.__aerosol_subtype_frame))

        menu_bar.add_cascade(label='Tabs', menu=menu_tabs)

        # Help Menu
        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label='Documentation', command=lambda: webbrowser.open_new(
                constants.HELP_PAGE))
        menu_help.add_command(label='About', command=self.about)
        menu_bar.add_cascade(label='Help', menu=menu_help)

        # configure menu to screen
        self.__root.config(menu=menu_bar)

    def setup_window(self):
        """
        Sets the title of root and places window on screen
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
        elif _platform == 'darwin':
            logger.info('OSX system detected')
            self.__child.geometry('%dx%d+%d+%d' % (
                constants.CHILDWIDTH + 75, constants.CHILDHEIGHT + 50, x + constants.WIDTH,
                y + constants.HEIGHT / 4))
        else:
            # if the main window and the tools window's width are greater than the screen width
            if constants.WIDTH + constants.CHILDHEIGHT > sw:
                # place the tools window 10/11 from the left of the screen
                self.__child.geometry('%dx%d+%d+%d' % (
                    constants.CHILDWIDTH, constants.CHILDHEIGHT, 10 * sw / 11 - constants.CHILDWIDTH / 2,
                    y + constants.HEIGHT / 4))
            else:
                # place the tools window 50 units from the the right end of the main window
                self.__child.geometry('%dx%d+%d+%d' % (
                    constants.CHILDWIDTH, constants.CHILDHEIGHT, x + constants.WIDTH + 50, y + constants.HEIGHT / 4))
            logger.info("Placed toolswindow at: " + str(self.__child.geometry()))
        self.__root.wm_iconbitmap(ICO)
        self.__child.wm_iconbitmap(ICO)

    def setup_main_screen(self):
        """
        Setup the top GUI, initialize toolbar window and set the plot to a blank image
        """
        logger.info('Creating upper program GUI')
        # Create label , entry box and browse button
        label_file = Label(self.__dialog_frame, text="File:")
        self.__label_file_dialog = Label(self.__dialog_frame, width=50, justify=LEFT,
                                         bg=white, relief=SUNKEN)
        browse_button = Button(self.__dialog_frame, text='Browse', width=10,
                               command=self.import_file)
        label_file.grid(row=1, column=0)
        self.__label_file_dialog.grid(row=1, column=1, padx=10)
        browse_button.grid(row=1, column=3)

        # Load shapes from JSON
        load_button = \
            Button(self.__dialog_shape_frame, image=self.load_img, width=30, height=30, command=self.load)
        load_button.pack(side=RIGHT, padx=2)
        create_tool_tip(load_button, 'Load JSON')

        # Save shapes as JSON
        save_button = \
            Button(self.__dialog_shape_frame, image=self.save_img, width=30, height=30, command=self.save_as_json)
        save_button.pack(side=RIGHT, padx=2)
        create_tool_tip(save_button, 'Save selected\n objects to\n JSON')

        # Save shapes as JSON
        dot_shp_button = \
            Button(self.__dialog_shape_frame, image=self.dot_shp_img, width=30, height=30)
        dot_shp_button.pack(side=RIGHT, padx=2)
        create_tool_tip(dot_shp_button, 'Export to\n shapefile')

        self.option_menu = ShapeOptionMenu(self.__dialog_shape_frame, self.shape_var, "",
                                           command=self.select_shape)
        self.option_menu.bind("<ButtonPress-1>", self.update_shape_optionmenu)
        self.option_menu.pack(side=RIGHT, padx=10)
        label_shapes = Label(self.__dialog_shape_frame, text="Select")
        label_shapes.pack(side=RIGHT)
        self.__child.setup_toolbar_buttons()
        logger.info('Setting initial plot')
        self.set_plot(Plot.baseplot, 0)

    #   end Initialization functions
    ############################################################

    ############################################################
    #   Exclusive menu bar & top gui functions

    def update_shape_optionmenu(self, event):
        """
        Callback function bound to *<ButtonPress-1>* which displays the current list
        of shapes on the plot to the option menu. All tags are grabbed which can then
        be selected by the user to see which object they are looking for.

        :param event: Tkinter passed event object, **ignored**
        """
        ops = [x.get_tag() for x in self.__shapemanager.get_current_list() if x is not None]
        self.option_menu.set_menu(ops)

    def select_shape(self, tag):
        self.__shapemanager.select_from_tag(tag)

    def import_file(self):
        """
        Load an HDF file for use with displaying backscatter and depolarized images
        """
        logger.info('Importing HDF file')
        # function to import HDF file used my open and browse
        file_types = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes=file_types)
        fl = dlg.show()
        if fl != '':
            if self.__file is not None and fl is not self.__file:
                self.new_file_flag = True
            self.__file = fl
            self.__data_block = VocalDataBlock(fl)
            segments = self.__file.rpartition('/')
            self.__label_file_dialog.config(width=50, bg=white, relief=SUNKEN, justify=LEFT,
                                            text=segments[2])

    def export_db(self, only_selected=False):
        """
        Notify the database that a save is taking place, the
        db will then save all polygons present on the screen
        """
        logger.info('Notifying database to save with select flag %s' % (str(only_selected)))
        success = self.__shapemanager.save_db(only_selected)
        if success:
            logger.info('Success, saved to db')
            tkMessageBox.showinfo('database', 'Objects saved to database')
        else:
            logger.error('No objects to be saved')
            tkMessageBox.showerror('database', 'No objects to be saved')

    @staticmethod
    def import_json_db():
        """
        Import the contents of a JSON file to the database, works hand in hand
        with the ``export_json_db`` class method. This will allows users to share
        their database without needing to manually move their db file.
        :return:
        """
        options = dict()
        options['defaultextension'] = '.zip'
        options['filetypes'] = [('CALIPSO Data Archive', '*.zip'), ('All files', '*')]
        fl = tkFileDialog.askopenfilename(**options)
        if fl != '':
            log_fname = fl.rpartition('/')[2]
            logger.info('Importing database from \'%s\'' % log_fname)
            success = db.import_from_json(fl)
            if success:
                logger.info('Success, JSON file imported')
                tkMessageBox.showinfo('database', 'shapes from %s imported ' % log_fname +
                                      '(note: new tags have been assigned to these shapes!)')
            else:
                logger.error('Invalid JSON file')
                tkMessageBox.showerror('database', 'Invalid JSON file %s' % log_fname)

    @staticmethod
    def export_json_db():
        """
        Export the contents of the database to an archive containing JSON, which can then be
        loaded into other databases and have all shapes imported
        """
        if tkMessageBox.askyesno('Export database',
                                 'Database will be exported to a specified' +
                                         ' archive (this operation is a copy, not a move)' +
                                         ' continue?'):
            options = dict()
            options['defaultextension'] = '.zip'
            options['filetypes'] = [('ZIP Files', '*.zip'), ('All files', '*')]
            fl = tkFileDialog.asksaveasfilename(**options)
            if fl != '':
                log_fname = fl.rpartition('/')[2]
                logger.info('Dumping database to \'%s\'' % log_fname)
                success = db.dump_to_json(fl)
                if success:
                    logger.info('Success, JSON file created')
                    tkMessageBox.showinfo('database', 'Database exported to \'%s\'' % log_fname)
                else:
                    logger.error('No objects to be saved')
                    tkMessageBox.showerror('database', 'No objects inside database to export to JSON')
        else:
            logger.info('Export to database canceled')

    # End menu bar functions
    ############################################################

    def plot_baseplot(self, in_i):
        self.__metadata_text = "Metadata\nMetadata\nMetadata\nMetadata\nMetadata\nMetadata\nMetadata\nMetadata"
        self.__metadata_label = Label(self.__baseplot_frame, text=self.__metadata_text,
                                      width=constants.WIDTH, height=constants.HEIGHT,
                                      bg='LightYellow')
        self.__metadata_label.pack()

    def plot_not_available(self, in_i, in_type):
        self.__shapemanagers[in_i].set_plot(Plot.not_available)
        im = mpimg.imread(PATH + '/dat/grey.jpg')
        self.__figs[in_i].get_yaxis().set_visible(False)
        self.__figs[in_i].set_title("Plot currently not available")
        self.__figs[in_i].get_xaxis().set_visible(False)
        self.__figs[in_i].imshow(im)

    def set_plot(self, plot_type, in_i):
        """
        Draws to the canvas according to the *plot_type* specified in the arguments. Accepts one of
        the attributes below

        .. py:attribute:: BASE_PLOT
        .. py:attribute:: BACKSCATTE RED
        .. py:attribute:: DEPOLARIZED
        .. py:attribute:: VFM

        :param int plot_type: accepts ``BASE_PLOT, BACKSCATTERED, DEPOLARIZED, VFM``
        :param list xrange\_: accepts a range of time to plot
        :param list yrange: accepts a range of altitude to plot
        """
        #xrange_ = self.__my_meta_data.get_meta_x(2)
        #yrange = self.__my_meta_data.get_meta_y(2)

        self.__data_block.set_working_meta(self.__my_meta_data)

        if plot_type == Plot.baseplot:
            # Hide the axis and print an image
            self.plot_baseplot(in_i)

        elif plot_type == Plot.backscattered:
            try:
                logger.info('Setting plot to Backscattered 532 (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))
                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    if data_block_iterator == -99:
                        self.plot_not_available(in_i, plot_type)
                    else:
                        self.load_figure_attributes(data_block_iterator, in_i)
                else:
                    logger.info('Using Original functions')
                    self.__figs[in_i] = render_backscattered(self.__data_block.get_file_name(1),
                                                             [
                                                                self.__data_block.get_percent_to_iterator(
                                                                    self.__my_meta_data.get_meta_x(0),
                                                                    self.__my_meta_data.get_meta_type()),
                                                                self.__data_block.get_percent_to_iterator(
                                                                    self.__my_meta_data.get_meta_x(1),
                                                                    self.__my_meta_data.get_meta_type())
                                                             ],
                                                             self.__my_meta_data.get_meta_y(2),
                                                             self.__figs[in_i],
                                                             self.__p_figs[in_i])

                self.__shapemanagers[in_i].set_current(Plot.backscattered, self.__figs[in_i])
                self.__drawplot_canvases[in_i].show()
                self.__toolbar.update()
                self.__plots[in_i] = Plot.backscattered
            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', 'No File Exists')
            except IndexError:
                tkMessageBox.showerror('Backscattered Plot', 'Index out of bounds')

        elif plot_type == Plot.depolarized:
            try:

                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.info('Setting plot to Depolarization (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))

                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    if data_block_iterator == -99:
                        self.plot_not_available(in_i, plot_type)
                    else:
                        self.load_figure_attributes(data_block_iterator, in_i)
                else:
                    render_depolarized(self.__data_block.get_file_name(1),
                                       [
                                           self.__data_block.get_percent_to_iterator(
                                               self.__my_meta_data.get_meta_x(0),
                                               self.__my_meta_data.get_meta_type()),
                                           self.__data_block.get_percent_to_iterator(
                                               self.__my_meta_data.get_meta_x(1),
                                               self.__my_meta_data.get_meta_type())
                                       ],
                                       self.__my_meta_data.get_meta_y(2), self.__figs[in_i],
                                                             self.__p_figs[in_i])
                    logger.info('Using Original functions')

                self.__shapemanagers[in_i].set_current(Plot.depolarized, self.__figs[in_i])
                self.__drawplot_canvases[in_i].show()
                self.__toolbar.update()
                self.__plots[in_i] = Plot.depolarized
            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")

        elif plot_type == Plot.vfm:
            try:

                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.info('Setting plot to vfm (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))

                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    if data_block_iterator == -99:
                        self.plot_not_available(in_i, plot_type)
                    else:
                        self.load_figure_attributes(data_block_iterator,in_i)
                else:
                    logger.info('Using Original functions')
                    render_vfm(self.__data_block.get_file_name(2),
                               [
                                    self.__data_block.get_percent_to_iterator(
                                        self.__my_meta_data.get_meta_x(0),
                                        self.__my_meta_data.get_meta_type()),
                                    self.__data_block.get_percent_to_iterator(
                                        self.__my_meta_data.get_meta_x(1),
                                        self.__my_meta_data.get_meta_type())
                                ],
                                self.__my_meta_data.get_meta_y(2), self.__figs[in_i],
                                self.__p_figs[in_i])

                    self.__shapemanagers[in_i].set_current(Plot.vfm, self.__figs[in_i])
                    self.__drawplot_canvases[in_i].show()
                    self.__toolbar.update()
                    self.__plots[in_i] = Plot.vfm

            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")

        elif plot_type == Plot.iwp:
            try:
                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.info('Setting plot to iwp (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))

                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    if data_block_iterator == -99:
                        self.plot_not_available(in_i, plot_type)
                    else:
                        self.load_figure_attributes(data_block_iterator, in_i)
                else:
                    render_iwp(self.__data_block.get_file_name(2),
                        [
                            self.__data_block.get_percent_to_iterator(
                                self.__my_meta_data.get_meta_x(0),
                                self.__my_meta_data.get_meta_type()),
                            self.__data_block.get_percent_to_iterator(
                                self.__my_meta_data.get_meta_x(1),
                                self.__my_meta_data.get_meta_type())
                        ],
                                self.__my_meta_data.get_meta_y(2), self.__figs[in_i],
                                self.__p_figs[in_i])
                    logger.info('Using Original functions')

                    self.__shapemanagers[in_i].set_current(Plot.iwp, self.__fig)
                    self.__drawplot_canvases[in_i].show()
                    self.__toolbar.update()
                    self.__plots[in_i] = Plot.iwp
            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")

        elif plot_type == Plot.blend:
            try:

                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.info('Setting plot to Blend (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))

                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    logger.warning('Blend not implemented in original version of vocal')
                    self.plot_not_available(in_i, plot_type)

                    '''
                    self.__data_block.set_working_meta(self.__my_meta_data)
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    self.load_figure_attributes(data_block_iterator, in_i)
                    '''
                else:
                    logger.info('Using Original functions')
                    logger.warning('Blend not implemented in original version of vocal')
                    self.plot_not_available(in_i, plot_type)

            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")

        elif plot_type == Plot.parallel:
            try:

                # Clear any references to the current figure, construct a new figure
                # and render the depolarized plot to it
                logger.info('Setting plot to Parallel (' + str(self.__my_meta_data.get_meta_type()) + ') ' +
                            'x range: ' + str(self.__my_meta_data.get_meta_x(2)) +
                            ' y range: ' + str(self.__my_meta_data.get_meta_y(2)))

                if constants.debug_switch != 99:
                    logger.info('Using VocalDataBlock')
                    self.plot_not_available(in_i, plot_type)
                    logger.warning('Parallel not implemented...yet')
                    '''
                    self.__data_block.set_working_meta(self.__my_meta_data)
                    data_block_iterator = self.__data_block.get_figure(self.__my_meta_data)
                    self.load_figure_attributes(data_block_iterator, in_i)
                    '''
                else:
                    logger.info('Using Original functions')
                    self.plot_not_available(in_i, plot_type)
                    logger.warning('Parallel not implemented...yet')

                self.__shapemanagers[in_i].set_current(Plot.parallel, self.__fig[in_i])
                self.__drawplot_canvases[in_i].show()
                self.__toolbar.update()
                self.__plots[in_i] = Plot.parallel

            except IOError:
                logger.error('IOError, no file exists')
                tkMessageBox.showerror('File Not Found', "No File Exists")
        else:
            logger.warning('Plot Type not yet supported')
            self.plot_not_available(in_i, plot_type)

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
        logger.info('Pan point 2, finding distance and panning...')
        # Find distance and add an amplifier of 1.5
        dst = int(distance(self.panx, self.pany, event.x, event.y) * 1.5)
        # If the user is scrolling backwards
        if self.panx < event.x:
            # Already at beginning
            if self.xrange[0] == 0:
                logger.warning(
                        'Attempting to pan backwards, already at beginning nothing to be done')
                return
            # The end position would be negative
            if self.xrange[0] - dst < 0:
                logger.warning('Attempting to pan past beginning, setting to beginning')
                # Set both xrange and dst to zero and simply reload beginning range
                self.xrange = (0, self.xrange[1])
                dst = 0
            self.set_plot(self.plot, (self.xrange[0] - dst, self.xrange[1] - dst))
            logger.info('Panning backwards')
        else:
            logger.info('Panning forwards')
            self.set_plot(self.plot, xrange_=(self.xrange[0] + dst, self.xrange[1] + dst),
                          yrange=(int(self.__child.begin_alt_range_entry.get()),
                                  int(self.__child.end_alt_range_entry.get())))
        self.__child.begin_range_entry.delete(0, END)
        self.__child.end_range_entry.delete(0, END)
        self.__child.begin_range_entry.insert(END, str(self.xrange[0]))
        self.__child.end_range_entry.insert(END, str(self.xrange[1]))

    def save_json(self):
        """
        **DEPRECATED**

        Save all shapes on the map inside a JSON object given a previously
        saved file. If no file exists prompt for file
        """
        logger.info('Notifying JSON to save')
        # Save to last saved file, if no file exists prompt to a new file
        if self.__shapemanager.get_count() > 0:
            saved = True
            if self.__shapemanager.get_filename() == '':
                saved = self.save_as_json()  # Still prompt for a file name if none currently exists
            else:
                self.__shapemanager.save_json()  # Else do a normal save with internal file
            if saved:
                tkMessageBox.showinfo('save', 'Shapes saved successfully')
            else:
                return False
        else:
            tkMessageBox.showerror('save as JSON', 'No objects to be saved')

    def save_as_json(self, save_all=False):
        """
        Save all selected objects on the plot, asking for a filename first

        if ``save_all`` is specified and set to ``True``, the function will save **all**
        shapes across **all** plots in the program.
        """
        logger.info('Notifying JSON to save as')
        # Save to a file entered by user, saveAll saves ALL objects across canvas
        # and cannot be called as a normal save(must always be save as)
        if self.__shapemanager.get_selected_count() > 0:
            options = dict()
            options['defaultextension'] = '.json'
            options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
            f = tkFileDialog.asksaveasfilename(**options)
            if f == '':
                logger.info("cancelling save as json")
                return False
            if save_all:
                self.__shapemanager.save_all_json(f)
            else:
                self.__shapemanager.save_json(f)
        else:
            logger.error('No selected objects found, canceling save')
            tkMessageBox.showerror('save as JSON', 'No objects to be saved')

    def load(self):
        """
        load JSON objects from file by calling :py:meth:`polygonlist.readPlot(f)`
        """
        logger.info('Loading JSON')
        # loads JSON object by calling the polygonList internal readPlot method
        options = dict()
        options['defaultextension'] = '.json'
        options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
        f = tkFileDialog.askopenfilename(**options)
        if f is '':
            return
        self.__shapemanager.read_plot(f)

    def about(self):
        """
        Simple TopLevel window displaying the authors
        """
        logger.info('Opening about window')
        file_window = Toplevel(self.__root)
        file_window.geometry("300x300")
        file_window.title('About')

        text = Text(file_window)
        text.insert(END, constants.ABOUT)
        text.config(state=DISABLED)
        text.pack(expand=True, fill=BOTH)

        button_close = Button(file_window, text='Close', command=file_window.destroy)
        button_close.pack()

        center(file_window, (300, 300))

    def paint(self, event):
        """
        Opens the paint window for specifying the shape's color

        :param event: A Tkinter passed event object
        """
        shape = self.__shapemanager.find_shape(event)
        color = askcolor()
        if color[0] is not None:
            red = format(color[0][0], '02x')
            green = format(color[0][1], '02x')
            blue = format(color[0][2], '02x')
            color = '#' + red + green + blue
            logger.info('Painting %s -> %s' % (shape.get_tag(), color))
            shape.get_itemhandler().set_facecolor(color)
            self.__drawplot_canvas.show()

    def reset(self):
        """
        Reset all objects on the screen, move pan to original
        """
        logger.info("Resetting plot")
        self.__shapemanager.reset()  # reset all shapes
        self.__toolbar.home()  # proc toolbar function to reset plot to home

    ############################################################
    #   The following functions open dialogs which are defined
    #   in separate files. Dialog should always be treated as
    #   singletons

    def attribute_dialog(self, event):
        """
        Open attribute window for specifying attributes on objects

        :param event: A Tkinter passed event object
        """
        logger.info('Grabbing shape object')
        shape = self.__shapemanager.find_shape(event)
        logger.info('Opening attributes dialog')
        AttributesDialog(self.__root, shape). \
            wm_iconbitmap(ICO)

    def extract_dialog(self, event):
        """
        Opens a subwindow that displays the data bounded by the shape

        :param event: A Tkinter passed event object
        """
        shape = self.__shapemanager.find_shape(event)
        logger.info("Extracting data for %s" % shape.get_tag())
        ExtractDialog(self.__root, shape, self.__file, self.xrange, self.yrange). \
            wm_iconbitmap(ICO)

    def import_dialog(self):
        """
        Open the database import window allowing the user to import and
        delete entries.
        """
        logger.info('Opening database import window')
        if (not ImportDialog.singleton):
            ImportDialog(self.__root, self). \
                wm_iconbitmap(ICO)
        else:
            logger.warning('Found existing import window, canceling')

    # end dialog functions
    ############################################################

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

        :rtype: :py:class:`SubplotAxes`
        """
        if self.__fig:
            return self.__fig
        logger.error('Fig does not exist')

    def get_file(self):
        """
        Return the current HDF file being displayed

        :type: :py:class:`str`
        """
        return self.__file

    def close(self):
        """
        Checks if the all the shapes are saved. If a shape is unsaved, the
        program will ask the user whether save or not, and then close the
        program
        """
        if not self.__shapemanager.is_all_saved():
            logger.warning('Unsaved shapes found')
            answer = tkMessageBox. \
                askyesnocancel('Close Without Saving',
                               'There are unsaved shapes on the plot. Save these shapes?')
            if answer is True:
                logger.info('Saving shapes')
                saved = self.save_json()
                if saved:
                    error_check()
                    self.__root.destroy()
                else:
                    return
            elif answer is False:
                logger.info('Dumping unsaved shapes')
                error_check()
                self.__root.destroy()
            elif answer is None:
                return
        else:
            error_check()
            self.__root.destroy()

    ############################################################
    # New functions
    ############################################################
    def goToMain(self):
        self.__drawplot_notebook.select(self.__backscattered532_frame)

    def loadTabs(self, in_type=0, in_xrange=[0,100], in_yrange=[0,30]):
        self.__my_meta_data = MetaData(1, in_xrange[0], in_xrange[1],
                                       in_yrange[0], in_yrange[1], "512")
        for i in range(1,10):
            self.__shapemanagers[i].set_hdf(self.__file)
            self.__p_figs[i].clear()
            self.__figs[i] = self.__p_figs[i].add_subplot(1, 1, 1)

        if self.__tab_buttons[0].get():
            self.set_plot(Plot.baseplot, 0)
        if self.__tab_buttons[1].get():
            self.__my_meta_data._type = 1
            self.set_plot(Plot.backscattered, 1)
        if self.__tab_buttons[2].get():
            self.__my_meta_data._type = 2
            self.set_plot(Plot.depolarized, 2)
        if self.__tab_buttons[3].get():
            self.__my_meta_data._type = 3
            self.set_plot(Plot.vfm, 3)
        if self.__tab_buttons[4].get():
            self.__my_meta_data._type = 4
            self.set_plot(Plot.iwp, 4)
        if self.__tab_buttons[5].get():
            self.__my_meta_data._type = 5
            self.set_plot(Plot.blend, 5)
        if self.__tab_buttons[6].get():
            self.__my_meta_data._type = 6
            self.set_plot(Plot.parallel, 6)
        if self.__tab_buttons[7].get():
            self.__my_meta_data._type = 1
            self.__my_meta_data._wavelength = '1024'
            self.set_plot(Plot.backscattered, 7)
        if self.__tab_buttons[8].get():
            self.__my_meta_data._type = 8
            self.set_plot(Plot.colorratio, 8)
        if self.__tab_buttons[9].get():
            self.__my_meta_data._type = 9
            self.set_plot(Plot.aerosol, 9)

    def toggle_tabs_menu_item(self, btn_iterator, frame):

        if self.__tab_buttons[btn_iterator].get():
            self.__drawplot_notebook.add(frame)
        else:
            self.__drawplot_notebook.hide(frame)

    def create_tab_frames(self):

        self.__tab_buttons[0].set(True) #Meta Tab
        self.__tab_buttons[1].set(True) #Backscatter532
        self.__tab_buttons[2].set(True) #Depolarization
        self.__tab_buttons[3].set(True) # vfm
        self.__tab_buttons[4].set(True) # iwp
        self.__tab_buttons[5].set(False) #placeholder
        self.__tab_buttons[6].set(False) #placeholder
        self.__tab_buttons[7].set(False) #placeholder
        self.__tab_buttons[8].set(False) #placeholder
        self.__tab_buttons[9].set(False) #placeholder

        self.__baseplot_frame = Frame(self.__drawplot_notebook,
                                              width=constants.WIDTH,
                                              height=constants.HEIGHT)

        self.__backscattered532_frame = Frame(self.__drawplot_notebook,
                                              width=constants.WIDTH,
                                              height=constants.HEIGHT)

        self.__depolarized_frame = Frame(self.__drawplot_notebook,
                                         width=constants.WIDTH,
                                         height=constants.HEIGHT)

        self.__vfm_frame = Frame(self.__drawplot_notebook,
                                 width=constants.WIDTH,
                                 height=constants.HEIGHT)

        self.__ice_water_frame = Frame(self.__drawplot_notebook,
                                       width=constants.WIDTH,
                                       height=constants.HEIGHT)

        self.__blend_frame = Frame(self.__drawplot_notebook,
                                   width=constants.WIDTH,
                                   height=constants.HEIGHT)

        self.__parallel_frame = Frame(self.__drawplot_notebook,
                                      width=constants.WIDTH,
                                      height=constants.HEIGHT)

        self.__backscattered1064_frame = Frame(self.__drawplot_notebook,
                                           width=constants.WIDTH,
                                           height=constants.HEIGHT)

        self.__color_ratio_frame = Frame(self.__drawplot_notebook,
                                     width=constants.WIDTH,
                                     height=constants.HEIGHT)

        self.__aerosol_subtype_frame = Frame(self.__drawplot_notebook,
                                         width=constants.WIDTH,
                                         height=constants.HEIGHT)

        if self.__tab_buttons[0].get():
            self.__drawplot_notebook.add(self.__baseplot_frame, text='Meta Data')
        if self.__tab_buttons[1].get():
            self.__drawplot_notebook.add(self.__backscattered532_frame, text='Backscattered 532')
        if self.__tab_buttons[2].get():
            self.__drawplot_notebook.add(self.__depolarized_frame, text='Depolarized')
        if self.__tab_buttons[3].get():
            self.__drawplot_notebook.add(self.__vfm_frame, text='Vertical Feature Mask')
        if self.__tab_buttons[4].get():
            self.__drawplot_notebook.add(self.__ice_water_frame, text='Ice/Water Phase')
        if self.__tab_buttons[5].get():
            self.__drawplot_notebook.add(self.__blend_frame, text='Blend')
        if self.__tab_buttons[6].get():
            self.__drawplot_notebook.add(self.__parallel_frame, text='Parallel')
        if self.__tab_buttons[7].get():
            self.__drawplot_notebook.add(self.__backscattered1064_frame, text='Backscattered 1064')
        if self.__tab_buttons[8].get():
            self.__drawplot_notebook.add(self.__color_ratio_frame, text='Color Ratio')
        if self.__tab_buttons[9].get():
            self.__drawplot_notebook.add(self.__aerosol_subtype_frame, text='Aerosol Subtypes')

    def initiate_figures_and_canvases(self):

        for i in range(1,10):
            self.__p_figs[i] =  Figure(figsize=(11, 16))
            self.__figs[i] = self.__parent_fig.add_subplot(1, 1, 1)
            self.__p_figs[i].set_tight_layout(True)


        #self.__drawplot_canvases[0] = FigureCanvasTkAgg(self.__p_figs[0], master=self.__baseplot_frame)
        self.__drawplot_canvases[1] = FigureCanvasTkAgg(self.__p_figs[1], master=self.__backscattered532_frame)
        self.__drawplot_canvases[2] = FigureCanvasTkAgg(self.__p_figs[2], master=self.__depolarized_frame)
        self.__drawplot_canvases[3] = FigureCanvasTkAgg(self.__p_figs[3], master=self.__vfm_frame)
        self.__drawplot_canvases[4] = FigureCanvasTkAgg(self.__p_figs[4], master=self.__ice_water_frame)
        self.__drawplot_canvases[5] = FigureCanvasTkAgg(self.__p_figs[5], master=self.__blend_frame)
        self.__drawplot_canvases[6] = FigureCanvasTkAgg(self.__p_figs[6], master=self.__parallel_frame)
        self.__drawplot_canvases[7] = FigureCanvasTkAgg(self.__p_figs[7], master=self.__backscattered1064_frame)
        self.__drawplot_canvases[8] = FigureCanvasTkAgg(self.__p_figs[8], master=self.__color_ratio_frame)
        self.__drawplot_canvases[9] = FigureCanvasTkAgg(self.__p_figs[9], master=self.__aerosol_subtype_frame)

    def load_figure_attributes(self, ds_iterator, shape_iterator):

        colormap = ""

        in_type = self.__data_block.get_data_set_type(ds_iterator)
        if in_type == 1:
            colormap = 'dat/calipso-backscatter.cmap'
        elif in_type == 2:
            colormap = 'dat/calipso-depolar.cmap'
        elif in_type == 3:
            colormap = 'dat/calipso-vfm.cmap'
        elif in_type == 4:
            colormap = 'dat/calipso-icewaterphase.cmap'
        elif in_type == 5:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 6:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 7:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 8:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 9:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 10:
            colormap = 'dat/calipso-undefined.cmap'
        else:
            colormap = 'dat/calipso-undefined.cmap'
            # index error unknown colormap###

        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors'] / 255.0)
        cm.set_under(cmap['under'] / 255.0)
        cm.set_over(cmap['over'] / 255.0)
        cm.set_bad(cmap['bad'] / 255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

        if in_type == 1 or in_type == 7:
            data = self.__data_block.get_data_set(ds_iterator, 'transpose')
        else:
            data = self.__data_block.get_data_set(ds_iterator)

        if in_type == 3 or in_type == 4:
            alternate_latitude = self.__data_block.get_alt_latitude(ds_iterator)
        else:
            alternate_latitude = [self.__data_block.get_x_min(ds_iterator, 'latitude'),
                       self.__data_block.get_x_max(ds_iterator, 'latitude')]

        if constants.debug_switch > 0:
            logger.info("***** Preparing 'fig_imshow' *****")
            self.__data_block.print_data_set_info(ds_iterator)

        logger.info("***** Launching 'fig_imshow' *****")

        im = self.__figs[shape_iterator].imshow(
            data,
            extent=
            (
                alternate_latitude[0],
                alternate_latitude[1],
                self.__data_block.get_y_min(ds_iterator),
                self.__data_block.get_y_max(ds_iterator)
            ),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )

        self.__figs[shape_iterator].set_ylabel(self.__data_block.get_data_set_y_label(ds_iterator))
        self.__figs[shape_iterator].set_xlabel(self.__data_block.get_data_set_x_label(ds_iterator))
        title = self.__figs[shape_iterator].set_title(self.__data_block.get_data_set_title(ds_iterator))

        cbar = self.__p_figs[shape_iterator].colorbar(im)
        cbar.set_label(self.__data_block.get_data_set_cbar_label(ds_iterator))

        ax = self.__figs[shape_iterator].twiny()
        ax.set_xlabel(self.__data_block.get_data_set_x_label2(ds_iterator))
        ax.set_xlim(self.__data_block.get_x_min(ds_iterator, 'time'), self.__data_block.get_x_max(ds_iterator, 'time'))
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        ax.xaxis_date()

        self.__figs[shape_iterator].set_zorder(0)
        ax.set_zorder(1)

        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1] * 1.07])

        self.__figs[shape_iterator] = ax

    def stress_test(self):
        fname_V4_L1 = "C:\Users\jjdrisco\Documents\Test Data\Testcase1\CAL_LID_L1-Test0011-Mod001-V4-XX.2007-10-17T17-38-43ZN.hdf"
        fname_V4_L2 = "C:\Users\jjdrisco\Documents\Test Data\Testcase1\CAL_LID_L2_01kmCLay-Test0011-Mod001-V4-XX.2007-10-17T17-38-43ZN.hdf"
        fname_V3_L1 = "C:\Users\jjdrisco\Documents\Test Data\Testcase2\CAL_LID_L1-ValStage1-V3-01.2007-10-17T17-38-43ZN.hdf"
        fname_V3_L2 = "C:\Users\jjdrisco\Documents\Test Data\Testcase2CAL_LID_L2_01kmCLay-ValStage1-V3-01.2007-10-17T17-38-43ZN.hdf"

        #start_time = datetime.datetime.now()
        #my_block = VocalDataBlock(fname_V4_L1)
        #my_block = VocalDataBlock(fname_V4_L2)
        #my_block = VocalDataBlock(fname_V3_L1)
        my_block = VocalDataBlock(fname_V3_L1)

        '''i = my_block.get_figure(MetaData(1, 0, 100, 0, 30, 532))
        i = my_block.get_figure(MetaData(1, 0, 100, 0, 30, 1064))
        i = my_block.get_figure(MetaData(2, 0, 100, 0, 30, 532))
        i = my_block.get_figure(MetaData(2, 0, 100, 0, 30, 1064))'''
        #i = my_block.get_figure(MetaData(3, 0, 1000, 0, 30))
        #my_block.print_data_set_info(i)

def main():
    logger.info("Debug Level = %s" % str(constants.debug_switch))

    # Create Tkinter root and initialize Calipso
    logging.info('Starting CALIPSO program')
    Tk.CallWrapper = Catcher
    rt = Tk()
    logging.info('Instantiate CALIPSO program')
    program = Calipso(rt)

    if constants.debug_switch == 10:
        program.stress_test()
    else:
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

if __name__ == '__main__':
    main()
