#### IMPORTS #######################################################################################
from Tkconstants import END
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, HORIZONTAL, BOTH, VERTICAL, Message, TOP, LEFT, SUNKEN, Entry, \
    StringVar
import os
import tkFileDialog
import tkMessageBox

from bokeh.colors import white
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk  # @UnresolvedImport @UnusedImport
from gui import Constants
from gui.PolygonList import PolygonList
from gui.importdialog import dbDialog
from gui.plot.plot_depolar_ratio import drawDepolar
from gui.plot.plot_uniform_alt_lidar_dev import drawBackscattered
from gui.tools import NavigationToolbar2CALIPSO
from gui.toolswindow import ToolsWindow


class Calipso(object):
    '''
    Main class of the application, handles all GUI related events as well as 
    creating other GUI windows such as the toolbar or import dialog
    '''
    def __init__ (self, r):
        self.__root = r                     # root of program
        self.__file =  ''                    # current file in use
        
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
                                     width=Constants.WIDTH, 
                                     height=Constants.HEIGHT)      # the frame on which we will set our canvas for drawing etc.
        
        
        self.__child = ToolsWindow(self, r)       
        # the main canvas we will be drawing our data to
        self.__Parentfig = Figure(figsize=(16,11))
        self.__drawplotCanvas = FigureCanvasTkAgg(self.__Parentfig, master=self.__drawplotFrame)    
        # create tool bar and polygonDrawer     
        self.__toolbar = NavigationToolbar2CALIPSO(self.__drawplotCanvas, self.__child.coordinateFrame)
        # list of object drawn to the screen
        self.__polygonList = PolygonList(self.__drawplotCanvas)
        # show the frame
        self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.__drawplotFrame.pack()
    
    def setupWindow(self):
        self.__root.title("CALIPSO Visualization Tool")
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        self.x = (sw - Constants.WIDTH)/2
        self.y = (sh - Constants.HEIGHT)/2
        self.__root.geometry('%dx%d+%d+%d' % (Constants.WIDTH, Constants.HEIGHT, self.x, self.y))
        # the child is designed to appear off to the right of the parent window, so the x location
        #     is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        #     plus half the distance of the window
        self.__child.geometry('%dx%d+%d+%d' % (Constants.CHILDWIDTH, Constants.CHILDHEIGHT, self.x + self.x*4 + 20, self.y + self.y/2))
       
#### MENU BAR ######################################################################################   
    def setupMenu(self):
        self.__menuBar = Menu(self.__root)
        
        #File Menu
        self.__menuFile = Menu(self.__menuBar, tearoff=0)
        self.__menuFile.add_command(label="Import File", command=self.importFile)
        self.__menuFile.add_command(label="Export Image", command=self.exportImage)
        self.__menuFile.add_separator()
        self.__menuFile.add_command(label="Save", command=self.saveImage)
        self.__menuFile.add_command(label="Save all", command=lambda : self.notifySaveAsJSON(saveAll=True))
        self.__menuFile.add_command(label="Save as", command=self.notifySaveAsJSON)
        self.__menuFile.add_separator()
        self.__menuFile.add_command(label="Properties", command=self.properties)
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
    def setPlot(self, plotType):
        if (plotType) == Constants.BASE_PLOT:
            self.__polygonList.setPlot(Constants.BASE_PLOT)
        elif (plotType.get()) == Constants.BACKSCATTERED:
            try:
                self.__Parentfig.clear()
                self.__fig = self.__Parentfig.add_subplot(1,1,1)
                drawBackscattered(self.__file, self.__fig, self.__Parentfig)
                self.__drawplotCanvas.show()
                self.__polygonList.setPlot(Constants.BACKSCATTERED)
                self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
                self.__toolbar.update()
                self.__drawplotCanvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=0)
            except IOError:
                tkMessageBox.showerror("File Not Found", "No File Exists")
        elif (plotType.get()) == Constants.DEPOLARIZED:
            try:
                self.__Parentfig.clear()
                self.__fig = self.__Parentfig.add_subplot(1, 1, 1)
                drawDepolar(self.__file, self.__fig, self.__Parentfig)
                self.__polygonList.setPlot(Constants.DEPOLARIZED)
                self.__drawplotCanvas.show()
                self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
                self.__toolbar.update()
                self.__drawplotCanvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=0)
            except IOError:
                tkMessageBox.showerror("File Not Found", "No File Exists")
        elif (plotType.get()) == Constants.VFM:
            tkMessageBox.showerror("TODO", "Sorry, this plot is currently not implemented")
    
 
    # Reload the initial image
    def reset(self):
        #reset radio-buttons
        self.__polygonList.reset()
        self.__toolbar.home()
        
    def createTopScreenGUI(self):
        #File Dialog box, - shows the selected __file
        lblFile=Label(self.__dialogFrame, text="File:")
        lblFile.grid(row=1, column=0)
        self.__lblFileDialog = Label(self.__dialogFrame, width = 50, justify=LEFT, bg = white, relief = SUNKEN)
        self.__lblFileDialog.grid(row=1, column=1, padx=10)
        btnBrowse = Button(self.__dialogFrame, text ='Browse', width = 10, command=self.importFile)
        btnBrowse.grid(row=1, column=3)
        
    def notifySaveDB(self):
        # TODO: Check if no objects to be saved, notify if not, 
        # have save returns true false maybe?
        success = self.__polygonList.saveToDB()
        if success:
            tkMessageBox.showinfo("database", "All objects saved to database")
        else:
            tkMessageBox.showerror("database", "No objects to be saved")
            
    def notifySaveJSON(self):
        if self.__polygonList.getCount() > 0:
            if self.__polygonList.getFileName() == "":
                self.notifySaveAsJSON()
            else:
                self.__polygonList.save()
        else:
            tkMessageBox.showerror("save as JSON", "No objects to be saved")
            
    def notifySaveAsJSON(self, saveAll=False):
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
        
    def dbOpenDialog(self):
        dbDialog(self.__root, self)

    def importFile(self):
        ftypes = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
        dlg = tkFileDialog.Open(filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.__file = fl
            Segments = self.__file.rpartition('/')
            self.__lblFileDialog.config(width = 50, bg = white, relief = SUNKEN, justify = LEFT, text = Segments[2])
            self.__polygonList.setHDF(self.__file)
        return ''
    
    def exportImage(self):
        pass

    def saveImage(self):
        pass
    
    def test(self, event):
        result = self.__toolbar.message.get()
        print type(result)
        print self.__toolbar.message.get()
        
    def load(self):
        options = {}
        options['defaultextension'] = '.json'
        options['filetypes'] = [('CALIPSO Data files', '*.json'), ('All files', '*')]
        f = tkFileDialog.askopenfilename(**options)
        if f is "":
            return
        self.__polygonList.readPlot(f)
    
    def attributeWindow(self, event):
        filewin = Toplevel(self.__root, width=950, height=950)
        filewin.title("Edit Attributes")
        self.textbox = Entry(filewin, width=50)
        self.textbox.pack()
        frame = Frame(filewin)
        frame.pack()
        self.string = StringVar()
        self.label = Label(frame, textvariable=self.string, justify=LEFT)
        self.label.grid(row=1, column=0)
        getButton = Button(frame, text="Add", command=lambda: self.getText(event))
        getButton.grid(row=2, column=0)
        closeButton = Button(frame, text="Close", command=filewin.destroy)
        closeButton.grid(row=2, column=1)

    def getText(self, event):
        print self.textbox.get()
        self.text = self.textbox.get()
        try:
            self.__polygonList.edit(event, self.text)
            self.textbox.delete(0, END)
            self.string.set("Added attribute.")
        except Exception:
            self.string.set("Attribute already exists!")
        
    def properties(self):
        pass
    
    def getPolygonList(self):
        return self.__polygonList
    
    def getToolbar(self):
        return self.__toolbar
        
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
        self.setPlot(Constants.BASE_PLOT)
        


#### RUN LINES ##################################################################################        
if __name__ == "__main__":
    rt = Tk()
    program = Calipso(rt)       # Create main GUI window

    program.setupWindow()       # create window in center screen
    program.setupMenu()         # create top menu
    program.setupMainScreen()   # create top buttons, initialize child and display base_plt
        
    rt.mainloop()               # program main loop
    os._exit(1)
