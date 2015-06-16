'''
Created on Jun 11, 2015

@author: nqian
'''
# import antigravity
from tkColorChooser import askcolor

from datetime import datetime

from gui import Constants
from gui.Polygon import PolygonDrawer
from gui.PolygonReader import PolygonReader
from gui.PolygonWriter import PolygonWriter


class PolygonList(object):
    '''
    classdocs
    '''

    outlineToggle = True
    hideToggle = True

    def __init__(self, canvas):
        '''
        Constructor
        '''
        self.__canvas = canvas
        self.__polygonList = [[PolygonDrawer(canvas)],      # base plot list
                              [PolygonDrawer(canvas)],      # backscattered list
                              [PolygonDrawer(canvas)],      # depolarized list
                              [PolygonDrawer(canvas)]]      # vfm list
        self.__currentList = None
        self.__polyWritier = PolygonWriter()
        self.__polyReader = PolygonReader()
        self.__hdf = ''
        self.__plot = Constants.BASE_PLOT_STR
        self.__count = 0
        self.__data = {}
        self.__drag_data = {"x": 0, "y": 0, "item": None}
        
        self.__canvas._tkcanvas.tag_bind("polygon", "<Button-1>", self.onTokenButtonPress)
        self.__canvas._tkcanvas.tag_bind("polygon", "<ButtonRelease-1>", self.onTokenButtonRelease)
        self.__canvas._tkcanvas.tag_bind("polygon", "<B1-Motion>", self.onTokenMotion)
        
    def onTokenButtonPress(self, event):
        if PolygonDrawer.dragToggle:
            self.__drag_data["item"] = self.__canvas._tkcanvas.find_closest(event.x, event.y)[0]
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
        
    def onTokenButtonRelease(self, event):
        if PolygonDrawer.dragToggle:
            self.__drag_data["item"] = None
            self.__drag_data["x"] = 0
            self.__drag_data["y"] = 0
        
    def onTokenMotion(self, event):
#         print self.__canvas._tkcanvas.gettags(self.__drag_data["item"])
        if PolygonDrawer.dragToggle:
            dx = event.x - self.__drag_data["x"]
            dy = event.y - self.__drag_data["y"]
            self.__canvas._tkcanvas.move(self.__drag_data["item"], dx, dy)
            for shape in self.__currentList:
                if shape.getItemHandler() is self.__drag_data["item"]:
                    shape.move(dx, dy)
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
    
    def setPlot(self, plot):
        newPlot = ""
#         oldData = self.readPlot()
        if plot == 0:
            self.__currentList = self.__polygonList[Constants.BASE_PLOT]
            newPlot = Constants.BASE_PLOT_STR
        elif plot == 1:
            self.__currentList = self.__polygonList[Constants.BACKSCATTERED]
            newPlot = Constants.BACKSCATTERED_STR
            if len(self.__polygonList[Constants.BACKSCATTERED]) > 1:
                for shape in self.__polygonList[Constants.BACKSCATTERED]:
                    if not shape.isEmpty():
                        shape.redrawShape()
        elif plot == 2:
            self.__currentList = self.__polygonList[Constants.DEPOLARIZED]
            newPlot = Constants.DEPOLARIZED_STR
            if len(self.__polygonList[Constants.DEPOLARIZED]) > 1:
                for shape in self.__polygonList[Constants.DEPOLARIZED]:
                    if not shape.isEmpty():
                        shape.redrawShape()
        else:
            self.__currentList = self.__polygonList[Constants.VFM]
            newPlot = Constants.VFM_STR
            if len(self.__polygonList[Constants.VFM]) > 1:
                for shape in self.__polygonList[Constants.VFM]:
                    if not shape.isEmpty():
                        shape.redrawShape()
        self.__canvas._tkcanvas.delete(self.__plot)
        self.__canvas._tkcanvas.delete("line")
        self.__plot = newPlot
    
    def anchorRectangle(self, event):
        self.__currentList[-1].anchorRectangle(event)
        
    def plotPoint(self, event):
        check = self.__currentList[-1].plotPoint(event, self.__plot)
        if check:
            self.generateTag()
            self.__currentList.append(PolygonDrawer(self.__canvas))
            
    def rubberBand(self, event):
        self.__currentList[-1].rubberBand(event)
        
    def fillRectangle(self, event):
        self.__currentList[-1].fillRectangle(event, self.__plot)
        self.generateTag()
        self.__currentList.append(PolygonDrawer(self.__canvas))
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def drawPolygon(self):
        self.__currentList[-1].drawPolygon(self.__plot)
        self.generateTag()
        self.__currentList.append(PolygonDrawer(self.__canvas))
        
    def generateTag(self, index=-1):
        string = "shape" + str(self.__count)
        self.__currentList[index].setTag(string)
        self.__count += 1
    
    def reset(self):
        self.__currentList = [PolygonDrawer(self.__canvas)]
        self.__count = 0
        self.__canvas._tkcanvas.delete("polygon")
        self.__canvas._tkcanvas.delete("line")
    
    def delete(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        if target[0] > 2:
            self.__canvas._tkcanvas.delete(target)
        polyShape = self.__findPolygonByItemHandler(target)
        self.__currentList.remove(polyShape)
            
    def outline(self):
        PolygonList.outlineToggle = not PolygonList.outlineToggle
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if PolygonList.outlineToggle:
                color = shape.getColor()
                self.__canvas._tkcanvas.itemconfigure(poly, fill=color)
            else:
                self.__canvas._tkcanvas.itemconfigure(poly, fill="")
    
    def paint(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        color = askcolor()
        self.__canvas._tkcanvas.itemconfigure(target, fill=color[1], outline=color[1])
        polyShape = self.__findPolygonByItemHandler(target)
        polyShape.setColor(color[1])
        
    def hide(self):
        PolygonList.hideToggle = not PolygonList.hideToggle
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if PolygonList.hideToggle:
                color = shape.getColor()
                self.__canvas._tkcanvas.itemconfigure(poly, fill=color, outline=color)
            else:
                self.__canvas._tkcanvas.itemconfigure(poly, fill="", outline="")
                
    def properties(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        for shape in self.__currentList:
            if shape.getItemHandler() is target[0]:
                print shape
                return
        print "Polygon shape not found"
                
    def toggleDrag(self, event):
        PolygonDrawer.toggleDrag(event)
        
    def __findPolygonByItemHandler(self, itemHandler):
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if poly == itemHandler[0]:
                return shape
            
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
            
    def readPlot(self, fileName="C:\\Users\\nqian\\Documents\\Carol.json"):
        self.__polyReader.setFileName(fileName)
        self.__polyReader.readJSON()
        plot = 0
        for lst in self.__polygonList:
            self.__polyReader.packPolygonDrawer(lst, Constants.PLOTS[plot], self.__canvas)
            if PolygonList.plotStringtoInt(self.__plot) == plot:
                for shape in lst:
                    if not shape.isEmpty():
                        shape.redrawShape()
            plot += 1
        
    def save(self, fileName="objs/polygons.json"):
        self.__polyWritier.setJsonFile(fileName)
        today = datetime.utcnow()
        year = today.year
        month = today.month
        day = today.day
        hour = today.hour
        minute = today.minute
        second = today.second
        self.__data['time'] = str(year) + "-" + str(month) + "-" + str(day) + "T" + str(hour) + ":" + str(minute) + ":" + str(second) + "Z"
        self.__data["hdfFile"] = self.__hdf
        for i in range(len(self.__polygonList)):
            shapeDict = {}
            for j in range(len(self.__polygonList[i])-1):
                tag = self.__polygonList[i][j].getTag()
                vertices = self.__polygonList[i][j].getVertices()
                color = self.__polygonList[i][j].getColor()
                value = {"vertices": vertices, "color": color}
                shapeDict[tag] = value
            self.__data[self.__plotInttoString(i)] = shapeDict
        self.__polyWritier.encode(self.__data)
                
if __name__=="__main__":
    print PolygonList.plotStringtoInt(Constants.PLOTS[0])
    print PolygonList.plotStringtoInt(Constants.PLOTS[1])
    print PolygonList.plotStringtoInt(Constants.PLOTS[2])
    print PolygonList.plotStringtoInt(Constants.PLOTS[3])