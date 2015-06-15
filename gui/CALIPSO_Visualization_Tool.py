#### IMPORTS #######################################################################################
from Tkinter import Tk, Label, Toplevel, Menu, Text, END, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton, Message, TOP, LEFT, SUNKEN, FALSE, BOTTOM, SW
import os
import tkFileDialog

from bokeh.colors import white
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk
from gui import Constants
from gui.PolygonList import PolygonList
from gui.plot.plot_depolar_ratio import drawDepolar
from gui.plot.plot_uniform_alt_lidar_dev import drawBackscattered
from tools import createToolTip, ToggleableButton, NavigationToolbar2CALIPSO, \
    ToolbarToggleableButton
from toolswindow import toolsWindow

#### PROGRAM CONSTANTS ####
HEIGHT          = 665
WIDTH           = 1265
CHILDWIDTH      = 200
CHILDHEIGHT     = 300

#### START OF CLASS ################################################################################
class Calipso(object):
    
    def __init__ (self, r):
        self.__root = r                     # root of program
        self.__file = ''                    # current file in use
        ######################################### CREATE MAIN WINDOW #########################################
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
        self.__drawplotFrame = Frame(pndwinBottom, width=WIDTH, height=HEIGHT)      # the frame on which we will set our canvas for drawing etc.
        
        self.__Parentfig = Figure(figsize=(16,11))
        
        ######################################### CREATE CHILD WINDOW #########################################
        
        self.__child = toolsWindow(self, r)
        
        ######################################### INIT CANVAS #########################################

        # the main canvas we will be drawing our data to
        self.__drawplotCanvas = FigureCanvasTkAgg(self.__Parentfig, master=self.__drawplotFrame)    
        # create tool bar and polygonDrawer     
        self.toolbar = NavigationToolbar2CALIPSO(self.__drawplotCanvas, self.__child.coordinateFrame)
        # list of object drawn to the screen
        self.polygonList = PolygonList(self.__drawplotCanvas)
        # show the frame
        self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.__drawplotFrame.pack()
        
    @staticmethod
    def ignore():
        pass

#### MAIN WINDOW SETUP #############################################################################            
    #Creates the GUI window
    def setupWindow(self):
        self.__root.title("CALIPSO Visualization Tool")
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        self.x = (sw - WIDTH)/2
        self.y = (sh - HEIGHT)/2
        self.__root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, self.x, self.y))
        # the child is designed to appear off to the right of the parent window, so the x location
        #     is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        #     plus half the distance of the window
        self.__child.geometry('%dx%d+%d+%d' % (CHILDWIDTH, CHILDHEIGHT, self.x + self.x*4 + 20, self.y + self.y/2))
       
#### MENU BAR ######################################################################################   
    def setupMenu(self):
        self.__menuBar = Menu(self.__root)
        
        #File Menu
        self.__menuFile = Menu(self.__menuBar, tearoff=0)
        self.__menuFile.add_command(label="Import File", command=self.importFile)
        self.__menuFile.add_command(label="Export Image", command=self.exportImage)
        self.__menuFile.add_separator()
        self.__menuFile.add_command(label="Save", command=self.saveImage)
        self.__menuFile.add_command(label="Save as", command=self.saveAs)
        self.__menuFile.add_separator()
        self.__menuFile.add_command(label="Exit", command=self.__root.quit)
        self.__menuBar.add_cascade(label="File", menu=self.__menuFile)
        
        #Polygon Menu
        self.__menuPolygon = Menu(self.__menuBar, tearoff=0)
        self.__menuPolygon.add_command(label="Import from Database", command=self.dbOpenDialog)
        self.__menuPolygon.add_command(label="Export to Database", command=self.notifySaveDB)
        self.__menuBar.add_cascade(label="Polygon", menu=self.__menuPolygon)
        
        #Help Menu
        self.__menuHelp = Menu(self.__menuBar, tearoff=0)
        self.__menuHelp.add_command(label="About", command=self.about)
        self.__menuBar.add_cascade(label="Help", menu=self.__menuHelp)
        
        
        
        #configure menu to screen
        self.__root.config(menu=self.__menuBar)

#### MAIN SCREEN #############################################################################

    # parameter: plotType = int value(0-2) associated with desired plotType
    def selPlot(self, plotType):
        if (plotType) == Constants.BASE_PLOT:
            self.polygonList.setPlot(Constants.BASE_PLOT)
        elif (plotType.get()) == Constants.BACKSCATTERED:
            try:
                self.__Parentfig.clear()
                self.__fig = self.__Parentfig.add_subplot(1,1,1)
                drawBackscattered(self.__file, self.__fig, self.__Parentfig)
                self.__drawplotCanvas.show()
                self.polygonList.setPlot(Constants.BACKSCATTERED)
                self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
                self.toolbar.update()
                self.__drawplotCanvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=0)
            except IOError:
                filewin = Toplevel(self.__root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n")
        elif (plotType.get()) == Constants.DEPOLARIZED:
            try:
                self.__Parentfig.clear()
                self.__fig = self.__Parentfig.add_subplot(1, 1, 1)
                drawDepolar(self.__file, self.__fig, self.__Parentfig)
                self.polygonList.setPlot(Constants.DEPOLARIZED)
                self.__drawplotCanvas.show()
                self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
                self.toolbar.update()
                self.__drawplotCanvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=0)
            except IOError:
                filewin = Toplevel(self.__root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n")
        elif (plotType.get()) == Constants.VFM:
            filewin = Toplevel(self.__root)
            T = Text(filewin, height=5, width=30)
            T.pack()
            T.insert(END, "Sorry, this plot is currently not implemented. \n")
    
 
    # Reload the initial image
    def reset(self):
        #reset radio-buttons
        self.polygonList.reset()
        self.toolbar.home()
        
    def createTopScreenGUI(self):
        #File Dialog box, - shows the selected __file
        lblFile=Label(self.__dialogFrame, text="File:")
        lblFile.grid(row=1, column=0)
        self.__lblFileDialog = Label(self.__dialogFrame, width = 50, justify=LEFT, bg = white, relief = SUNKEN)
        self.__lblFileDialog.grid(row=1, column=1, padx=10)
        btnBrowse = Button(self.__dialogFrame, text ='Browse', width = 10, command=self.importFile)
        btnBrowse.grid(row=1, column=3)
        
    def notifySaveDB(self):
        self.polygonList.save()
        filewin = Toplevel(self.__root)
        filewin.title("Notice")
        filewin.geometry('%dx%d+%d+%d' % (100, 75, self.x + self.x*2 - 60, self.y + self.y/2 + 160))
        T = Message(filewin, text="JSON written to gui/objs/", anchor=SW)
        T.pack()
            
        btnClose = Button(filewin, text="Close", command=filewin.destroy)
        btnClose.pack()
        
    def dbOpenDialog(self):
        pass

    def importFile(self):
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.__file = fl
            Segments = self.__file.rpartition('/')
            self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
            self.polygonList.setHDF(self.__file)
        return ''
    
    def exportImage(self):
        pass

    def saveImage(self):
        pass
    
    def saveAs(self):
        options = {}
        options['defaultextension'] = '.hdf'
        options['filetypes'] = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        tkFileDialog.asksaveasfile(mode='w', **options)
        
    def about(self): 
        filewin = Toplevel(self.__root)
        filewin.title("About")
        T = Message(filewin, text="NASA DEVELOP \nLaRC Spring 2015 Term \n \nJordan Vaa (Team Lead) \nCourtney Duquette \nAshna Aggarwal")
        T.pack()
            
        btnClose = Button(filewin, text="Close", command=filewin.destroy)
        btnClose.pack()  
    
    # Setup the body of the GUI, initialize the default image (CALIPSO_A_Train.jpg)
    def setupMainScreen(self):
        self.createTopScreenGUI()
        self.__child.setupToolBarButtons()
        self.selPlot(Constants.BASE_PLOT)
        


#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    rt = Tk()
    program = Calipso(rt)
    
    program.setupWindow()
    program.setupMenu()
    program.setupMainScreen()
        
    rt.mainloop()
    os._exit(1)
