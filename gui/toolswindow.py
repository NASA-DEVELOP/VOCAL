'''
Created on Jun 15, 2015

@author: Grant Mercer
'''
from Tkinter import Label, Toplevel, Menu, PanedWindow, Frame, Button, IntVar, HORIZONTAL, \
    RAISED, BOTH, VERTICAL, Menubutton,FALSE, BOTTOM
from PIL import Image, ImageTk  # @UnresolvedImport @UnusedImport
from gui import Constants
from tools import createToolTip, ToggleableButton, \
    ToolbarToggleableButton

class toolsWindow(Toplevel):
    def __init__(self, parent, root):
        Toplevel.__init__(self, root)
        
        self.__parent = parent
        self.__root = root
        
        self.title("Tools")
        self.resizable(width=FALSE, height=FALSE)
        baseChildPane = PanedWindow(self)
        baseChildPane.pack(fill=BOTH, expand = 1)
        sectionedChildPane = PanedWindow(self, orient=VERTICAL)
        baseChildPane.add(sectionedChildPane)
                
        upperPane = PanedWindow(sectionedChildPane, orient=HORIZONTAL, width=5)
        sectionedChildPane.add(upperPane)
        lowerPane = PanedWindow(sectionedChildPane)
        sectionedChildPane.add(lowerPane)
        
        self.upperButtonFrame = Frame(upperPane)                                  # upper button frame holding text buttons
        self.upperButtonFrame.pack()                                              
            
        self.lowerButtonFrame = Frame(lowerPane)                                  # lower button frame for tools
        self.lowerButtonFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.lowerButtonFrame.config(highlightbackground="grey")
        self.lowerButtonFrame.pack()
        
        self.coordinateFrame = Frame(lowerPane, width=50, height=50)
        self.coordinateFrame.config(highlightthickness=1)                        # create a small border around the frame
        self.coordinateFrame.config(highlightbackground="grey")
        self.coordinateFrame.pack(side=BOTTOM, fill=BOTH)
        
        
        
    def setupToolBarButtons(self):
        ###################################Upper Frame##############################################
        btnReset = Button(self.upperButtonFrame, text = "Reset", width = 10, command=self.__parent.reset)
        btnReset.grid(row=0, column=0, padx=10, pady=5)
        
        #Plot Type Selection - Radio-button determining how to plot the __file
        menubtnPlotSelection = Menubutton(self.upperButtonFrame, text="Plot Type", relief=RAISED, width = 10)
        menubtnPlotSelection.grid(row=0, column=1, padx=10, pady=5)
        menubtnPlotSelection.menu = Menu(menubtnPlotSelection, tearoff=0)
        menubtnPlotSelection["menu"]=menubtnPlotSelection.menu
        
        plotType = IntVar()
        menubtnPlotSelection.menu.add_radiobutton(label="Backscattered", variable=plotType, value=Constants.BACKSCATTERED, command=lambda: self.__parent.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="Depolarization Ratio", variable=plotType, value=Constants.DEPOLARIZED, command=lambda: self.__parent.selPlot(plotType))
        menubtnPlotSelection.menu.add_radiobutton(label="VFM Plot", variable=plotType, value=Constants.VFM, command=lambda: self.__parent.selPlot(plotType))
        
        ###################################Lower Frame##############################################
        
        lblSpace1 = Label(self.lowerButtonFrame, width=1)     # create space between frame outline
        lblSpace1.grid(row=0, column=0)
            
        lblSpace2 = Label(self.lowerButtonFrame, width=1)
        lblSpace2.grid(row=0, column=5)
        
        # magnify icon
        self.magnifydrawIMG = ImageTk.PhotoImage(file="ico/magnify.png")
        self.__zoomButton = ToolbarToggleableButton(self.__root, self.lowerButtonFrame, lambda : self.__parent.toolbar.zoom(True), image=self.magnifydrawIMG, width=30, height=30)
        self.__zoomButton.latch(cursor="tcross")
        self.__zoomButton.grid(row=0, column=2, padx=2, pady=5)
        createToolTip(self.__zoomButton, "Zoom to rect")
        
        # plot move cursor icon
        self.plotcursorIMG = ImageTk.PhotoImage(file="ico/plotcursor.png")
        self.__plotCursorButton = ToolbarToggleableButton(self.__root, self.lowerButtonFrame, lambda : self.__parent.toolbar.pan(True), image=self.plotcursorIMG, width=30, height=30)
        self.__plotCursorButton.latch(cursor="hand1")
        self.__plotCursorButton.grid(row=0, column=1, padx=2, pady=5)
        createToolTip(self.__plotCursorButton, "Move about plot")
        
        # plot undo icon
        self.undoIMG = ImageTk.PhotoImage(file="ico/back.png")
        self.__undoButton = Button(self.lowerButtonFrame, image=self.undoIMG, width=30, height=30, command=lambda : self.__parent.toolbar.back(True))
        self.__undoButton.grid(row=0, column=3, padx=2, pady=5)
        createToolTip(self.__undoButton, "Previous View")
        
        # plot redo icon
        self.redoIMG = ImageTk.PhotoImage(file="ico/forward.png")
        self.__redoButton = Button(self.lowerButtonFrame, image=self.redoIMG, width=30, height=30, command=lambda : self.__parent.toolbar.forward(True))
        self.__redoButton.grid(row=0, column=4, padx=2, pady=5)
        createToolTip(self.__redoButton, "Next View")

        # drawBackscattered rectangle shape
        self.polygonIMG = ImageTk.PhotoImage(file="ico/polygon.png")
        self.__polygonButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.polygonIMG, width=30, height=30)
        self.__polygonButton.latch(key="<Button-1>", command=self.__parent.polygonList.anchorRectangle, cursor="tcross")
        self.__polygonButton.latch(key="<B1-Motion>", command=self.__parent.polygonList.rubberBand, cursor="tcross")
        self.__polygonButton.latch(key="<ButtonRelease-1>", command=self.__parent.polygonList.fillRectangle, cursor="tcross")
        self.__polygonButton.grid(row=1, column=1, padx=2, pady=5)
        createToolTip(self.__polygonButton, "Draw Rect")
        
        # free form shape creation
        self.freedrawIMG = ImageTk.PhotoImage(file="ico/freedraw.png")
        self.__freedrawButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.freedrawIMG, width=30, height=30)
        self.__freedrawButton.latch(key="<Button-1>", command=self.__parent.polygonList.plotPoint, cursor="tcross")
        self.__freedrawButton.grid(row=1, column=3, padx= 2, pady=5)
        createToolTip(self.__freedrawButton, "Free Draw")
        
        # move polygon and rectangles around
        self.dragIMG = ImageTk.PhotoImage(file="ico/cursorhand.png")
        self.__dragButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.dragIMG, width=30, height=30)
        self.__dragButton.latch(key="<Button-2>", command=self.__parent.polygonList.toggleDrag, cursor="hand1")
        self.__dragButton.grid(row=1, column=2, padx=2, pady=5)
        createToolTip(self.__dragButton, "Drag")
        
        # erase polygon drawings
        self.eraseIMG = ImageTk.PhotoImage(file="ico/eraser.png")
        self.__eraseButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.eraseIMG, width=30, height=30)
        self.__eraseButton.latch(key="<Button-1>", command=self.__parent.polygonList.delete, cursor="X_cursor")
        self.__eraseButton.grid(row=1, column=4, padx=2, pady=5)
        createToolTip(self.__eraseButton, "Erase polygon")

        self.paintIMG = ImageTk.PhotoImage(file="ico/paint.png")
        self.__paintButton = ToggleableButton(self.__root, self.lowerButtonFrame, image=self.paintIMG, width=30, height=30)
        self.__paintButton.latch(key="<Button-1>", command=self.__parent.polygonList.paint, cursor="")
        self.__paintButton.grid(row=2, column=2, padx=2, pady=5)
        createToolTip(self.__paintButton, "Paint")

        self.outlineIMG = ImageTk.PhotoImage(file="ico/focus.png")
        self.__outlineButton = Button(self.lowerButtonFrame, image=self.outlineIMG, width=30, height=30, command=lambda: self.__parent.polygonList.outline())
        self.__outlineButton.grid(row=2, column=1, padx=2, pady=5)
        createToolTip(self.__outlineButton, "Focus")
        
        self.plotIMG = ImageTk.PhotoImage(file="ico/hide.png")
        self.__plotButton = Button(self.lowerButtonFrame, image=self.plotIMG, width=30, height=30, command=lambda: self.paren.polygonList.hide())
#       self.__plotButton.latch(key="<Button-1>", command=self.__polygonList.hide, cursor="")
        self.__plotButton.grid(row=2, column=3, padx=2, pady=5)
        createToolTip(self.__plotButton, "Hide polygons")