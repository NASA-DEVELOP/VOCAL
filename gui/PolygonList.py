'''
Created on Jun 8, 2015

@author: nqian
'''
from gui.PolygonDrawing import PolygonDrawing

class PolygonList(object):
    '''
    Handles multiple instances of PolygonDrawing to support multiple polygons on a screen
    '''

    def __init__(self, canvas):
        '''
        Constructor
        '''
        self.__polygonList = [PolygonDrawing(canvas)]
        self.__selectedPolygon = None
        self.__canvas = canvas
        
    def getNewestPolygon(self):
        return self.__polygonList[-1]
    
    def addVertex(self, event):
        check = self.__polygonList[-1].addVertex(event)
        if check:
            self.__polygonList.append(PolygonDrawing(self.__canvas))
    
    def anchorRectangle(self, event):
        self.__polygonList[-1].anchorRectangle(event)
    
    def plotPoint(self, event):
        check = self.__polygonList[-1].plotPoint(event)
        if check:
            self.__polygonList.append(PolygonDrawing(self.__canvas))
    
    def drag(self, event):
        self.__polygonList[-1].drag(event)
    
    def fillRectangle(self, event):
        self.__polygonList[-1].fillRectangle(event)
        self.__polygonList.append(PolygonDrawing(self.__canvas))
        
    def toggleDrag(self, event):
        self.__polygonList[-1].toggleDrag(event)
        
    def reset(self):
        self.__canvas._tkcanvas.delete("polygon")
        self.__canvas._tkcanvas.delete("line")
        PolygonDrawing.num = 0
        self.__polygonList = [PolygonDrawing(self.__canvas)]
        
    def delete(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        self.__canvas._tkcanvas.delete(target)
