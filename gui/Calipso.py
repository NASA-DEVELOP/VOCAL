#### IMPORTS #######################################################################################
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, HORIZONTAL, BOTH, VERTICAL, Message, TOP, LEFT, \
    SUNKEN
import os
import tkFileDialog
import tkMessageBox

from bokeh.colors import white
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk  # @UnresolvedImport @UnusedImport
from gui import Constants
from gui.PolygonList import PolygonList
from gui.attributesDialog import AttributesDialog
from gui.importdialog import dbDialog
from gui.plot.plot_depolar_ratio import drawDepolar
from gui.plot.plot_uniform_alt_lidar_dev import drawBackscattered
from gui.tools import NavigationToolbar2CALIPSO, Observer
from gui.toolswindow import ToolsWindow


class Calipso(object):
    '''
    Main class of the application, handles all GUI related events as well as 
    creating other GUI windows such as the toolbar or import dialog
    '''
    def __init__ (self, r):
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
                                     width=Constants.WIDTH, 
                                     height=Constants.HEIGHT)                       # the frame on which we will set our canvas for drawing etc.
        
        
        self.__child = ToolsWindow(self, r)                                         # tools window which holds all manipulation buttons 
        self.__Parentfig = Figure(figsize=(16,11))                                  # the figure we're drawing our plot to
        self.__drawplotCanvas = FigureCanvasTkAgg(self.__Parentfig,                 # canvas USING the figure we're drawing our plot to \
            master=self.__drawplotFrame)   
        self.__polygonList = PolygonList(self.__drawplotCanvas, self)               # internal polygonList
        observer = Observer(self.__polygonList)
        self.__toolbar = NavigationToolbar2CALIPSO(self.__drawplotCanvas,           # create barebones toolbar we can borrow backend functions from \
            self.__child.coordinateFrame, observer)
        
        
        self.__drawplotCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)   # pack and display canvas
        self.__drawplotFrame.pack()
    
    def setupWindow(self):
        self.__root.title("CALIPSO Visualization Tool")
        sw = self.__root.winfo_screenwidth()
        sh = self.__root.winfo_screenheight()
        self.x = (sw - Constants.WIDTH)/2
        self.y = (sh - Constants.HEIGHT)/2
        self.__root.geometry('%dx%d+%d+%d' % (Constants.WIDTH, Constants.HEIGHT, self.x, self.y))
        # the child is designed to appear off to the right of the parent window, so the x location
        # is parentWindow.x + the length of the window + padding, and y is simply the parentWindow.y
        # plus half the distance of the window
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
        Plots data from the loaded HDF file given a plotType param passed via 
        the radio button menu
        '''
        if (plotType) == Constants.BASE_PLOT:
            self.__polygonList.setPlot(Constants.BASE_PLOT)                                     # sets the screen to a blank canvas
        elif (plotType.get()) == Constants.BACKSCATTERED:
            try:
                self.__Parentfig.clear()                                                        # clear the figure
                self.__fig = self.__Parentfig.add_subplot(1,1,1)                                # create subplot
                drawBackscattered(self.__file, self.__fig, self.__Parentfig)                    # plot the backscattered image 
                self.__drawplotCanvas.show()                                                    # show canvas
                self.__polygonList.setPlot(Constants.BACKSCATTERED)                             # set the current plot on polygonList
                self.__toolbar.update()                                                         # update toolbar
            except IOError:
                tkMessageBox.showerror("File Not Found", "No File Exists")                      # error if no file exists in current file var
        elif (plotType.get()) == Constants.DEPOLARIZED:
            try:
                self.__Parentfig.clear()                                                        # clear the figure
                self.__fig = self.__Parentfig.add_subplot(1, 1, 1)                              # create subplot
                drawDepolar(self.__file, self.__fig, self.__Parentfig)                          # plot the depolarized image
                self.__polygonList.setPlot(Constants.DEPOLARIZED)                               # set the internal plot
                self.__drawplotCanvas.show()                                                    # show plot
                self.__toolbar.update()                                                         # update toolbar
            except IOError:
                tkMessageBox.showerror("File Not Found", "No File Exists")                      # error if no file exists
        elif (plotType.get()) == Constants.VFM:
            tkMessageBox.showerror("TODO", "Sorry, this plot is currently not implemented")     # vfm doesn't exist
    
    
 
    def reset(self):
        '''
        Reset all objects on the screen, move pan to original
        '''
        self.__polygonList.reset()  # reset all buttons
        self.__toolbar.home()       # proc toolbar function to reset plot to home
        
    def createTopScreenGUI(self):
        ''' 
        Create buttons associated with the top GUI e.g. File label, browse
        '''
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
        success = self.__polygonList.saveToDB()
        if success:
            tkMessageBox.showinfo("database", "All objects saved to database")
        else:
            tkMessageBox.showerror("database", "No objects to be saved")
            
    def notifySaveJSON(self):
        '''
        Save all shapes on the map inside a JSON object given a previously
        saved file. If no file exists prompt for file
        '''
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
    
    def exportImage(self):
        pass

    def saveImage(self):
        pass

    def load(self):
        '''
        load JSON objects from file by aclling polygonlist.readPlot(f)
        '''
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
        '''
        poly = self.__polygonList.findPolygon(event)
        AttributesDialog(self.__root, poly)

    def getPolygonList(self):
        '''
        Returns polygonList
        '''
        return self.__polygonList       # get functions for private varialbes
    
    def getToolbar(self):
        '''
        Returns toolbar
        '''
        return self.__toolbar
    
    def getFig(self):
        return self.__fig
        
    def about(self): 
        '''
        Simple TopLevel window displaying the authors
        '''
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
