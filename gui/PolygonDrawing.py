'''
Created on Jun 4, 2015

@author: Nathan Qian
'''

from Tkinter import Widget
from numpy import empty_like, dot, array

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
        self.__prevX = -1.0
        self.__prevY = -1.0
        
    def addVertex(self, event):
        self.__vertices.append((event.x, event.y))
        print("Added vertex at (" + str(event.x) + "," + str(event.y) + ")")
        if self.canDrawPolygon():
            self.drawPolygon()
            
    def anchorRectangle(self, event):
        self.__vertices.append((event.x, event.y))
        
    def plotPoint(self, event):
        self.__vertices.append((event.x, event.y))
        if len(self.__vertices) > 1:
            self.__canvas.create_line(self.__prevX, self.__prevY, event.x, event.y, fill="red", width="2")
#             if self.isPolygon():
#                 self.drawPolygon()
#                 return
        if len(self.__vertices) > 3:
            a1 = toPoint(self.__vertices[0])
            a2 = toPoint(self.__vertices[1])
            b1 = toPoint(self.__vertices[-1])
            b2 = toPoint(self.__vertices[-2])
            if isIntersecting(a1, a2, b1, b2):
                self.drawPolygon()
        self.__prevX = event.x
        self.__prevY = event.y
        
    def drag(self, event):
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
        
    def isPolygon(self):
        if len(self.__vertices) < 3:
            return False
        else:
            a1 = toPoint(self.__vertices[0])
            a2 = toPoint(self.__vertices[1])
            b1 = toPoint(self.__vertices[-1])
            b2 = toPoint(self.__vertices[-2])
            if getIntersection(a1, a2, b1, b2):
                return getIntersection(a1, a2, b1, b2)
            else:
                return False
           
    
    def drawPolygon(self):
        self.__canvas.create_polygon(self.__vertices, outline="red", fill="red", width=2)
        
    def reset(self):
        self.__vertices = []
        
def perpendicular(a):
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def getIntersection(a1, a2, b1, b2):
    '''
    Determines if two line segments are intersecting
    @param a1, a2: The endpoints of the first line segment
    @param b1, b1: The endpoints of the second line segment
    '''
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    return (num /denom.astype(float))*db + b1

def isIntersecting(a1, a2, b1, b2):
    point = getIntersection(a1, a2, b1, b2)
    if ((point[0] < max(min(a1[0], a2[0]), min(b1[0], b2[0]))) or
        (point[0] > min(max(a1[0], a2[0]), max(b1[0], b2[0])))):
        return False
    else:
        return True
    
def toPoint(pair):
        return array([pair[0], pair[1]])