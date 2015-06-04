'''
Created on Jun 4, 2015

@author: Nathan Qian
'''

from Tkinter import Widget

class PolygonDrawing(Widget):
    '''
    classdocs
    '''

    def __init__(self, canvas):
        '''
        Constructor
        '''
        self.__vertices = []
        self.__hdf = ""
        self.__canvas = canvas
        
    def addVertex(self, event):
        self.__vertices.append((event.x, event.y))
        print("Added vertex at (" + str(event.x) + "," + str(event.y) + ")")
        if self.canDrawPolygon():
            self.drawPolygon()
            
    def anchorRectangle(self, event):
        self.__vertices.append((event.x, event.y))
        
    def drawRectangle(self, event):
        print 'Widget=%s x=%s y=%s' % (event.widget, event.x, event.y)
        
    def fillRectangle(self, event):
        ix = self.__vertices[0][0]
        iy = self.__vertices[0][1]
        self.__canvas.create_rectangle(ix, iy, event.x, event.y, outline="red", fill="red")
        self.__vertices.append((event.x, iy))
        self.__vertices.append((event.x, event.y))
        self.__vertices.append((ix, event.y))
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def getVertices(self):
        return self.__vertices
    
    def getHDF(self):
        return self.__hdf
    
    def canDrawPolygon(self):
        if len(self.__vertices) >= 3:
            return True
        else:
            return False
    
    def drawPolygon(self):
        self.__canvas.create_polygon(self.__vertices, outline="red", fill="red", width=2)
        
    def reset(self):
        self.__vertices = []