from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, HORIZONTAL, BOTH, VERTICAL, Message, TOP, LEFT, \
    SUNKEN
import Tkinter as tk
import logging, os, tkFileDialog, tkMessageBox

from bokeh.colors import white
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk  # @UnresolvedImport @UnusedImport
from attributesdialog import AttributesDialog
import constants
from importdialog import dbDialog
from plot.plot_depolar_ratio import drawDepolar
from plot.plot_uniform_alt_lidar_dev import drawBackscattered
from polygon.list import PolygonList
from tools.navigationtoolbar import NavigationToolbar2CALIPSO
from tools.tools import Observer, Catcher
from toolswindow import ToolsWindow
from log import logger

class Calipso(object):
    '''
    Main class of the application, handles all GUI related events as well as 
    creating other GUI windows such as the toolbar or import dialog
    '''
    def __init__ (self, r):
        logger.info("Instantiating Calipso")        
        self.__root = r                         # root of program
        self.__file =  ''                       # current file in use
        
        # TODO: Add icon for window an task bar
        
        basePane = PanedWindow()                            # main paned window that stretches to fit entire screen
        basePane.pack(fill=BOTH, expand = 1)                # fill and expand
        sectionedPane = PanedWindow(orient=VERTICAL)        # paned window that splits into a top and bottom section
        basePane.add(sectionedPane)
        
        pndwinTop = PanedWindow(sectionedPane, orient=HORIZONTAL)                   # the paned window which holds all buttons
        sectionedPane.add(pndwinTop)                                                # set pndwinTop to sectionedPane
        
        self.__dialogFrame = Frame(pndwinTop)                                       # frame to hold dialog for browsing files
        self.__dialogFrame.pack(side = LEFT)
        
        pndwinBottom = PanedWindow(sectionedPane)                                   # expands the distance below the button
        sectionedPane.add(pndwinBottom)
        self.__drawplotFrame = Frame(pndwinBottom, 
                                     width=constants.WIDTH, 
                                     height=constants.HEIGHT)                       # the frame on which we will set our canvas for drawing etc.
        
        
        self.__child = ToolsWindow(self, r)                                         # tools window which holds all manipulation buttons 
        self.__Parentfig = Figure(figsize=(16,11))                                  # the figure we're drawing our plot to
        self.__fig = None
        self.__drawplotCanvas = FigureCanvasTkAgg(self.__Parentfig,                 # canvas USING the figure we're drawing our plot to \
            master=self.__drawplotFrame)   
        self.__polygonList = PolygonList(self.__drawplotCanvas, self)               # internal polygonList
        observer = Observer(self.__polygonList)
        self.__toolbar = NavigationToolbar2CALIPSO(self.__drawplotCanvas,           # create barebones toolbar we can borrow backend functions from \
            self.__child.coordinateFrame, observer)
        
        
        self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # pack and display canvas
        self.__drawplotFrame.pack()
        
    
    def setupWindow(self):
        '''
        Sets the title of root and invokes py:meth:`centerWindow`
        '''
        logger.info("Setting up window")
        self.__root.title("CALIPSO Visualization Tool")
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        self.x = (sw - constants.WIDTH)/2
        self.y = (sh - constants.HEIGHT)/2
        self.__root.geometry('%dx%d+%d+%d' % (constants.WIDTH, constants.HEIGHT, self.x, self.y))
        # the child is designed to appear off to the right of the parent window, so the x location
        # is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        # plus half the distance of the window
        self.__child.geometry('%dx%d+%d+%d' % (constants.CHILDWIDTH, constants.CHILDHEIGHT, self.x + self.x*4 + 20, self.y + self.y/2))
       
#### MENU BAR ######################################################################################   
    def setupMenu(self):
        '''
        Creates a drop down menu bar
        '''
        logger.info("Setting up menu")
        self.__menuBar = Menu(self.__root)
        
        #File Menu
        self.__menuFile = Menu(self.__menuBar, tearoff=0)
        self.__menuFile.add_command(label="Import File", command=self.importFile)
        self.__menuFile.add_command(label="Save all", command=lambda : self.notifySaveAsJSON(saveAll=True))
        self.__menuFile.add_command(label="Save as", command=self.notifySaveAsJSON)
        self.__menuFile.add_separator()
        self.__menuFile.add_command(label="Exit", command=self.__root.quit)
        self.__menuBar.add_cascade(label="File", menu=self.__menuFile)
        
        #Polygon Menu
        self.__menuPolygon = Menu(self.__menuBar, tearoff=0)
        self.__menuPolygon.add_command(label="Import from Database", command=lambda : dbDialog(self.__root, self))
        self.__menuPolygon.add_command(label="Export to Database", command=self.notifySaveDB)
        self.__menuBar.add_cascade(label="Polygon", menu=self.__menuPolygon)
        
        #Help Menu
        self.__menuHelp = Menu(self.__menuBar, tearoff=0)
        self.__menuHelp.add_command(label="About", command=self.about)
        self.__menuBar.add_cascade(label="Help", menu=self.__menuHelp)
        
        #configure menu to screen
        self.__root.config(menu=self.__menuBar)

    def setPlot(self, plotType):
        '''
        Draws to the canvas according to the *plotType* specified in the arguments. Accepts one of the 
        attributes below
        
        .. py:attribute:: BASE_PLOT
        .. py:attribute:: BACKSCATTERED
        .. py:attribute:: DEPOLARIZED
        .. py:attribute:: VFML
        
        :param int plotType: accepts ``BASE_PLOT, BACKSCATTERED, DEPOLARIZED, VFM``
        '''
        if (plotType) == constants.BASE_PLOT:
            self.__polygonList.setPlot(constants.BASE_PLOT)                                     # sets the screen to a blank canvas
        elif (plotType.get()) == constants.BACKSCATTERED:
            try:
                logger.info("Setting plot to backscattered")
                self.__Parentfig.clear()                                                        # clear the figure
                self.__fig = self.__Parentfig.add_subplot(1,1,1)                                # create subplot
                drawBackscattered(self.__file, self.__fig, self.__Parentfig)                    # plot the backscattered image 
                self.__drawplotCanvas.show()                                                    # show canvas
                self.__polygonList.setPlot(constants.BACKSCATTERED)                             # set the current plot on polygonList
                self.__toolbar.update()                                                         # update toolbar
            except IOError:
                logger.error("IOError, no file exists")
                tkMessageBox.showerror("File Not Found", "No File Exists")                      # error if no file exists in current file var
        elif (plotType.get()) == constants.DEPOLARIZED:
            try:
                logger.info("Setting plot to depolarized")
                self.__Parentfig.clear()                                                        # clear the figure
                self.__fig = self.__Parentfig.add_subplot(1, 1, 1)                              # create subplot
                drawDepolar(self.__file, self.__fig, self.__Parentfig)                          # plot the depolarized image
                self.__polygonList.setPlot(constants.DEPOLARIZED)                               # set the internal plot
                self.__drawplotCanvas.show()                                                    # show plot
                self.__toolbar.update()                                                         # update toolbar
            except IOError:
                logger.error("IOError, no file exists")
                tkMessageBox.showerror("File Not Found", "No File Exists")                      # error if no file exists
        elif (plotType.get()) == constants.VFM:
            logger.error("Accessing unimplemented VFM plot")
            tkMessageBox.showerror("TODO", "Sorry, this plot is currently not implemented")     # vfm doesn't exist
    
    def reset(self):
        '''
        Reset all objects on the screen, move pan to original
        '''
        logger.info("Reseting plot")
        self.__polygonList.reset()  # reset all buttons
        self.__toolbar.home()       # proc toolbar function to reset plot to home
        
    def createTopScreenGUI(self):
        ''' 
        Initializes and creates the file dialog and browse button that appear at the top of the screen
        '''
        logger.info("Creating top screen GUI")
        lblFile=Label(self.__dialogFrame, text="File:")                                 # File label upper:left
        self.__lblFileDialog = Label(self.__dialogFrame, width = 50, justify=LEFT,      # Input box that shows file currently loaded
            bg = white, relief = SUNKEN)
        btnBrowse = Button(self.__dialogFrame, text ='Browse', width = 10,              # same as 'open' option
            command=self.importFile)
        lblFile.grid(row=1, column=0)                                                   # place and pack File labe
        self.__lblFileDialog.grid(row=1, column=1, padx=10)                             # place and pack dialog label
        btnBrowse.grid(row=1, column=3)                                                 # pack and place 
        
    def notifySaveDB(self):
        '''
        Notify the database that a save is taking place, the
        db will then save all polygons present on the screen
        '''
        logger.info("Notified database to save")
        success = self.__polygonList.saveToDB()
        if success:
            logger.info("Success, saved to db")
            tkMessageBox.showinfo("database", "All objects saved to database")
        else:
            logger.error("No objects to be saved")
            tkMessageBox.showerror("database", "No objects to be saved")
            
    def notifySaveJSON(self):
        '''
        Save all shapes on the map inside a JSON object given a previously
        saved file. If no file exists prompt for file
        '''
        logger.info("Notify JSON to save")
        # Save to last saved file, if no file exists prompt to a new file
        if self.__polygonList.getCount() > 0:           
            if self.__polygonList.getFileName() == "":      
                self.notifySaveAsJSON()                     # Still prompt for a file name if none currently exists
            else:
                self.__polygonList.save()                   # Else do a normal save with internal file
        else:
            tkMessageBox.showerror("save as JSON", "No objects to be saved")
            
    def notifySaveAsJSON(self, saveAll=False):
        '''
        Save all shapes on the map given a file specified by the user
        '''
        logger.info("Notify JSON to save as")
        # Save to a file entered by user, saveAll saves ALL objects across canvas
        # and cannot be called as a normal save(must always be save as)
        if self.__polygonList.getCount() > 0:
            options = {}
            options['defaultextension'] = '.json'
            options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
            f = tkFileDialog.asksaveasfilename(**options)
            if f is "":
                return
            if saveAll: self.__polygonList.saveAll(f) 
            else: self.__polygonList.save(f)
        else:
            tkMessageBox.showerror("save as JSON", "No objects to be saved")

    def importFile(self):
        '''
        Load an HDF file for use with displaying backscatter and depolarized images
        '''
        logger.info("Importing HDF file")
        # function to import HDF file used my open and browse
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.__file = fl
            Segments = self.__file.rpartition('/')
            self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
            self.__polygonList.setHDF(self.__file)
        return ''
    
    def load(self):
        '''
        load JSON objects from file by calling :py:meth:`polygonlist.readPlot(f)`
        '''
        logger.info("Loading JSON")
        # loads JSON object by callig the polygonList internal readPlot method
        options = {}
        options['defaultextension'] = '.json'
        options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
        f = tkFileDialog.askopenfilename(**options)
        if f is "":
            return
        self.__polygonList.readPlot(f)
    
    def attributeWindow(self, event):
        '''
        Open attribute window for specifying attributes on objects
        
        :param event: A Tkinter passed event object
        '''
        logger.info("Searching for polygon")
        poly = self.__polygonList.findPolygon(event)
        if poly:
            logger.info("Opening attributes dialog") 
            AttributesDialog(self.__root, poly)

    def getPolygonList(self):
        '''
        Returns the internal :py:class:`polygonList` object
        
        :rtype: :py:class:`polygonList`
        '''
        logger.info("Getting PolygonList")
        return self.__polygonList       # get functions for private varialbes
    
    def getToolbar(self):
        '''
        Returns the internal :py:class:`toolbar` object
        
        :rtype: :py:class:`NavigationToolbar2CALIPSO`
        '''
        logger.info("Getting toolbar")
        return self.__toolbar
    
    def getFig(self):
        '''
        Returns the figure that is plotted to the canvas
        
        :rtype: :py:class:`Figure`
        '''
        logger.info("Getting fig")
        if self.__fig : return self.__fig
        logger.error("Fig does not exist")
        
    def about(self): 
        '''
        Simple TopLevel window displaying the authors
        '''
        logger.info("Opening about window")
        filewin = Toplevel(self.__root)
        filewin.title("About")
        T = Message(filewin, text="NASA DEVELOP\n \nLaRC Spring 2015 Term \nJordan Vaa (Team Lead) \nCourtney Duquette \nAshna Aggarwal \
            \n\nLaRC Summer 2015 Term \nGrant Mercer (Team Lead) \nNathan Qian")
        T.pack()
            
        btnClose = Button(filewin, text="Close", command=filewin.destroy)
        btnClose.pack()  
    
    def setupMainScreen(self):
        '''
        Setup the top GUI, initialize toolbar window and set the plot to a blank image
        '''
        logger.info("Setting up main screen")
        self.createTopScreenGUI()
        self.__child.setupToolBarButtons()
        self.setPlot(constants.BASE_PLOT)
        
def main():
    logging.info("Starting CALIPSO program")
    tk.CallWrapper = Catcher    # Catch Tkinter exceptions to be written by log
    rt = Tk()
    program = Calipso(rt)       # Create main GUI window

    program.setupWindow()       # create window in center screen
    program.setupMenu()         # create top menu
    program.setupMainScreen()   # create top buttons, initialize child and display base_plt
        
    rt.mainloop()               # program main loop
    logging.info("Terminated CALIPSO program")
    os._exit(1)
        
#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    main()
