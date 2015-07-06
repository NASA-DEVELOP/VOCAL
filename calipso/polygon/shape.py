######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

from constants import *
from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle

# noinspection PyProtectedMember
class Shape(object):
    """
    Displays the polygon objects onto the canvas by supplying draw methods
    and maintaining internal information on the shape. Draws to matplotlib
    backend
    """

    drag_toggle= False
    color_counter = 0
    COLORS = ['snow', 'light cyan']

    def __init__(self, canvas, tag='', color=''):
        self.__canvas = canvas
        self.__vertices = []
        self.__coordinates = []
        self.__tag = tag
        self.__color = color
        self.__item_handler = 0
        self.__plot = BASE_PLOT
        self.__attributes = []
        self.__note = ''
        self.__id = None
        self.lastrect = None
        self.__prev_x = 1.0
        self.__prev_y = 1.0

    def anchor_rectangle(self, event):
        """
        Establishes a corner of a rectangle as an anchor for when the user drags the cursor to create
        a rectangle. Used in 'Draw Rect' button

        :param event: A matplotlib backend event object
        """
        self.__coordinates.append((event.xdata, event.ydata))
        self.__vertices.append((event.x, event.y))
        self.__prev_x = event.x
        self.__prev_y = event.y

    def plot_point(self, event):
        pass

    def rubberband(self, event):
        """
        Draws a temporary helper rectangle that outlines the final shape of the rectangle for
        the user. This draws to **screen** coordiantes, so backend is not needed here.

        :param event: A ``matplotlib.backend_bases.MouseEvent`` forwarded object.
        """
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.__canvas._tkcanvas.create_rectangle(self.__prev_x,
                                                                 abs(HEIGHT - self.__prev_y - 35),
                                                                 event.x,
                                                                 abs(HEIGHT - event.y - 35))

    def fill_rectangle(self, event, fig, plot=BASE_PLOT_STR, fill=False):
        """
        Draws the rectangle and stroes the cooridnates of the rectangle internally. Used
        in 'Draw Rect' button. Forwards argument parameters to ``draw``

        :param fig: Figure to draw canvas to
        :param plot: ``constants`` ploytype to forward to draw
        :param bool fill: Whether to fill or no fill the shape
        """
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
        self.__coordinates.append((event.xdata, event.ydata))
        print self.__coordinates
        cords = [[732839.154474, 1],
                 [732839.154474, 2],
                 [732839.154574, 3],
                 [732839.154474, 1]]
        poly = Polygon(self.__coordinates)
        fig.add_patch(poly)

    def add_attribute(self, tag):
        pass

    def remove_attribute(self, tag):
        pass

    def set_attribute(self, attributes):
        pass

    def set_tag(self, tag):
        pass

    def set_color(self, color):
        pass

    def set_vertices(self, vertex_list):
        pass

    def set_plot(self, plot):
        pass

    def set_coordinates(self, coordinates):
        pass

    def set_vertex(self, index, point):
        pass

    def set_id(self, _id):
        pass

    def set_notes(self, note):
        pass

    def get_coordinates(self):
        pass

    def get_notes(self):
        pass

    def get_attributes(self):
        pass

    def get_plot(self):
        pass

    def get_color(self):
        pass

    def get_id(self):
        pass

    def get_tag(self):
        pass

    def get_itemhandler(self):
        pass

    def is_attribute(self, tag):
        pass

    def move(self, dx, dy, dmx, dmy):
        pass

    def __can_draw(self):
        pass

    def draw(self, fig, plot=BASE_PLOT_STR, fill=False):
        pass

    def redraw(self):
        pass

    def is_empty(self):
        pass

    def __str__(self):
        pass

    @staticmethod
    def toggle_drag(event):
        pass