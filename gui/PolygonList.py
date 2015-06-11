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
        self.__polygonList = [PolygonDrawer(canvas)]
        self.__polyWritier = PolygonWriter()
        self.__hdf = ''
        self.__count = 0
        self.__data = {}
    
    def anchorRectangle(self, event):
        self.__polygonList[-1].anchorRectangle(event)
        
    def plotPoint(self, event):
        check = self.__polygonList[-1].plotPoint(event)
        if check:
            self.generateTag()
            self.__polygonList.append(PolygonDrawer(self.__canvas))
            
    def rubberBand(self, event):
        self.__polygonList[-1].rubberBand(event)
        
    def fillRectangle(self, event):
        self.__polygonList[-1].fillRectangle(event)
        self.generateTag()
        self.__polygonList.append(PolygonDrawer(self.__canvas))
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def drawPolygon(self):
        self.__polygonList[-1].drawPolygon()
        self.generateTag()
        self.__polygonList.append(PolygonDrawer(self.__canvas))
        
    def generateTag(self, index=-1):
        string = "shape" + str(self.__count)
        self.__polygonList[index].setTag(string)
        self.__count += 1
    
    def reset(self):
        self.__polygonList = [PolygonDrawer(self.__canvas)]
        self.__count = 0
    
    #TODO: figure out deleting
    def delete(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        if target[0] > 2:
            self.__canvas._tkcanvas.delete(target)
        polyShape = self.__findPolygonByItemHandler(target)
        self.__polygonList.remove(polyShape)
            
    def outline(self):
        PolygonList.outlineToggle = not PolygonList.outlineToggle
        for shape in self.__polygonList:
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
        for shape in self.__polygonList:
            poly = shape.getItemHandler()
            if PolygonList.hideToggle:
                color = shape.getColor()
                self.__canvas._tkcanvas.itemconfigure(poly, fill=color, outline=color)
            else:
                self.__canvas._tkcanvas.itemconfigure(poly, fill="", outline="")
                
    def toggleDrag(self, event):
        PolygonDrawer.toggleDrag(event)
        
    def __findPolygonByItemHandler(self, itemHandler):
        for shape in self.__polygonList:
            poly = shape.getItemHandler()
            if poly == itemHandler[0]:
                return shape
    
    def save(self):
        self.__data["hdfFile"] = self.__hdf
        for shape in self.__polygonList:
            tag = shape.getTag()
            vertices = shape.getVertices()
            color = shape.getColor()
            value = {"vertices": vertices, "color": color}
            self.__data[tag] = value
            self.__polyWritier.encode(self.__data)