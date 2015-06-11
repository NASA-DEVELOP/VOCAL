'''
Created on Jun 11, 2015

@author: nqian
'''
# import antigravity
from gui.Polygon import PolygonDrawer
from gui.PolygonWriter import PolygonWriter
from tkColorChooser import askcolor


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
        self.__polygonList = [[PolygonDrawer(canvas)],
                              [PolygonDrawer(canvas)],
                              [PolygonDrawer(canvas)],
                              [PolygonDrawer(canvas)]]
        self.__currentList = None
        self.__polyWritier = PolygonWriter()
        self.__hdf = ''
        self.__plot = -1
        self.__count = 0
        self.__data = {}
    
    def setPlot(self, plot):
        self.__plot = plot
        if self.__plot == 0:
            self.__currentList = self.__polygonList[0]
        elif self.__plot == 1:
            self.__currentList = self.__polygonList[1]
        elif self.__plot == 2:
            self.__currentList = self.__polygonList[2]
        else:
            self.__currentList = self.__polygonList[3]
    
    def anchorRectangle(self, event):
        self.__currentList[-1].anchorRectangle(event)
        
    def plotPoint(self, event):
        check = self.__currentList[-1].plotPoint(event)
        if check:
            self.generateTag()
            self.__currentList.append(PolygonDrawer(self.__canvas))
            
    def rubberBand(self, event):
        self.__currentList[-1].rubberBand(event)
        
    def fillRectangle(self, event):
        self.__currentList[-1].fillRectangle(event)
        self.generateTag()
        self.__currentList.append(PolygonDrawer(self.__canvas))
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def drawPolygon(self):
        self.__currentList[-1].drawPolygon()
        self.generateTag()
        self.__currentList.append(PolygonDrawer(self.__canvas))
        
    def generateTag(self, index=-1):
        string = "shape" + str(self.__count)
        self.__currentList[index].setTag(string)
        self.__count += 1
    
    def reset(self):
        self.__currentList = [PolygonDrawer(self.__canvas)]
        self.__count = 0
    
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
                
    def toggleDrag(self, event):
        PolygonDrawer.toggleDrag(event)
        
    def __findPolygonByItemHandler(self, itemHandler):
        for shape in self.__currentList:
            poly = shape.getItemHandler()
            if poly == itemHandler[0]:
                return shape
            
    def __plotInttoString(self, plot):
        if plot == 0:
            return "Base_Plot"
        elif plot == 1:
            return "Backscattered"
        elif plot == 2:
            return "Depolarized"
        else:
            return "VFM"
    
    def save(self):
        self.__data["hdfFile"] = self.__hdf
        for i in range(len(self.__polygonList)):
            plotDict = {}
            for j in range(len(self.__polygonList[i])-1):
                tag = self.__currentList[j].getTag()
                vertices = self.__currentList[j].getVertices()
                color = self.__currentList[j].getColor()
                value = {"vertices": vertices, "color": color}
                plotDict = {tag: value}
            self.__data[self.__plotInttoString(i)] = plotDict
        self.__polyWritier.encode(self.__data)    