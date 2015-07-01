######################################
#    Created on Jun 11, 2015
#
#    @author: nqian
######################################
# import antigravity
from datetime import datetime
from tkColorChooser import askcolor
import tkMessageBox

import constants
from db import db
from polygon.drawer import PolygonDrawer
from polygon.reader import PolygonReader
from log import logger

class PolygonList(object):
    '''
    Manages all polygons present on the screen, writes to db on call
    
    :param canvas: Canvas to draw polygons to
    :param master: Calipso alias
    '''

    outlineToggle = True
    hideToggle = True

    def __init__(self, canvas, master):
        '''
        Constructor
        '''
        self.__canvas = canvas
        self.__master = master
        logger.info("Define initial polygonList")
        self.__polygonList = [[PolygonDrawer(canvas, self.__master)],      # base plot list
                              [PolygonDrawer(canvas, self.__master)],      # backscattered list
                              [PolygonDrawer(canvas, self.__master)],      # depolarized list
                              [PolygonDrawer(canvas, self.__master)]]      # vfm list
        self.__currentList = None           # manipulates polygonList through aliasing
        self.__currentFile = ""
        logger.info("Instantiate polygonReader")
        self.__polyReader = PolygonReader()
        self.__hdf = ''
        self.__plot = constants.BASE_PLOT_STR
        logger.info("Query db for unique tag")
        self.__count = db.queryUniqueTag()
        self.__data = {}
        self.__drag_data = {"x": 0, "y": 0, "mx": 0, "my": 0, "item": None}
        
        self.__canvas._tkcanvas.tag_bind("polygon", "<Button-1>", self.onTokenButtonPress)
        self.__canvas._tkcanvas.tag_bind("polygon", "<ButtonRelease-1>", self.onTokenButtonRelease)
        self.__canvas._tkcanvas.tag_bind("polygon", "<B1-Motion>", self.onTokenMotion)
        
    # TODO: fix dragging
    def onTokenButtonPress(self, event):
        '''
        Saves the target polygon's original position for movement tracking
        
        :param event: Tkinter passed event object
        '''
        if PolygonDrawer.dragToggle:
            logger.info("Searching for nearset polygon")
            self.__drag_data["item"] = self.__canvas._tkcanvas.find_closest(event.x, event.y)[0]
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
            string = self.__master.getToolbar().message.get()
            x = string[2:15].strip()
            y = string[17:].strip()
            self.__drag_data["mx"] = float(x)
            self.__drag_data["my"] = float(y)
        
    def onTokenButtonRelease(self, event):
        '''
        Clears data on movement tracking
        
        :param event: Tkinter passed event object
        '''
        if PolygonDrawer.dragToggle:
            logger.info("Mouse relased on dragging")
            self.__drag_data["item"] = None
            self.__drag_data["x"] = 0
            self.__drag_data["y"] = 0
            self.__drag_data["mx"] = 0
            self.__drag_data["my"] = 0
        
    def onTokenMotion(self, event):
        '''
        Calculates how far the polygon has moved and redraws the shape
        
        :param event: Tkinter passed event object
        '''
        if PolygonDrawer.dragToggle:
            logger.info("Received mouse motion for dragging")
            string = self.__master.getToolbar().message.get()
            x = string[2:15].strip()
            y = string[17:].strip()
            dx = event.x - self.__drag_data["x"]
            dy = event.y - self.__drag_data["y"]
            dmx = float(x) - self.__drag_data["mx"]
            dmy = float(y) - self.__drag_data["my"]
            self.__canvas._tkcanvas.move(self.__drag_data["item"], dx, dy)
            for shape in self.__currentList:
                if shape.getItemHandler() is self.__drag_data["item"]:
                    shape.move(dx, dy, dmx, dmy)
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
            self.__drag_data["mx"] = float(x)
            self.__drag_data["my"] = float(y)
    
    def setPlot(self, plot):
        '''
        Determines which list currentList should alias
        
        :param int plot: Value for setting plot
        '''
        newPlot = ""
        if plot == 0:
            logger.warning("Set plot for PolygonList to base plot")
            self.__currentList = self.__polygonList[constants.BASE_PLOT]
            newPlot = constants.BASE_PLOT_STR
        elif plot == 1:
            logger.info("Set plot for PolygonList to backscattered")
            self.__currentList = self.__polygonList[constants.BACKSCATTERED]
            newPlot = constants.BACKSCATTERED_STR
            if len(self.__polygonList[constants.BACKSCATTERED]) > 1:        # ignores when no shapes are drawn
                logger.info("Redraw polygons")
                for shape in self.__polygonList[constants.BACKSCATTERED]:
                    if not shape.isEmpty():             # ignores the blank shape in the list
                        shape.redrawShape()
        elif plot == 2:
            logger.info("Set plot for PolygonList to depolarized")
            self.__currentList = self.__polygonList[constants.DEPOLARIZED]
            newPlot = constants.DEPOLARIZED_STR
            if len(self.__polygonList[constants.DEPOLARIZED]) > 1:
                logger.info("Redraw polygons")
                for shape in self.__polygonList[constants.DEPOLARIZED]:
                    if not shape.isEmpty():
                        shape.redrawShape()
        else:
            logger.info("Set plot for PolygongList to VFM")
            self.__currentList = self.__polygonList[constants.VFM]
            newPlot = constants.VFM_STR
            if len(self.__polygonList[constants.VFM]) > 1:
                for shape in self.__polygonList[constants.VFM]:
                    if not shape.isEmpty():
                        shape.redrawShape()
        self.__canvas._tkcanvas.delete(self.__plot)
        self.__canvas._tkcanvas.delete("line")
        self.__plot = newPlot
    
    def anchorRectangle(self, event):
        '''
        Informs the correct list's blank to plot a corner of a rectangle
        
        :param event: Tkinter passed event object
        '''
        logger.info("Anchoring rectangle")
        if self.__plot == constants.BASE_PLOT_STR:
            return
        self.__currentList[-1].anchorRectangle(event)
        
    def getCount(self):
        '''
        Returns the number of polygons in the list, excluding the blanks
        '''
        return len(self.__polygonList[0]) + len(self.__polygonList[1]) + \
               len(self.__polygonList[2]) + len(self.__polygonList[3]) - 4
               
    def getFileName(self):
        return self.__currentFile
     
    def plotPoint(self, event):
        '''
        Informs the correct list's blank to plot a point on the screen
        
        :param event: Tkinter passed event object
        '''
        if self.__plot == constants.BASE_PLOT_STR:
            logger.error("Cannot draw to base plot")
            return
        logger.info("Plotting point")
        check = self.__currentList[-1].plotPoint(event, self.__plot, PolygonList.outlineToggle)
        if check:
            self.generateTag()
            self.__currentList.append(PolygonDrawer(self.__canvas, self.__master))
            
    def rubberBand(self, event):
        '''
        Uses a blank shape to draw helper rectangles
        
        :param event: Tkinter passed event object
        '''
        if self.__plot == constants.BASE_PLOT_STR:
            return
        self.__currentList[-1].rubberBand(event)
        
    def fillRectangle(self, event):
        '''
        Informs the correct list's blank to draw a rectangle on the screen
        
        :param event: Tkinter passed event object
        '''
        if self.__plot == constants.BASE_PLOT_STR:
            logger.error("Cannot draw to base plot")
            return
        self.__currentList[-1].fillRectangle(event, self.__plot, PolygonList.outlineToggle)
        self.generateTag()
        logger.info("Creating rectangle (" + self.__currentList[-1].getTag() +")")
        self.__currentList.append(PolygonDrawer(self.__canvas, self.__master))
        
    def setHDF(self, HDFFilename):
        '''
        Set the internal filename variable
        
        :param str HDFFilename: New filename
        '''
        self.__hdf = HDFFilename
        
    def drawPolygon(self):
        '''
        Informs the correct list's blank to draw a polyogon on the screen
        '''
        if self.__plot == constants.BASE_PLOT_STR:
            return
        self.__currentList[-1].drawPolygon(self.__plot, PolygonList.outlineToggle)
        self.generateTag()
        logger.info("Creating polygon (" + self.__currentList[-1].getTag() + ")")
        self.__currentList.append(PolygonDrawer(self.__canvas, self.__master))
        
    def generateTag(self, index=-1):
        '''
        Produces a unique tag for each shape for each session
        
        :param int index: Generate new tag for given index
        '''
        string = "shape" + str(self.__count)
        self.__currentList[index].setTag(string)
        self.__count += 1
    
    def reset(self):
        '''
        Clears the screen and removes polygons from the list
        '''
        logger.info("Reseting PolygonList")
        idx = self.__polygonList.index(self.__currentList)
        self.__polygonList[idx] = [PolygonDrawer(self.__canvas, self.__master)]
        self.__currentList = self.__polygonList[idx]

        self.__count = 0
        self.__canvas._tkcanvas.delete("polygon")
        self.__canvas._tkcanvas.delete("line")
    
    def delete(self, event):
        '''
        Deletes the shape from the list
        
        :param event: Tkinter passed event object
        '''
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        if target[0] > 2:           # ignore the canvas
            logger.info("Deleting polygon")
            self.__canvas._tkcanvas.delete(target)
            polyShape = self.__findPolygonByItemHandler(target)
            self.__currentList.remove(polyShape)
            
    def outline(self):
        '''
        Toggles displaying the shapes outline. When toggled, new shapes a 
        drawn with only outlines
        '''
        PolygonList.outlineToggle = not PolygonList.outlineToggle
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if PolygonList.outlineToggle:
                color = shape.getColor()
                self.__canvas._tkcanvas.itemconfigure(poly, fill=color)
            else:
                self.__canvas._tkcanvas.itemconfigure(poly, fill="")
    
    def paint(self, event):
        '''
        Recolors the shape
        
        :param event: Tkinter passed event object 
        '''
        flag = False
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        for shape in self.__currentList:
            if shape.getItemHandler() == target[0]:
                flag = True
        if flag:
            logger.info("Recoloring polygon")
            color = askcolor()
            self.__canvas._tkcanvas.itemconfigure(target, fill=color[1], outline=color[1])
            polyShape = self.__findPolygonByItemHandler(target)
            polyShape.setColor(color[1])
        
    def hide(self):
        '''
        Hides all shapes drawn on the canvas
        '''
        logger.info("Toggling hide")
        PolygonList.hideToggle = not PolygonList.hideToggle
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if PolygonList.hideToggle:
                color = shape.getColor()
                self.__canvas._tkcanvas.itemconfigure(poly, fill=color, outline=color)
            else:
                self.__canvas._tkcanvas.itemconfigure(poly, fill="", outline="")
                
    def properties(self, event):
        '''
        Displays the properties of the selected polygon
        
        :param event: Tkinter passed event object
        '''
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        for shape in self.__currentList:
            if shape.getItemHandler() is target[0]:
                logger.info("Retrieving shape's properties")
                tkMessageBox.showinfo("properties",str(shape))
                return
        logger.warning("Shape not found")
                
    def toggleDrag(self, event):
        '''
        Wrapper method for calling polygondrawer toggledrag method
        
        :param event: Tkinter passed event object
        '''
        logger.info("Toggling drag")
        PolygonDrawer.toggleDrag(event)
        
    def findPolygon(self, event):
        '''
        Return polygon matching closest to mouse cursor
        
        :param event: Tkinter passed event object
        '''
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        for shape in self.__currentList:
            if shape.getItemHandler() == target[0]:
                logger.info("Found polygon")
                return shape
        logger.error("Polygon not found")
    
    def __findPolygonByItemHandler(self, itemHandler):
        '''
        Retrieves a shape based on its item handler
        
        :param itemHandler: Handle to polygon object
        '''
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if poly == itemHandler[0]:
                logger.info("Found shape by item handler")
                return shape
        logger.warning("Not shape found with item handler")
            
    @staticmethod
    def __plotInttoString(plot):
        if plot == 0:
            return "base_plot"
        elif plot == 1:
            return "backscattered"
        elif plot == 2:
            return "depolarized"
        else:
            return "vfm"
        
    @staticmethod
    def plotStringtoInt(plot):
        if plot.lower() == "base_plot":
            return 0
        elif plot.lower() == "backscattered":
            return 1
        elif plot.lower() == "depolarized":
            return 2
        elif plot.lower() == "vfm":
            return 3
            
    def readPlot(self, fileName="", readFromString=""):
        '''
        Load data from JSON file into polygon shapes
        
        :param str fileName: Name of JSON file to read from
        :param str readFromString: If not a filename, read JSON from string
        '''
        if readFromString != "":
            logger.info("Reading JSON from string")
            self.__polyReader.readFromStrJSON(readFromString)
        else:
            logger.info("Reading JSON from file")
            self.__polyReader.setFileName(fileName)
            self.__polyReader.readFromFileJSON()
        plot = 0
        logger.info("Parse JSON data for new polygons")
        for lst in self.__polygonList:
            self.__polyReader.packPolygonDrawer(lst, constants.PLOTS[plot], self.__canvas, self.__master)
            if PolygonList.plotStringtoInt(self.__plot) == plot:
                for shape in lst:
                    if not shape.isEmpty():
                        logger.info("Drawing polygon")
                        shape.redrawShape()
            plot += 1
        
            
    def saveToDB(self):
        '''
        Saves to database
        '''
        if len(self.__currentList) == 1:
            return False
        today = datetime.utcnow().replace(microsecond=0)
        db.commitToDB(self.__currentList, str(today), self.__hdf)
        return True
        
    def save(self, fileName=""):
        '''
        Saves shapes to JSON for current plot only
        
        :param str fileName: Filename to save JSON to
        '''
        if fileName != "": self.__currentFile = fileName
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data["hdfFile"] = self.__hdf
        shapeDict = {}
        for i in range(len(self.__polygonList)):
            self.__data[self.__plotInttoString(i)] = {}
        i = self.__polygonList.index(self.__currentList)
        for j in range(len(self.__currentList)-1):
            tag = self.__currentList[j].getTag()
            vertices = self.__currentList[j].getVertices()
            coordinates = self.__currentList[j].getCoordinates()
            color = self.__currentList[j].getColor()
            attributes = self.__polygonList[i][j].getAttributes()
            note = self.__polygonList[i][j].getNotes()
            _id = self.__polygonList[i][j].getID()
            value = {"vertices": vertices, "coordinates": coordinates, "color": color, "attributes": attributes, "notes": note, "id": _id}
            shapeDict[tag] = value
        self.__data[self.__plotInttoString(i)] = shapeDict
        logger.info("Encoding to JSON")
        db.encode(self.__currentFile, self.__data)    
        
    def saveAll(self, fileName=""):
        '''
        Saves shape to JSON from all plots
        
        :param str fileName: Filename to save JSON to
        '''
        logger.info("Saving all shapes to JSON")
        if fileName is not None: self.__currentFile = fileName
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data["hdfFile"] = self.__hdf
        for i in range(len(self.__polygonList)):
            shapeDict = {}
            for j in range(len(self.__polygonList[i])-1):
                tag = self.__polygonList[i][j].getTag()
                vertices = self.__polygonList[i][j].getVertices()
                coordinates = self.__polygonList[i][j].getCoordinates()
                color = self.__polygonList[i][j].getColor()
                attributes = self.__polygonList[i][j].getAttributes()
                note = self.__polygonList[i][j].getNotes()
                _id = self.__polygonList[i][j].getID()
                value = {"vertices": vertices, "coordinates": coordinates, "color": color, "attributes": attributes, "notes": note, "id": _id}
                shapeDict[tag] = value
            self.__data[self.__plotInttoString(i)] = shapeDict
        logger.info("Encoding to JSON")
        db.encode(self.__currentFile, self.__data)  