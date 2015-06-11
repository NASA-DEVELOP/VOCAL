'''
Created on Jun 11, 2015

@author: nqian
'''
# import antigravity
from gui.Polygon import PolygonDrawer
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
        self.__polygonList = [PolygonDrawer(canvas)]
        self.__polyWritier = PolygonWriter()
        self.__hdf = ''
        self.__count = 0
    
    def anchorRectangle(self, event):
        self.__polygonList[-1].anchorRectangle(event)
        
    def plotPoint(self, event):
        check = self.__polygonList[-1].plotPoint(event)
        if check:
            self.__polygonList.append(PolygonDrawer(self.__canvas))
            
    def rubberBand(self, event):
        self.__polygonList.rubberBand(event)
        
    def fillRectangle(self, event):
        self.__polygonList[-1].fillRectangle(event)
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def drawPolygon(self):
        self.__polygonList[-1].drawPolygon()
        self.__polygonList.append(PolygonDrawer(self.__canvas))
        
    def generateTag(self, index=-1):
        string = "shape" + str(self.__count)
        self.__polygonList[index].setTag(string)
        self.__count += 1
    
    def reset(self):
        self.__polygonList = [PolygonDrawer(self.__canvas)]
        self.__count = 0
    
    #TODO: figure out deleting
    def delete(self, event, PolygonDrawer):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        if target[0] > 2:
            self.__canvas._tkcanvas.delete(target)
            
    def outline(self):
        PolygonList.outlineToggle = not PolygonList.outlineToggle
        for shape in self.__polygonList:
            if PolygonList.outlineToggle:
                pass
            else:
                pass
    
    def paint(self, event):
        pass
    
    def pack(self):
        pass