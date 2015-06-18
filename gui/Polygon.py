'''
Created on Jun 4, 2015

@author: Nathan Qian
'''

# import antigravity
from numpy import empty_like, dot, array
from gui import Constants

class PolygonDrawer(object):
    '''
    Displays the polygon objects onto the canvas by supplying draw methods.
    '''
    
    dragToggle = False
    colorCounter = 0
    COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
          'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
          'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
          'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
          'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
          'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
          'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
          'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
          'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
          'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
          'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
          'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red',
          'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
          'thistle', 'snow2', 'snow3',
          'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
          'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
          'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
          'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
          'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
          'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
          'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
          'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
          'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
          'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
          'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
          'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
          'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
          'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
          'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
          'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
          'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
          'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
          'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
          'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
          'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
          'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
          'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
          'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
          'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
          'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
          'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
          'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
          'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
          'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
          'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
          'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
          'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
          'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
          'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
          'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
          'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
          'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
          'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
          'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
          'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
          'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
          'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
          'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
          'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
          'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
          'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
          'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
          'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
          'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
          'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
          'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
          'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
          'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
          'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
          'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
    
    

    def __init__(self, canvas, tag="", color=""):
        '''
        Constructor
        '''
        self.__vertices = []
        self.__coordinates = []
        self.__canvas = canvas
        self.__prevX = -1.0
        self.__prevY = -1.0
        self.__tag = tag
        self.__color = color
        self.__itemHandler = 0
        self.__plot = ""
        self.__attributes = []
                    
    def anchorRectangle(self, event):
        '''
        Establishes a corner of a rectangle as anchor for when the user drags the cursor to 
        create a rectangle. Used in "Draw Rect" button
        '''
        self.__vertices.append((event.x, event.y))
        self.__prevX = event.x
        self.__prevY = event.y
        
    def plotPoint(self, event, plot=Constants.BASE_PLOT_STR, fill=False):
        self.__vertices.append((event.x, event.y))
        if len(self.__vertices) > 1:
            self.__canvas._tkcanvas.create_line(self.__prevX, self.__prevY, event.x, event.y, fill=PolygonDrawer.COLORS[PolygonDrawer.colorCounter%479], width="2", tags="line")
        if len(self.__vertices) > 3:
            index = self.__canDrawPolygon()
            if index > -1:
                a1 = tupleToNpArray(self.__vertices[index])
                a2 = tupleToNpArray(self.__vertices[index+1])
                b1 = tupleToNpArray(self.__vertices[-1])
                b2 = tupleToNpArray(self.__vertices[-2])
                x = getIntersection(a1, a2, b1, b2)
                pair = npArrayToTuple(x)
                self.__vertices[index] = pair
                del self.__vertices[:index]
                self.__vertices.pop()
                self.drawPolygon(plot, fill)
                self.__plot = plot
                self.__canvas._tkcanvas.delete("line")
                PolygonDrawer.colorCounter += 16
                return True
        self.__prevX = event.x
        self.__prevY = event.y
                
    def rubberBand(self, event):
#         print 'Widget=%s x=%s y=%s' % (event.widget, event.x, event.y)
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.__canvas._tkcanvas.create_rectangle(self.__prevX, self.__prevY, event.x, event.y)
        
    def fillRectangle(self, event, plot=Constants.BASE_PLOT_STR, fill=False):
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
        color = PolygonDrawer.COLORS[PolygonDrawer.colorCounter%479]
        if fill is False:
            fillColor = ""
        else:
            fillColor = color
        self.__itemHandler = self.__canvas._tkcanvas.create_rectangle(ix, iy, event.x, event.y, outline=color, fill=fillColor, tags=("polygon", self.__tag, plot))
        self.__color = color
        self.__vertices.append((event.x, iy))
        self.__vertices.append((event.x, event.y))
        self.__vertices.append((ix, event.y))
        self.__plot = plot
        PolygonDrawer.colorCounter += 16
        
    def addAttribute(self, tag):
        for item in self.__attributes:
            if item == tag:
                raise Exception()
        self.__attributes.append(tag)
        
    def setAttributes(self, attributes):
        self.__attributes = attributes

    def setTag(self, tag):
        self.__tag = tag;
        
    def setColor(self, color):
        self.__color = color
        
    def setVertices(self, vertexList):
        self.__vertices = vertexList
        
    def setPlot(self, plot):
        self.__plot = plot
        
    def setCoordinates(self, coordinates):
        self.__coordinates = coordinates
        
    def getCoordinates(self):
        return self.__coordinates
        
    def getAttributes(self):
        return self.__attributes
        
    def getPlot(self):
        return self.__plot 
    
    def getVertices(self):
        return self.__vertices
    
    def getColor(self):
        return self.__color

    def getTag(self):
        return self.__tag
    
    def getItemHandler(self):
        return self.__itemHandler
    
    def move(self, dx, dy):
        for i in range(len(self.__vertices)):
            newPoint = (self.__vertices[i][0] + dx, self.__vertices[i][1] + dy)
            self.__vertices[i] = newPoint
    
    def __canDrawPolygon(self):
        b1 = tupleToNpArray(self.__vertices[-1])
        b2 = tupleToNpArray(self.__vertices[-2])
        for i in range(len(self.__vertices)-3):
            a1 = tupleToNpArray(self.__vertices[i])
            a2 = tupleToNpArray(self.__vertices[i+1])
            if isIntersecting(a1, a2, b1, b2):
                return i
        return -1
            
    def drawPolygon(self, plot=Constants.BASE_PLOT_STR, fill=False):
        color = PolygonDrawer.COLORS[PolygonDrawer.colorCounter%479]
        if fill is False:
            fillColor = ""
        else:
            fillColor = color
        self.__itemHandler = self.__canvas._tkcanvas.create_polygon(self.__vertices, outline=color, fill=fillColor, width=2, tags=("polygon", self.__tag, plot))
        self.__color = color
        self.__plot = plot
        PolygonDrawer.colorCounter += 16
        
    def redrawShape(self):
        self.__itemHandler = self.__canvas._tkcanvas.create_polygon(self.__vertices, outline=self.__color, fill=self.__color, width=2, tags=("polygon", self.__tag, self.__plot))
        
    def drawFromJSON(self, plot, color, vertices):
        self.__itemHandler = self.__canvas._tkcanvas.create_polygon(vertices, outline=color, fill=color, width=2, tags=("polygon", plot))
        self.__color = color
        
    def isEmpty(self):
        if len(self.__vertices) == 0:
            return True
        else:
            return False
        
    def __str__(self):
        string = "Vertices:\n"
        for point in self.__vertices:
            string += "\t(" + str(point[0]) + "," + str(point[1]) + ")\n"
        string += "Attributes:\n"
        for item in self.__attributes:
            string += "\t" + item + "\n"
        return string
    
    @staticmethod
    def toggleDrag(event):
        PolygonDrawer.dragToggle = not PolygonDrawer.dragToggle
                            
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