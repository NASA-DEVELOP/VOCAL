#### IMPORTS #######################################################################################
from Tkinter import Tk, Label, Toplevel, Menu, Text, END, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton, Message, TOP, LEFT, SUNKEN, FALSE
import os
import tkFileDialog

from bokeh.colors import white
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk
from Polygon import PolygonDrawer
from gui.plot_uniform_alt_lidar_dev import draw
from tools import createToolTip, ToggleableButton, NavigationToolbar2CALIPSO, \
    ToolbarToggleableButton





#### PROGRAM CONSTANTS ####
BASE_PLOT       = 0
BACKSCATTERED   = 1
DEPOLARIZED     = 2
VFM             = 3
HEIGHT          = 665
WIDTH           = 1265
CHILDWIDTH      = 200
CHILDHEIGHT     = 300

#### START OF CLASS ################################################################################
class Calipso(object):
    
    def __init__ (self, r):
        self.__root = r                     # root of program
        
        self.__zoomButton = None            # zoom button
        self.__polygonButton = None         # polygon button
        self.__freedrawButton = None        # free draw button
        self.__magnifyButton = None         # magnify button
        self.__dragButton = None
        self.__file = ''                    # current file in use
        self.__lblFileDialog = Label()      # shows the selected file
        self.__zoomValue=0                  # zoom value in program
        self.__EGzoomValue=0                # zoom value for eye glass
        self.__imageFilename = ''           # name of image file
        self.__zimg_id = None               # for use with crop function, saves previous state
        self.__orig_img = None              # saves original state of image for use with crop
        self.__menuBar = None               # menu bar appearing at top of screen
        self.__menuFile = None              # sub menu
        self.__menuHelp = None              # sub menu
        
        ######################################### CREATE MAIN WINDOW #########################################
        basePane = PanedWindow()                            # main paned window that stretches to fit entire screen
        basePane.pack(fill=BOTH, expand = 1)                # fill and expand
        sectionedPane = PanedWindow(orient=VERTICAL)        # paned window that splits into a top and bottom section
        basePane.add(sectionedPane)
        
        pndwinTop = PanedWindow(sectionedPane, orient=HORIZONTAL)                   # the paned window which holds all buttons
        sectionedPane.add(pndwinTop)                                                # add pndwinTop to sectionedPane
        
        self.__dialogFrame = Frame(pndwinTop)                                       # frame to hold dialog for browsing files
        self.__dialogFrame.pack(side = LEFT)
        
        pndwinBottom = PanedWindow(sectionedPane)                                   # expands the distance below the button
        sectionedPane.add(pndwinBottom)
        self.__drawplotFrame = Frame(pndwinBottom, width=WIDTH, height=HEIGHT)      # the frame on which we will add our canvas for drawing etc.
        
        self.__Parentfig = Figure(figsize=(16,11))
        
        # the main canvas we will be drawing our data to
        self.__drawplotCanvas = FigureCanvasTkAgg(self.__Parentfig, master=self.__drawplotFrame)    
        # create tool bar and polygonDrawer     
        self.__toolbar = NavigationToolbar2CALIPSO(self.__drawplotCanvas)
        self.__polygonDrawer = PolygonDrawer(self.__drawplotCanvas)
        
        self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.__drawplotFrame.pack()
        
        ######################################### CREATE CHILD WINDOW #########################################
        
        self.__child = Toplevel()
        self.__child.title("Tools")
        self.__child.resizable(width=FALSE, height=FALSE)
        baseChildPane = PanedWindow(self.__child)
        baseChildPane.pack(fill=BOTH, expand = 1)
        sectionedChildPane = PanedWindow(self.__child, orient=VERTICAL)
        baseChildPane.add(sectionedChildPane)
                
        upperPane = PanedWindow(sectionedChildPane, orient=HORIZONTAL, width=5)
        sectionedChildPane.add(upperPane)
        lowerPane = PanedWindow(sectionedChildPane)
        sectionedChildPane.add(lowerPane)
        
        self.__upperButtonFrame = Frame(upperPane)                                  # upper button frame holding text buttons
        self.__upperButtonFrame.pack()                                              
            
        self.__lowerButtonFrame = Frame(lowerPane)                                  # lower button frame for tools
        self.__lowerButtonFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.__lowerButtonFrame.config(highlightbackground="grey")
        self.__lowerButtonFrame.pack()

#### MAIN WINDOW SETUP #############################################################################    
    def centerWindow(self):
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        x = (sw - WIDTH)/2
        y = (sh - HEIGHT)/2
        self.__root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
        # the child is designed to appear off to the right of the parent window, so the x location
        #     is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        #     plus half the distance of the window
        self.__child.geometry('%dx%d+%d+%d' % (CHILDWIDTH, CHILDHEIGHT, x + x*4 + 20, y + y/2))
        
    #Creates the GUI window
    def setupWindow(self):
        self.__root.title("CALIPSO Visualization Tool")
        self.centerWindow()
       
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
        
        #Help Menu
        self.__menuHelp = Menu(self.__menuBar, tearoff=0)
        self.__menuHelp.add_command(label="Tutorial", command=self.tutorial)
        self.__menuHelp.add_separator()
        self.__menuHelp.add_command(label="About", command=self.about)
        self.__menuBar.add_cascade(label="Help", menu=self.__menuHelp)
        
        #configure menu to screen
        self.__root.config(menu=self.__menuBar)

#### MAIN SCREEN #############################################################################

    # parameter: plotType = int value(0-2) associated with desired plotType
    def selPlot(self, plotType):
        if (plotType) == BASE_PLOT:
            pass
        elif (plotType.get()) == BACKSCATTERED:
            try:
                self.__Parentfig.clear()
                self.__fig = self.__Parentfig.add_subplot(1,1,1)
                draw(self.__file, self.__drawplotCanvas, self.__toolbar, self.__fig, self.__Parentfig)
                self.__drawplotCanvas.show()
                self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
                self.__toolbar.update()
                self.__drawplotCanvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=0)
            except IOError:
                filewin = Toplevel(self.__root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n")
        elif (plotType.get()) == DEPOLARIZED:
            filewin = Toplevel(self.__root)
            T = Text(filewin, height=5, width=30)
            T.pack()
            T.insert(END, "Sorry, this plot is currently not implemented. \n")
        elif (plotType.get()) == VFM:
            filewin = Toplevel(self.__root)
            T = Text(filewin, height=5, width=30)
            T.pack()
            T.insert(END, "Sorry, this plot is currently not implemented. \n")
    
 
    # Reload the initial image
    def reset(self):
        #reset radio-buttons
        self.__polygonDrawer.reset()
        self.__toolbar.home()
        
    def toolbarCleanup(self, str_):
        self.__toolbar._active = str_
        
    def createTopScreenGUI(self):
        #File Dialog box, - shows the selected __file
        lblFile=Label(self.__dialogFrame, text="File:")
        lblFile.grid(row=1, column=0)
        self.__lblFileDialog = Label(self.__dialogFrame, width = 50, justify=LEFT, bg = white, relief = SUNKEN)
        self.__lblFileDialog.grid(row=1, column=1, padx=10)
        btnBrowse = Button(self.__dialogFrame, text ='Browse', width = 10, command=self.importFile)
        btnBrowse.grid(row=1, column=3)
        

        
    def createChildWindowGUI(self):
        btnReset = Button(self.__upperButtonFrame, text = "Reset", width = 10, command=self.reset)
        btnReset.grid(row=0, column=0, padx=10, pady=5)
        
        #Plot Type Selection - Radio-button determining how to plot the __file
        menubtnPlotSelection = Menubutton(self.__upperButtonFrame, text="Plot Type", relief=RAISED, width = 10)
        menubtnPlotSelection.grid(row=0, column=1, padx=10, pady=5)
        menubtnPlotSelection.menu = Menu(menubtnPlotSelection, tearoff=0)
        menubtnPlotSelection["menu"]=menubtnPlotSelection.menu
        
        plotType = IntVar()
        menubtnPlotSelection.menu.add_radiobutton(label="Backscattered", variable=plotType, value=BACKSCATTERED, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="Depolarization Ratio", variable=plotType, value=DEPOLARIZED, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="VFM Plot", variable=plotType, value=VFM, command=lambda: self.selPlot(plotType))
        
        ###################################Lower Frame##############################################
        
        lblSpace1 = Label(self.__lowerButtonFrame, width=1)     # create space between frame outline
        lblSpace1.grid(row=0, column=0)
            
        lblSpace2 = Label(self.__lowerButtonFrame, width=1)
        lblSpace2.grid(row=0, column=5)
        
        # NOTE : See tools.py for documentation on these wrapper classes
        
        # magnify icon
        self.magnifydrawIMG = ImageTk.PhotoImage(file="ico/magnify.png")
        self.__zoomButton = ToolbarToggleableButton(self.__root, self.__lowerButtonFrame, self.__toolbar.zoom, image=self.magnifydrawIMG, width=30, height=30)
        self.__zoomButton.latch(cursor="tcross", destructor=self.__toolbar.zoom)
        self.__zoomButton.grid(row=0, column=2, padx=2, pady=5)
        createToolTip(self.__zoomButton, "Zoom to rect")
        
        # plot move cursor icon
        self.plotcursorIMG = ImageTk.PhotoImage(file="ico/plotcursor.png")
        self.__plotCursorButton = ToolbarToggleableButton(self.__root, self.__lowerButtonFrame, lambda : self.__toolbar.pan(True), image=self.plotcursorIMG, width=30, height=30)
        self.__plotCursorButton.latch(cursor="hand1", destructor=lambda : self.toolbarCleanup('PAN'))
        self.__plotCursorButton.grid(row=0, column=1, padx=2, pady=5)
        createToolTip(self.__plotCursorButton, "Move about plot")
        
        # plot undo icon
        self.undoIMG = ImageTk.PhotoImage(file="ico/back.png")
        self.__undoButton = Button(self.__lowerButtonFrame, image=self.undoIMG, width=30, height=30, command=lambda : self.__toolbar.back(True))
        self.__undoButton.grid(row=0, column=3, padx=2, pady=5)
        createToolTip(self.__undoButton, "Previous View")
        
        # plot redo icon
        self.redoIMG = ImageTk.PhotoImage(file="ico/forward.png")
        self.__redoButton = Button(self.__lowerButtonFrame, image=self.redoIMG, width=30, height=30, command=lambda : self.__toolbar.forward(True))
        self.__redoButton.grid(row=0, column=4, padx=2, pady=5)
        createToolTip(self.__redoButton, "Next View")
        
        # draw rectangle shape
        self.polygonIMG = ImageTk.PhotoImage(file="ico/polygon.png")
        self.__polygonButton = ToggleableButton(self.__root, self.__lowerButtonFrame, image=self.polygonIMG, width=30, height=30)
        self.__polygonButton.latch(key="<Button-1>", command=self.__polygonDrawer.anchorRectangle, cursor="tcross")
        self.__polygonButton.latch(key="<B1-Motion>", command=self.__polygonDrawer.rubberBand, cursor="tcross")
        self.__polygonButton.latch(key="<ButtonRelease-1>", command=self.__polygonDrawer.fillRectangle, cursor="tcross")
        self.__polygonButton.grid(row=1, column=1, padx=2, pady=5)
        createToolTip(self.__polygonButton, "Draw Rect")
        
        # free form shape creation
        self.freedrawIMG = ImageTk.PhotoImage(file="ico/freedraw.png")
        self.__freedrawButton = ToggleableButton(self.__root, self.__lowerButtonFrame, image=self.freedrawIMG, width=30, height=30)
        self.__freedrawButton.latch(key="<Button-1>", command=self.__polygonDrawer.plotPoint, cursor="tcross")
        self.__freedrawButton.grid(row=1, column=3, padx= 2, pady=5)
        createToolTip(self.__freedrawButton, "Free Draw")
        
        # move polygon and rectangles around
        self.dragIMG = ImageTk.PhotoImage(file="ico/cursorhand.png")
        self.__dragButton = ToggleableButton(self.__root, self.__lowerButtonFrame, image=self.dragIMG, width=30, height=30)
        self.__dragButton.latch(key="<Button-2>", command=self.__polygonDrawer.toggleDrag, cursor="hand1")
        self.__dragButton.grid(row=1, column=2, padx=2, pady=5)
        createToolTip(self.__dragButton, "Drag")
        
        # erase polygon drawings
        self.eraseIMG = ImageTk.PhotoImage(file="ico/eraser.png")
        self.__eraseButton = ToggleableButton(self.__root, self.__lowerButtonFrame, image=self.eraseIMG, width=30, height=30)
        self.__eraseButton.latch(key="<Button-1>", command=self.__polygonDrawer.delete, cursor="X_cursor")
        self.__eraseButton.grid(row=1, column=4, padx=2, pady=5)
        createToolTip(self.__eraseButton, "Erase polygon")
        
        self.outlineIMG = ImageTk.PhotoImage(file="ico/focus.png")
        self.__outlineButton = Button(self.__lowerButtonFrame, image=self.outlineIMG, width=30, height=30, command=lambda: self.__polygonDrawer.outline())
        self.__outlineButton.grid(row=2, column=1, padx=2, pady=5)
        createToolTip(self.__outlineButton, "Focus")
        
        self.paintIMG = ImageTk.PhotoImage(file="ico/paint.png")
        self.__paintButton = ToggleableButton(self.__root, self.__lowerButtonFrame, image=self.paintIMG, width=30, height=30)
        self.__paintButton.latch(key="<Button-1>", command=self.__polygonDrawer.paint, cursor="")
        self.__paintButton.grid(row=2, column=2, padx=2, pady=5)
        createToolTip(self.__paintButton, "Paint")
        
        self.plotIMG = ImageTk.PhotoImage(file="ico/hide.png")
        self.__plotButton = Button(self.__lowerButtonFrame, image=self.plotIMG, width=30, height=30, command=lambda: self.__polygonDrawer.hide())
#         self.__plotButton.latch(key="<Button-1>", command=self.__polygonDrawer.hide, cursor="")
        self.__plotButton.grid(row=2, column=3, padx=2, pady=5)
        createToolTip(self.__plotButton, "Hide polygons")
       
        # 'hacky' solution. Lambdas cannot have more than one statement ... however a lambda will
        # evaluate an array so we can use some arbitrary array and place our commands inside that 
        # array. Here we simply bind focusing back into the child window as a way to automatically
        # unbind the toggleable buttons
        #self.__child.bind("<FocusIn>", 
        #                  lambda x: [ 
        #                             self.__polygonButton.unToggle(), 
        #                             self.__freedrawButton.unToggle(),
        #                             self.__zoomButton.unToggle(),
        #                             self.__dragButton.unToggle()])

    def importFile(self):
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.__file = fl
            Segments = self.__file.rpartition('/')
            self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
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
        
    def tutorial(self):
        filewin = Toplevel(self.__root)
        T = Text(filewin, height=10, width=40, wrap='word')
        T.pack()
        T.insert(END, "This is a tutorial of how to use the CALIPSO Visualization Tool")   
    
    # Setup the body of the GUI, initialize the default image (CALIPSO_A_Train.jpg)
    def setupMainScreen(self):
        self.createTopScreenGUI()
        self.createChildWindowGUI()
        self.selPlot(BASE_PLOT)
        


#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    rt = Tk()
    program = Calipso(rt)

    program.setupWindow()
    program.setupMenu()
    program.setupMainScreen()
        
    rt.mainloop()
    os._exit(1)
