'''
Created on Jun 4, 2015

@author: Nathan Qian
'''

from Tkinter import Widget
from numpy import empty_like, dot, array

class PolygonDrawer(Widget):
    '''
    Displays the polygon objects onto the canvas by supplying draw methods.
    '''
    
    num = 0
    colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]

    def __init__(self, canvas):
        '''
        Constructor
        '''
        self.__vertices = []
        self.__hdf = ""
        self.__canvas = canvas
        self.__prevX = -1.0
        self.__prevY = -1.0
        self.__drag_data = {"x": 0, "y": 0, "item": None}
        self.__dragMode = False
        
        self.__canvas._tkcanvas.tag_bind("polygon", "<Button-1>", self.OnTokenButtonPress)
        self.__canvas._tkcanvas.tag_bind("polygon", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.__canvas._tkcanvas.tag_bind("polygon", "<B1-Motion>", self.OnTokenMotion)
        
    def OnTokenButtonPress(self, event):
        if self.__dragMode:
            self.__drag_data["item"] = self.__canvas._tkcanvas.find_closest(event.x, event.y)[0]
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
        
    def OnTokenButtonRelease(self, event):
        if self.__dragMode:
            self.__drag_data["item"] = None
            self.__drag_data["x"] = 0
            self.__drag_data["y"] = 0
        
    def OnTokenMotion(self, event):
        print self.__canvas._tkcanvas.gettags(self.__drag_data["item"])
        if self.__dragMode:
            dx = event.x - self.__drag_data["x"]
            dy = event.y - self.__drag_data["y"]
            self.__canvas._tkcanvas.move(self.__drag_data["item"], dx, dy)
            self.__drag_data["x"] = event.x
            self.__drag_data["y"] = event.y
                    
    def anchorRectangle(self, event):
        '''
        Establishes a corner of a rectangle as anchor for when the user drags the cursor to 
        create a rectangle. Used in "Draw Rect" button
        '''
        self.__vertices.append((event.x, event.y))
        self.__prevX = event.x
        self.__prevY = event.y
        
    def plotPoint(self, event):
        '''
        Draws a line whenever a user clicks on a point on the canvas. When the lines form a polygon,
        the polygon is drawn and any extending lines are removed. Used in "Free Draw"
        '''
        self.__vertices.append((event.x, event.y))
        if len(self.__vertices) > 1:
            self.__canvas._tkcanvas.create_line(self.__prevX, self.__prevY, event.x, event.y, fill=PolygonDrawer.colors[PolygonDrawer.num%8], width="2", tags="line")
        if len(self.__vertices) > 3:
            # TODO: check if polygon besides the first line
            a1 = tupleToNpArray(self.__vertices[0])
            a2 = tupleToNpArray(self.__vertices[1])
            b1 = tupleToNpArray(self.__vertices[-1])
            b2 = tupleToNpArray(self.__vertices[-2])
            if isIntersecting(a1, a2, b1, b2):
                x = getIntersection(a1, a2, b1, b2)
                pair = npArrayToTuple(x)
                self.__vertices[0] = pair
                self.__vertices.pop()
                self.drawPolygon()
                self.__canvas._tkcanvas.delete("line")
                self.__clear()
                return True
        self.__prevX = event.x
        self.__prevY = event.y
        
    def drag(self, event):
        print 'Widget=%s x=%s y=%s' % (event.widget, event.x, event.y)
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.__canvas._tkcanvas.create_rectangle(self.__prevX, self.__prevY, event.x, event.y)
        
    def fillRectangle(self, event):
        '''
        Draws the rectangle and stores the vertices of the rectangle internally. Used in "Draw Rect"
        '''
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
        ix = self.__vertices[0][0]
        iy = self.__vertices[0][1]
        identifier = self.generateTag()
        self.__canvas._tkcanvas.create_rectangle(ix, iy, event.x, event.y, outline="red", fill=PolygonDrawer.colors[PolygonDrawer.num%8], tags=("polygon", identifier))
        self.__clear()
        
    def setHDF(self, HDFFilename):
        self.__hdf = HDFFilename
        
    def getVertices(self):
        return self.__vertices
    
    def getHDF(self):
        return self.__hdf
    
    def __canDrawPolygon(self):
        b1 = tupleToNpArray(self.__vertices[-1])
        b2 = tupleToNpArray(self.__vertices[-2])
        for i in range(0, len(self.__vertices)-2):
            a1 = tupleToNpArray(self.__vertices[i])
            a2 = tupleToNpArray(self.__vertices[i+1])
            if isIntersecting(a1, a2, b1, b2):
                return True
        return False
            
    def drawPolygon(self):
        identifier = self.generateTag()
        self.__canvas._tkcanvas.create_polygon(self.__vertices, outline="red", fill=PolygonDrawer.colors[PolygonDrawer.num%8], width=2, tags=("polygon", identifier))
        self.__clear()
    
    def toggleDrag(self, event):
        self.__dragMode = not self.__dragMode
        print self.__dragMode
        
    def generateTag(self):
        string = "shape" + str(PolygonDrawer.num)
        PolygonDrawer.num += 1
        return string
    
    def reset(self):
        self.__canvas._tkcanvas.delete("polygon")
        self.__canvas._tkcanvas.delete("line")
        PolygonDrawer.num = 0
        
    def delete(self, event):
        target = self.__canvas._tkcanvas.find_closest(event.x, event.y)
        self.__canvas._tkcanvas.delete(target)

    
    def __clear(self):
        self.__vertices = []
        self.__drag_data["item"] = None
        self.__drag_data["x"] = 0
        self.__drag_data["y"] = 0
        
def perpendicular(a):
    '''
    Returns a numpy array that's orthogonal to the param
    '''
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def getIntersection(a1, a2, b1, b2):
    '''
    Retrieves the point of intersection of two lines given two points
    on each line
    @param a1, a2: Two points on the first line
    @param b1, b1: Two points on the second line
    '''
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    return (num /denom.astype(float))*db + b1

def isIntersecting(a1, a2, b1, b2):
    '''
    Determines if two line segments are intersecting by checking if the point of intersection
    exists on the line segments
    @param a1, a2: The endpoints of the first line segment
    @param b1, b2: The endpoints of the second line segment
    '''
    point = getIntersection(a1, a2, b1, b2)
    if ((point[0] < max(min(a1[0], a2[0]), min(b1[0], b2[0]))) or
        (point[0] > min(max(a1[0], a2[0]), max(b1[0], b2[0])))):
        return False
    else:
        return True
    
def tupleToNpArray(pair):
    '''
    Converts a tuple to a numpy array
    '''
    return array([pair[0], pair[1]])
    
def npArrayToTuple(array):
    x = array[0]
    y = array[1]
    return (x, y)