######################################
#    Created on Jun 15, 2015
#
#    @author: Grant Mercer
######################################
from Tkinter import Label, Toplevel, Menu, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton, FALSE, BOTTOM, Radiobutton, Entry, X,TOP, LEFT, Y

from PIL import Image, ImageTk  # @UnresolvedImport @UnusedImport
import constants
from tools.toggleablebutton import ToggleableButton, ToolbarToggleableButton
from tools.tooltip import createToolTip
from log import logger
from msilib.schema import RadioButton

class ToolsWindow(Toplevel):
    '''
    Other main portion of the program, the tools window is in charge of managing all
    tool and manipulation related buttons , and is created bound to root but is 
    technically a standalone window.
    '''
    def __init__(self, parent, root):
        '''
        Call base class __init__, also create panes for buttons and setup
        any prerequisite widgets before creating buttons
        :param parent: the class that has this instance of ToolsWindow
        :param root: the root of the program
        '''
        Toplevel.__init__(self, root)
        
        self.__parent = parent
        self.__root = root
        self.plotType = IntVar()
        
        self.title("Tools")
        self.resizable(width=FALSE, height=FALSE)
        self.protocol("WM_DELETE_WINDOW", ToolsWindow.ignore)
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True )    
        
        self.coordinateFrame = Frame(self.container, width=50, height=50)
        self.coordinateFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.coordinateFrame.config(highlightbackground="grey")
        self.coordinateFrame.pack(side=BOTTOM, fill=BOTH, expand=False)                                      
    
    @staticmethod
    def ignore():
        '''
        Do nothing when the user presses the close button
        '''
        pass
        
    def setupToolBarButtons(self):
        '''
        Create tool bar buttons
        '''
        logger.info("Setting up toolbar")
        
        self.upperButtonFrame = Frame(self.container)                                  # upper button frame holding text buttons
        self.upperButtonFrame.pack(side=TOP, fill=X)    
        
        self.resetButton = Button(self.upperButtonFrame, text = "Reset", width = 12, command=self.__parent.reset)
        self.resetButton.grid(row=0, column=0)
        self.renderButton = Button(self.upperButtonFrame, text = "Render", width = 12, height=4, command = self.render)
        self.renderButton.grid(row=0, column=1, rowspan=4, sticky="e")
        
        self.bScattered = Radiobutton(self.upperButtonFrame, text="Backscattered", 
            variable=self.plotType, value=constants.BACKSCATTERED).grid(row=1, column=0, sticky="w")
        self.depolarized = Radiobutton(self.upperButtonFrame, text="Depolarized", 
            variable=self.plotType, value=constants.DEPOLARIZED).grid(row=2, column=0, sticky="w")

        self.upperRangeFrame = Frame(self.container)
        self.upperRangeFrame.pack(side=TOP, fill=X)
        
        Label(self.upperRangeFrame, text="Step").\
            grid(row=3, column=0, pady=5, sticky="w")
        self.beginRangeEntry = Entry(self.upperRangeFrame, width=12)
        self.beginRangeEntry.grid(row=3, column=1, pady=5, sticky="w")
        
        Label(self.upperRangeFrame, text="to").\
            grid(row=3, column=2, pady=5, sticky="w")
        self.endRangeEntry = Entry(self.upperRangeFrame, width=11)
        self.endRangeEntry.grid(row=3, column=3, pady=5, sticky="w")
        
        ###################################Lower Frame##############################################
        
        self.lowerButtonFrame = Frame(self.container)                                  # lower button frame for tools
        self.lowerButtonFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.lowerButtonFrame.config(highlightbackground="grey")
        self.lowerButtonFrame.pack(side=BOTTOM)
        
        lblSpace1 = Label(self.lowerButtonFrame, width=1)     # create space between frame outline
        lblSpace1.grid(row=0, column=0)
            
        lblSpace2 = Label(self.lowerButtonFrame, width=1)
        lblSpace2.grid(row=0, column=5)
        
        # magnify icon
        logger.info("Creating toolbar buttons")
        self.magnifydrawIMG = ImageTk.PhotoImage(file="ico/magnify.png")
        self.__zoomButton = ToolbarToggleableButton(self.__root, self.lowerButtonFrame, lambda : self.__parent.getToolbar().zoom(True), image=self.magnifydrawIMG, width=30, height=30)
        self.__zoomButton.latch(cursor="tcross")
        self.__zoomButton.grid(row=0, column=2, padx=2, pady=5)
        createToolTip(self.__zoomButton, "Zoom to rect")
        
        # plot move cursor icon
        self.plotcursorIMG = ImageTk.PhotoImage(file="ico/plotcursor.png")
        self.__plotCursorButton = ToolbarToggleableButton(self.__root, self.lowerButtonFrame, lambda : self.__parent.getToolbar().pan(True), image=self.plotcursorIMG, width=30, height=30)
        self.__plotCursorButton.latch(cursor="hand1")
        self.__plotCursorButton.grid(row=0, column=1, padx=2, pady=5)
        createToolTip(self.__plotCursorButton, "Move about plot")
        
        # plot undo icon
        self.undoIMG = ImageTk.PhotoImage(file="ico/back.png")
        self.__undoButton = Button(self.lowerButtonFrame, image=self.undoIMG, width=30, height=30, command=lambda : self.__parent.getToolbar().back(True))
        self.__undoButton.grid(row=0, column=3, padx=2, pady=5)
        createToolTip(self.__undoButton, "Previous View")
        
        # plot redo icon
        self.redoIMG = ImageTk.PhotoImage(file="ico/forward.png")
        self.__redoButton = Button(self.lowerButtonFrame, image=self.redoIMG, width=30, height=30, command=lambda : self.__parent.getToolbar().forward(True))
        self.__redoButton.grid(row=0, column=4, padx=2, pady=5)
        createToolTip(self.__redoButton, "Next View")

        # draw rectangle shape
        self.polygonIMG = ImageTk.PhotoImage(file="ico/polygon.png")
        self.__polygonButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.polygonIMG, width=30, height=30)
        self.__polygonButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().anchorRectangle, cursor="tcross")
        self.__polygonButton.latch(key="<B1-Motion>", command=self.__parent.getPolygonList().rubberBand, cursor="tcross")
        self.__polygonButton.latch(key="<ButtonRelease-1>", command=self.__parent.getPolygonList().fillRectangle, cursor="tcross")
        self.__polygonButton.grid(row=1, column=1, padx=2, pady=5)
        createToolTip(self.__polygonButton, "Draw Rect")
        
        # free form shape creation
        self.freedrawIMG = ImageTk.PhotoImage(file="ico/freedraw.png")
        self.__freedrawButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.freedrawIMG, width=30, height=30)
        self.__freedrawButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().plotPoint, cursor="tcross")
        self.__freedrawButton.grid(row=1, column=3, padx= 2, pady=5)
        createToolTip(self.__freedrawButton, "Free Draw")
        
        # move polygon and rectangles around
        self.dragIMG = ImageTk.PhotoImage(file="ico/cursorhand.png")
        self.__dragButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.dragIMG, width=30, height=30)
        self.__dragButton.latch(key="<Button-2>", command=self.__parent.getPolygonList().toggleDrag, cursor="hand1")
        self.__dragButton.grid(row=1, column=2, padx=2, pady=5)
        createToolTip(self.__dragButton, "Drag")
        
        # erase polygon drawings
        self.eraseIMG = ImageTk.PhotoImage(file="ico/eraser.png")
        self.__eraseButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.eraseIMG, width=30, height=30)
        self.__eraseButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().delete, cursor="X_cursor")
        self.__eraseButton.grid(row=1, column=4, padx=2, pady=5)
        createToolTip(self.__eraseButton, "Erase polygon")

        # recolor shapes
        self.paintIMG = ImageTk.PhotoImage(file="ico/paint.png")
        self.__paintButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.paintIMG, width=30, height=30)
        self.__paintButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().paint, cursor="")
        self.__paintButton.grid(row=2, column=2, padx=2, pady=5)
        createToolTip(self.__paintButton, "Paint")

        # outline shapes
        self.outlineIMG = ImageTk.PhotoImage(file="ico/focus.png")
        self.__outlineButton = Button(self.lowerButtonFrame, image=self.outlineIMG, width=30, height=30, command=lambda: self.__parent.getPolygonList().outline())
        self.__outlineButton.grid(row=2, column=1, padx=2, pady=5)
        createToolTip(self.__outlineButton, "Focus")
        
        # hide shapes
        self.plotIMG = ImageTk.PhotoImage(file="ico/hide.png")
        self.__plotButton = Button(self.lowerButtonFrame, image=self.plotIMG, width=30, height=30, command=lambda: self.__parent.getPolygonList().hide())
        self.__plotButton.grid(row=2, column=3, padx=2, pady=5)
        createToolTip(self.__plotButton, "Hide polygons")
        
        # save shapes as JSON
        self.saveIMG = ImageTk.PhotoImage(file="ico/save.png")
        self.__saveButton = Button(self.lowerButtonFrame, image=self.saveIMG, width=30, height=30, command=self.__parent.notifySaveJSON)
        self.__saveButton.grid(row=2, column=4, padx=2, pady=5)
        createToolTip(self.__saveButton, "Save visible\n objects\n to JSON")
        
        # load shapes from JSON
        self.loadIMG = ImageTk.PhotoImage(file="ico/load.png")
        self.__loadButton = Button(self.lowerButtonFrame, image=self.loadIMG, width=30, height=30, command=self.__parent.load)
        self.__loadButton.grid(row=3, column=1, padx=2, pady=5)
        createToolTip(self.__loadButton, "Load JSON")
        
        # retrieve shape properties
        self.propIMG = ImageTk.PhotoImage(file="ico/cog.png")
        self.__propButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.propIMG, width=30, height=30)
        self.__propButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().properties)
        self.__propButton.grid(row=3, column=2, padx=2, pady=5)
        createToolTip(self.__propButton, "Polygon Properties")
        
        # edit shape attributes
        self.editIMG = ImageTk.PhotoImage(file="ico/edit.png")
        self.__editButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.editIMG, width=30, height=30)
        self.__editButton.latch(key="<Button-1>", command=self.__parent.attributeWindow)
        self.__editButton.grid(row=3, column=3, padx=2, pady=5)
        createToolTip(self.__editButton, "Edit Attributes")
        
        self.testIMG = ImageTk.PhotoImage(file="ico/button.png")
        self.__testButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.testIMG, width=30, height=30)
        self.__testButton.latch(key="<Button-1>", command=self.__parent.getPolygonList().extractShapeData)
        self.__testButton.grid(row=3, column=4, padx=2, pady=5)
        createToolTip(self.__editButton, "Test button")
        
    def render(self):
        self.__parent.setPlot(self.plotType)
