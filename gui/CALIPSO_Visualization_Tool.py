#### IMPORTS #######################################################################################
from Tkinter import Tk, Label, Toplevel, Menu, Text, END, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton, Message, Canvas, CENTER, Scrollbar, BOTTOM, RIGHT, LEFT, X, Y, SUNKEN
import tkFileDialog
from PIL import Image, ImageTk
import sys
from bokeh.colors import white

#### PROGRAM CONSTANTS ####
BASE_PLOT       = 0
BACKSCATTERED   = 1
DEPOLARIZED     = 2
VFM             = 3
HEIGHT          = 665
WIDTH           = 1265

#### START OF CLASS ################################################################################
class Calipso:
    
    def __init__ (self, r):
        self.root = r
        
        self.file = ''
        self.lblFileDialog = Label()
        self.zoomValue=0
        self.imageFilename = ''
        self.zimg_id = None
        self.orig_img = None
        
        
        m1 = PanedWindow()
        m1.pack(fill=BOTH, expand = 1)
        m2 = PanedWindow(orient=VERTICAL)
        m1.add(m2)
        
        self.child = Toplevel()
        
        pndwinTop = PanedWindow(m2, orient=HORIZONTAL)
        m2.add(pndwinTop)
        
        self.frmTop = Frame(pndwinTop)
        self.frmTop.pack(side = LEFT)
        
        pndwinBottom = PanedWindow(m2)
        m2.add(pndwinBottom)
        frmBottom = Frame(pndwinBottom)
        
        xscrollbar = Scrollbar(frmBottom, orient=HORIZONTAL)
        xscrollbar.pack(side = BOTTOM, fill = X)
        yscrollbar = Scrollbar(frmBottom)
        yscrollbar.pack(side = RIGHT, fill = Y)
        self.canvasLower = Canvas(frmBottom, height=HEIGHT, width=WIDTH, scrollregion=(0, 0, 0, 0), xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        
        xscrollbar.config(command=self.canvasLower.xview)
        yscrollbar.config(command=self.canvasLower.yview)
        
        frmBottom.pack()

#### MAIN WINDOW SETUP #############################################################################    
    def centerWindow(self):
        pw = 1275
        ph = 700
        cw = 200
        ch = 350
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - pw)/2
        y = (sh - ph)/2
        self.root.geometry('%dx%d+%d+%d' % (pw, ph, x, y))
        self.child.geometry('%dx%d+%d+%d' % (cw, ch, x + x*4 + 20, y + y/2))
        
    #Creates the GUI window
    def setupWindow(self):
        self.root.title("CALIPSO Visualization Tool")
        self.centerWindow()
       
#### MENU BAR ######################################################################################   
    def importFile(self):
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.file = fl
            Segments = self.file.rpartition('/')
            self.lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
    
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
        filewin = Toplevel(self.root)
        filewin.title("About")
        T = Message(filewin, text="NASA DEVELOP \nLaRC Spring 2015 Term \n \nJordan Vaa (Team Lead) \nCourtney Duquette \nAshna Aggarwal")
        T.pack()
        
        btnClose = Button(filewin, text="Close", command=filewin.destroy)
        btnClose.pack()
        
    def tutorial(self):
        filewin = Toplevel(self.root)
        T = Text(filewin, height=10, width=40, wrap='word')
        T.pack()
        T.insert(END, "This is a tutorial of how to use the CALIPSO Visualization Tool")   
               
    def setupMenu(self):
        menuBar = Menu(self.root)
        
        #File Menu
        menuFile = Menu(menuBar, tearoff=0)
        menuFile.add_command(label="Import File", command=self.importFile)
        menuFile.add_command(label="Export Image", command=self.exportImage)
        menuFile.add_separator()
        menuFile.add_command(label="Save", command=self.saveImage)
        menuFile.add_command(label="Save as", command=self.saveAs)
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.root.quit)
        menuBar.add_cascade(label="File", menu=menuFile)
        
        #Help Menu
        menuHelp = Menu(menuBar, tearoff=0)
        menuHelp.add_command(label="Tutorial", command=self.tutorial)
        menuHelp.add_separator()
        menuHelp.add_command(label="About", command=self.about)
        menuBar.add_cascade(label="Help", menu=menuHelp)
        
        #self.root.bind("<Button-1>", self.zoomIn)
        #self.root.bind("<Button-3>", self.zoomOut)
        #self.canvasLower.bind("<Motion>", self.crop)
        
        #configure menu to screen
        self.root.config(menu=menuBar)

#### MAIN SCREEN #############################################################################
    def addToCanvas(self, pimage):
        # parameter: pimage = image to be drawn on Canvas
        self.canvasLower.create_image(WIDTH // 2, HEIGHT // 2, image=pimage, anchor=CENTER)
        self.canvasLower.image = pimage
        self.canvasLower.pack()
    
    def loadPic(self, imageFilename1, width, height):
        #parameter: imageFilename1 = File name of image to load as PhotoImage
        #           width = desired width of image
        #           height = desired height of image
        imageToLoad = Image.open(imageFilename1)
        self.orig_img = imageToLoad
        imageToLoad = imageToLoad.resize((width, height))
        loadedPhotoImage = ImageTk.PhotoImage(imageToLoad)
        return loadedPhotoImage

    def selPlot(self, plotType):
        #parameter: plotType = int value(0-2) associated with desired plotType
        if (plotType) == BASE_PLOT:
            self.imageFilename = "CALIPSO_A_Train.jpg"
            loadedPhotoImage = self.loadPic(self.imageFilename, WIDTH, HEIGHT)
            self.addToCanvas(loadedPhotoImage)
            
        elif (plotType.get()) == BACKSCATTERED:
            try:
                filename = self.file
                sys.argv = [filename]
                execfile("plot_uniform_alt_lidar_dev.py")
                self.imageFilename = "lidar_backscatter.png"
                
                #refresh image in lower frame 
                loadedPhotoImage = self.loadPic(self.imageFilename, WIDTH, HEIGHT)
                self.addToCanvas(loadedPhotoImage)
            
            except IOError:
                filewin = Toplevel(self.root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n")
        
        elif (plotType.get()) == DEPOLARIZED:
            try:
                filename = self.file
                sys.argv = [filename]
                execfile("plot_depolar_ratio.py")
                self.imageFilename = "depolarization_ratio.png"
                
                #refresh image in lower frame
                loadedPhotoImage = self.loadPic(self.imageFilename, WIDTH, HEIGHT)
                self.addToCanvas(loadedPhotoImage)
            
            except IOError:
                filewin = Toplevel(self.root)
                T = Text(filewin, height=5, width=30)
                T.pack()
                T.insert(END, "No File Exists \n") 
        
        elif (plotType.get()) == VFM:
            filewin = Toplevel(self.root)
            T = Text(filewin, height=5, width=30)
            T.pack()
            T.insert(END, "Sorry, this plot is currently not implemented. \n")
    
    def zoomIn_(self):
        self.zoomValue= self.zoomValue + 1
        if (self.zoomValue) != 0: 
            updatedWidth =  self.zoomValue*2000
            updatedHeight = self.zoomValue*1051
            photoImage = self.loadPic(self.imageFilename, updatedWidth, updatedHeight)
            self.addToCanvas(photoImage)
            self.canvasLower.config(scrollregion=(0, 0, updatedWidth, updatedHeight))
    
    def zoomOut_(self):
        if (self.zoomValue) >= 1:
            self.zoomValue = self.zoomValue-1 
                       
        if (self.zoomValue) > 0:            
            updatedWidth = (1/self.zoomValue)*2000
            updatedHeight = (1/self.zoomValue)*1051
            photoImage = self.loadPic(self.imageFilename, updatedWidth, updatedHeight)
            self.addToCanvas(photoImage)
            self.canvasLower.config(scrollregion=(0, 0, updatedWidth, updatedHeight))
            
        if (self.zoomValue) == 0:
            photoImage = self.loadPic(self.imageFilename, WIDTH, HEIGHT)
            self.addToCanvas(photoImage)
            self.canvasLower.config(scrollregion=(0, 0, 0, 0))
    
    def zoomIn(self, event):
        if self.zoomValue != 4 : self.zoomValue += 1
        self.crop(event)
        
    def zoomOut(self, event):
        if self.zoomValue != 0 : self.zoomValue -= 1
        self.crop(event)
        
    def crop(self, event):
        if self.zimg_id: self.canvasLower.delete(self.zimg_id)
        if (self.zoomValue) != 0:
            x, y = event.x, event.y
            if self.zoomValue == 1:
                tmp = self.orig_img.crop((x-45, y-30, x+45, y+30))
            elif self.zoomValue == 2:
                tmp = self.orig_img.crop((x-30, y-20, x+30, y+20))
            elif self.zoomValue == 3:
                tmp = self.orig_img.crop((x-15, y-10, x+15, y+10))
            elif self.zoomValue == 4:
                tmp = self.orig_img.crop((x-6, y-4, x+6, y+4))
            size = 300, 200
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvasLower.create_image(event.x, event.y, image=self.zimg)
            
                
        
    def reset(self):
        #reset radio-buttons
        self.zoomValue = 0
        self.canvasLower.config(scrollregion=(0, 0, 0, 0))
        self.selPlot(BASE_PLOT)
        self.file = ''
        self.lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = '')
        
    def polygon(self):
        pass
        
    def freeDraw(self):
        pass

    def topPanedWindow(self):
        #File Dialog box, - shows the selected file
        lblFile=Label(self.frmTop, text="File:")
        lblFile.grid(row=1, column=0)
        self.lblFileDialog = Label(self.frmTop, width = 50, bg = white, relief = SUNKEN)
        self.lblFileDialog.grid(row=1, column=1, padx=10)
        
        #Buttons - possible commands
        btnBrowse = Button(self.frmTop, text ='Browse', width = 10, command=self.importFile)
        btnBrowse.grid(row=1, column=3)
        btnZoomIn = Button(self.frmTop, text = "Zoom In", width = 10, command=self.zoomIn_)
        btnZoomIn.grid(row=1, column=5)
        btnZoomOut = Button(self.frmTop, text = "Zoom Out", width = 10, command=self.zoomOut_)
        btnZoomOut.grid(row=1, column=7)
        btnReset = Button(self.frmTop, text = "Reset", width = 10, command=self.reset)
        btnReset.grid(row=1, column=9)
        btnDrawBox = Button(self.frmTop, text = "Polygon", width = 10, command=self.polygon)
        btnDrawBox.grid(row=1, column=11)
        btnFreeDraw = Button(self.frmTop, text = "Free Draw", width = 10, command=self.freeDraw)
        btnFreeDraw.grid(row=1, column=13)
        
        #Plot Type Selection - Radio-button determining how to plot the file
        menubtnPlotSelection = Menubutton(self.frmTop, text="Plot Type", relief=RAISED, width = 23)
        menubtnPlotSelection.grid(row=1, column=15)
        menubtnPlotSelection.menu = Menu(menubtnPlotSelection, tearoff=0)
        menubtnPlotSelection["menu"]=menubtnPlotSelection.menu
        
        plotType = IntVar()
        menubtnPlotSelection.menu.add_radiobutton(label="Backscattered", variable=plotType, value=1, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="Depolarization Ratio", variable=plotType, value=2, command=lambda: self.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="VFM Plot", variable=plotType, value=3, command=lambda: self.selPlot(plotType))
        
        #Spaces between buttons
        lblSpace1 = Label(self.frmTop, width=2)
        lblSpace1.grid(row=1, column=4)
        lblSpace2 = Label(self.frmTop)
        lblSpace2.grid(row=1, column=6)
        lblSpace3 = Label(self.frmTop)
        lblSpace3.grid(row=1, column=8)
        lblSpace4 = Label(self.frmTop)
        lblSpace4.grid(row=1, column=10)
        lblSpace5 = Label(self.frmTop)
        lblSpace5.grid(row=1, column=12)
        lblSpace6 = Label(self.frmTop, width=2)
        lblSpace6.grid(row=1, column=14)
    
    #Setup the body of the GUI, initialize the default image (CALIPSO_A_Train.jpg)
    def setupMainScreen(self):
        self.topPanedWindow()
        self.selPlot(BASE_PLOT)

#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    rt = Tk()
    program = Calipso(rt)

    program.setupWindow()
    program.setupMenu()
    program.setupMainScreen()
        
    rt.mainloop()
