#### IMPORTS #######################################################################################
from __future__ import print_function
from Tkinter import Tk, Label, Toplevel, Menu, Text, END, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton, Message, Canvas, CENTER, Scrollbar, TOP, BOTTOM, RIGHT, LEFT, X, Y, \
    SUNKEN
import tkFileDialog
from PIL import Image, ImageTk
import sys
from bokeh.colors import white
from tools import createToolTip, ToggleableButton


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
class Calipso:
    
    def __init__ (self, r):
        self.__root = r
        
        self.__file = ''                    # current file in use
        self.__lblFileDialog = Label()      # shows the selected file
        self.__zoomValue=0                  # zoom value in program
        self.__EGzoomValue=0          # zoom value for eye glass
        self.__imageFilename = ''           # name of image file
        self.__zimg_id = None               # for use with crop function, saves previous state
        self.__orig_img = None              # saves original state of image for use with crop
        self.__menuBar = None               # menu bar appearing at top of screen
        self.__menuFile = None              # sub menu
        self.__menuHelp = None              # sub menu
        self.__toggleIsActive = False       # there cannot be more than one toggable tool active at any time
        self.__magnifyMode = False          # zoom in and out boolean
        self.__magnifyButton = None         # zoom in and out button
        self.__polygonMode = False
        self.__polygonButton = None
        self.__freedrawMode = False
        self.__freedrawButton = None
        self.__toggleableMap = []
        
        basePane = PanedWindow()                            # main paned window that stretches to fit entire screen
        basePane.pack(fill=BOTH, expand = 1)                # fill and expand
        sectionedPane = PanedWindow(orient=VERTICAL)        # paned window that splits into a top and bottom section
        basePane.add(sectionedPane)
        
        self.__child = Toplevel()
        self.__child.title("Tools")
        baseChildPane = PanedWindow(self.__child)
        baseChildPane.pack(fill=BOTH, expand = 1)
        sectionedChildPane = PanedWindow(self.__child, orient=VERTICAL)
        baseChildPane.add(sectionedChildPane)
        
        
        upperPane = PanedWindow(sectionedChildPane, orient=HORIZONTAL)
        sectionedChildPane.add(upperPane)
        lowerPane = PanedWindow(sectionedChildPane)
        sectionedChildPane.add(lowerPane)
        
        
        pndwinTop = PanedWindow(sectionedPane, orient=HORIZONTAL)                   # the paned window which holds all buttons
        sectionedPane.add(pndwinTop)                                                # add pndwinTop to sectionedPane
        
        self.__upperButtonFrame = Frame(upperPane)                                       # button frame for child window
        self.__upperButtonFrame.pack()
        
        self.__lowerButtonFrame = Frame(lowerPane)
        self.__lowerButtonFrame.config(highlightthickness=1)
        self.__lowerButtonFrame.config(highlightbackground="grey")
        self.__lowerButtonFrame.pack()
        
        self.__dialogFrame = Frame(pndwinTop)                                       # frame to hold dialog for browsing files
        self.__dialogFrame.pack(side = LEFT)
        
        pndwinBottom = PanedWindow(sectionedPane)                           # expands the distance below the button
        sectionedPane.add(pndwinBottom)
        drawplotFrame = Frame(pndwinBottom)                                 # the frame on which we will add our canvas for drawing etc.
        
        xscrollbar = Scrollbar(drawplotFrame, orient=HORIZONTAL)            # define scroll bars
        xscrollbar.pack(side = BOTTOM, fill = X)
        yscrollbar = Scrollbar(drawplotFrame)
        yscrollbar.pack(side = RIGHT, fill = Y)
        
        # the main canvas we will be drawing our data to
        self.__drawplotCanvas = Canvas(drawplotFrame, height=HEIGHT, width=WIDTH, scrollregion=(0, 0, 0, 0), xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        
        xscrollbar.config(command=self.__drawplotCanvas.xview)
        yscrollbar.config(command=self.__drawplotCanvas.yview)
        
        drawplotFrame.pack()

#### MAIN WINDOW SETUP #############################################################################    
    def centerWindow(self):
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        x = (sw - WIDTH)/2                      # ensure center screen
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
    def importFile(self):
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.__file = fl
            Segments = self.__file.rpartition('/')
            self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
    
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

    # parameter: pimage = image to be drawn on Canvas in the center location
    def addToCanvas(self, pimage):
        self.__drawplotCanvas.create_image(WIDTH // 2, HEIGHT // 2, image=pimage, anchor=CENTER)
        self.__drawplotCanvas.image = pimage
        self.__drawplotCanvas.pack()
    
    # parameter: imageFilename1 = File name of image to load as PhotoImage
    #           width = desired width of image
    #           height = desired height of image
    def loadPic(self, imageFilename1, width, height):
        imageToLoad = Image.open(imageFilename1)
        self.__orig_img = imageToLoad
        imageToLoad = imageToLoad.resize((width, height))
        loadedPhotoImage = ImageTk.PhotoImage(imageToLoad)
        return loadedPhotoImage

    # parameter: plotType = int value(0-2) associated with desired plotType
    def selPlot(self, plotType):
        if (plotType) == BASE_PLOT:
            self.__imageFilename = "CALIPSO_A_Train.jpg"
            loadedPhotoImage = self.loadPic(self.__imageFilename, WIDTH, HEIGHT)
            self.addToCanvas(loadedPhotoImage)
            
        elif (plotType.get()) == BACKSCATTERED:
            try:
                filename = self.__file
                sys.argv = [filename]
                execfile("plot_uniform_alt_lidar_dev.py")
                self.__imageFilename = "lidar_backscatter.png"
                
                #refresh image in lower frame 
                loadedPhotoImage = self.loadPic(self.__imageFilename, WIDTH, HEIGHT)
                self.addToCanvas(loadedPhotoImage)
            
            except IOError:
                filewin = Toplevel(self.__root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n")
        
        elif (plotType.get()) == DEPOLARIZED:
            try:
                filename = self.__file
                sys.argv = [filename]
                execfile("plot_depolar_ratio.py")
                self.__imageFilename = "depolarization_ratio.png"
                
                #refresh image in lower frame
                loadedPhotoImage = self.loadPic(self.__imageFilename, WIDTH, HEIGHT)
                self.addToCanvas(loadedPhotoImage)
            
            except IOError:
                filewin = Toplevel(self.__root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n") 
        
        elif (plotType.get()) == VFM:
            filewin = Toplevel(self.__root)
            T = Text(filewin, height=5, width=30)
            T.pack()
            T.insert(END, "Sorry, this plot is currently not implemented. \n")
    
    def zoomIn_(self):
        self.__zoomValue= self.__zoomValue + 1
        if (self.__zoomValue) != 0: 
            updatedWidth =  self.__zoomValue*2000
            updatedHeight = self.__zoomValue*1051
            photoImage = self.loadPic(self.__imageFilename, updatedWidth, updatedHeight)
            self.addToCanvas(photoImage)
            self.__drawplotCanvas.config(scrollregion=(0, 0, updatedWidth, updatedHeight))
    
    def zoomOut_(self):
        if (self.__zoomValue) >= 1:
            self.__zoomValue = self.__zoomValue-1 
                       
        if (self.__zoomValue) > 0:            
            updatedWidth = (1/self.__zoomValue)*2000
            updatedHeight = (1/self.__zoomValue)*1051
            photoImage = self.loadPic(self.__imageFilename, updatedWidth, updatedHeight)
            self.addToCanvas(photoImage)
            self.__drawplotCanvas.config(scrollregion=(0, 0, updatedWidth, updatedHeight))
            
        if (self.__zoomValue) == 0:
            photoImage = self.loadPic(self.__imageFilename, WIDTH, HEIGHT)
            self.addToCanvas(photoImage)
            self.__drawplotCanvas.config(scrollregion=(0, 0, 0, 0))
    
    def EGzoomIn(self, event):
        if self.__EGzoomValue != 4: self.__EGzoomValue += 1
        self.crop(event)
        
    def EGzoomOut(self, event):
        if self.__EGzoomValue != 0: self.__EGzoomValue -= 1
        self.crop(event)
    
    # Parameters: event object containing the mouse position
    def crop(self, event):
        if self.__zimg_id: self.__drawplotCanvas.delete(self.__zimg_id)
        if (self.__EGzoomValue) != 0:
            x, y = event.x, event.y
            if self.__EGzoomValue == 1:
                tmp = self.__orig_img.crop((x-45, y-30, x+45, y+30))
            elif self.__EGzoomValue == 2:
                tmp = self.__orig_img.crop((x-30, y-20, x+30, y+20))
            elif self.__EGzoomValue == 3:
                tmp = self.__orig_img.crop((x-15, y-10, x+15, y+10))
            elif self.__EGzoomValue == 4:
                tmp = self.__orig_img.crop((x-6, y-4, x+6, y+4))
            size = 300, 200
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.__zimg_id = self.__drawplotCanvas.create_image(event.x, event.y, image=self.zimg)
            
    def EGcleanUp(self):
        if self.z__img_id : self.__drawplotCanvas.delete(self.__zimg_id)

    # Reload the initial image
    def reset(self):
        #reset radio-buttons
        self.__zoomValue = 0
        self.__drawplotCanvas.config(scrollregion=(0, 0, 0, 0))
        self.selPlot(BASE_PLOT)
        self.__file = ''
        self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = '')
        
    def polygon(self, event):
        pass
        
    def freeDraw(self, event):
        pass

    def topPanedWindow(self):
        #File Dialog box, - shows the selected __file
        lblFile=Label(self.__dialogFrame, text="File:")
        lblFile.grid(row=1, column=0)
        self.__lblFileDialog = Label(self.__dialogFrame, width = 50, bg = white, relief = SUNKEN)
        self.__lblFileDialog.grid(row=1, column=1, padx=10)
        btnBrowse = Button(self.__dialogFrame, text ='Browse', width = 10, command=self.importFile)
        btnBrowse.grid(row=1, column=3)
        
        btnZoomIn = Button(self.__upperButtonFrame, text = "Zoom In", width = 10, command=self.zoomIn_)
        btnZoomIn.grid(row=0, column=0, padx=10, pady=5)
        btnZoomOut = Button(self.__upperButtonFrame, text = "Zoom Out", width = 10, command=self.zoomOut_)
        btnZoomOut.grid(row=0, column=1, padx=10, pady=5)
        btnReset = Button(self.__upperButtonFrame, text = "Reset", width = 10, command=self.reset)
        btnReset.grid(row=1, column=0, padx=10, pady=5)
        
        #Plot Type Selection - Radio-button determining how to plot the __file
        menubtnPlotSelection = Menubutton(self.__upperButtonFrame, text="Plot Type", relief=RAISED, width = 10)
        menubtnPlotSelection.grid(row=4, column=0, padx=10, pady=5)
        menubtnPlotSelection.menu = Menu(menubtnPlotSelection, tearoff=0)
        menubtnPlotSelection["menu"]=menubtnPlotSelection.menu
        
        plotType = IntVar()
        menubtnPlotSelection.menu.add_radiobutton(label="Backscattered", variable=plotType, value=BACKSCATTERED, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="Depolarization Ratio", variable=plotType, value=DEPOLARIZED, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="VFM Plot", variable=plotType, value=VFM, command=lambda: self.selPlot(plotType))
        
        ###################################Lower Frame##############################################
        
        lblSpace1 = Label(self.__lowerButtonFrame, width=2)     # create space between frame outline
        lblSpace1.grid(row=0, column=0)
        
        lblSpace2 = Label(self.__lowerButtonFrame, width=2)
        lblSpace2.grid(row=0, column=4)
        
        # polygon icon
        self.polygonIMG = ImageTk.PhotoImage(file="polygon.png")
        self.__polygonButton = Button(self.__lowerButtonFrame, image=self.polygonIMG, width = 30, command=self.togglePolygon)
        createToolTip(self.__polygonButton, "Draw Rect")
        self.__polygonButton.grid(row=0, column=1, padx=2, pady=5)
        
        # free draw icon
        self.freedrawIMG = ImageTk.PhotoImage(file="freedraw.png")
        self.__freedrawButton = Button(self.__lowerButtonFrame, image=self.freedrawIMG, width = 30, command=self.toggleFreeDraw)
        createToolTip(self.__freedrawButton, "Free Draw")
        self.__freedrawButton.grid(row=0, column=2, padx= 2, pady=5)

        # magnify icon
        self.magnifydrawIMG = ImageTk.PhotoImage(file="magnify.png")
        self.__magnifyButton = Button(self.__lowerButtonFrame, image=self.magnifydrawIMG, width=30, command=self.toggleEyeGlassZoom)
        createToolTip(self.__magnifyButton, "Eye Glass")
        self.__magnifyButton.grid(row=0, column=3, padx=2, pady=5)
       
        self.testButton = ToggleableButton(self.__root, self.__lowerButtonFrame, text="this", width=10)
        self.testButton.bind(key="<Button-1>" , command=self.EGzoomIn, cursor="circle")
        self.testButton.bind(key="<Motion>", command=self.crop)
        self.testButton.bind(key="<Button-3>", command=self.EGzoomOut, destructor=self.EGcleanUp)
        self.testButton.grid(row=1, column=0, padx=2, pady=5)

        # 'hacky' solution to execute multiple commands in a lambda, ensures any active buttons are restored
        self.__child.bind("<FocusIn>", 
                          lambda x: [self.toggleEyeGlassZoom(toggle=True), 
                                     self.togglePolygon(toggle=True), 
                                     self.toggleFreeDraw(toggle=True),
                                     self.testButton.unToggle()])
        
    
    # Setup the body of the GUI, initialize the default image (CALIPSO_A_Train.jpg)
    def setupMainScreen(self):
        self.topPanedWindow()
        self.selPlot(BASE_PLOT)
        
    # Parameters: toggle is the override argument that can manually turn off zoom, it is used in the
    #    case that the tools window is re-focused.
    def toggleEyeGlassZoom(self, toggle=False):
        if toggle:              
            self.__root.config(cursor="")                                       # unbind cursor
            self.__magnifyButton.config(relief=RAISED)                          # raise button
            self.__EGzoomValue = 0                                                # reset zoom value
            if self.__zimg_id: self.__drawplotCanvas.delete(self.__zimg_id)     # remove eye glass
            self.__magnifyMode = False                                          # disable magnify mode
        else:
            self.__magnifyMode = not self.__magnifyMode                         # switch value of magnify mode
            if self.__magnifyMode:
                self.__root.config(cursor="circle")                             # new cursor icon for magnify
                self.__magnifyButton.config(relief=SUNKEN)                      # sink button to show eye glass is active
                self.__root.bind("<Button-1>", self.EGzoomIn)                     # bind left and right mouse button to zoom in / zoom out
                self.__root.bind("<Button-3>", self.EGzoomOut)
                self.__drawplotCanvas.bind("<Motion>", self.crop)               # bind any motion to recrop eye glass
            else:
                self.__root.unbind("<Button-1>")
                self.__root.unbind("<Button-3>")                                # unbind mouseb 1 & 3
                self.__drawplotCanvas.unbind("<Motion>")                        # unbind motion
                self.__root.config(cursor="")                                   # put cursor back to normal
                self.__magnifyButton.config(relief=RAISED)                      # raise back button
                
    # Parameters: toggle is the override argument that can manually turn off polygon, it is used in the
    #    case that the tools window is re-focused
    def togglePolygon(self, toggle=False):
        if toggle:
            self.__root.config(cursor="")
            self.__polygonButton.config(relief=RAISED)
            self.__polygonMode = False
        else:
            self.__polygonMode = not self.__polygonMode
            if self.__polygonMode:
                self.__root.config(cursor="tcross")
                self.__polygonButton.config(relief=SUNKEN)
                self.__root.bind("<Button-1>", self.polygon)
            else:
                self.__root.unbind_all(self.polygon)
                self.__root.config(cursor="")
                self.__polygonButton.config(relief=RAISED)
    # Parameters: toggle is the override argument that can manually turn off free draw, it is used in the
    #    case that the tools window is re-focused  
    def toggleFreeDraw(self, toggle=False):
        if toggle:
            self.__root.config(cursor="")
            self.__freedrawButton.config(relief=RAISED)
        else:
            self.__freedrawMode = not self.__freedrawMode
            if self.__freedrawMode:
                # TO-DO custom cursor
                self.__root.config(cursor="tcross")
                self.__freedrawButton.config(relief=SUNKEN)
                self.__root.bind("<Button-1>", self.freeDraw)
            else:
                self.__root.unbind_all(self.freeDraw())
                self.__root.config(cursor="")
                self.__freedrawButton.config(relief=RAISED)
                
    # Parameters: takes a widget that is to be left alone, and untoggles all toggable options
    def unToggleAllBut(self, exception):
        pass    
            
        

#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    rt = Tk()
    program = Calipso(rt)

    program.setupWindow()
    program.setupMenu()
    program.setupMainScreen()
        
    rt.mainloop()
