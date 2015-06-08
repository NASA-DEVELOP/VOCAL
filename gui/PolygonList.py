'''
Created on Jun 8, 2015

@author: nqian
'''
from gui.PolygonDrawing import PolygonDrawing

class PolygonList(object):
    '''
    classdocs
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
    
    def addPolygon(self, poly):
        self.__polygonList.append(poly)
        
    def addVertex(self, event):
        print "Adding vertex"
        check = self.__polygonList[-1].addVertex(event)
        if check:
            self.__polygonList.append(PolygonDrawing(self.__canvas))
    
    def anchorRectangle(self, event):
        print "Anchor's aweigh"
        self.__polygonList[-1].anchorRectangle(event)
    
    def plotPoint(self, event):
        print "Plotting point"
        check = self.__polygonList[-1].plotPoint(event)
        if check:
            self.__polygonList.append(PolygonDrawing(self.__canvas))
    
    def drag(self, event):
        self.__polygonList[-1].drag(event)
    
    def fillRectangle(self, event):
        print "Filling rectangle"
        self.__polygonList[-1].fillRectangle(event)
        self.__polygonList.append(PolygonDrawing(self.__canvas))
        
    def toggleDrag(self, event):
        self.__polygonList[-1].toggleDrag(event)
        
    def reset(self):
        self.__canvas._tkcanvas.delete("polygon")
        self.__canvas._tkcanvas.delete("line")
        self.__polygonList = [PolygonDrawing(self.__canvas)]