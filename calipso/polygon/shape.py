######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

import random

from matplotlib.patches import Polygon

from constants import *
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from log import logger
from tools.linearalgebra import tuple_to_nparray, is_intersecting, \
    get_intersection, nparray_to_tuple


# noinspection PyProtectedMember
class Shape(object):
    """
    Displays the polygon objects onto the canvas by supplying draw methods
    and maintaining internal information on the shape. Draws to matplotlib
    backend
    """

    drag_toggle = False

    def __init__(self, canvas, tag='', color=''):
        self.__canvas = canvas
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
        Establishes a corner of a rectangle as an anchor for when the user drags the cursor to
        create a rectangle. Used in 'Draw Rect' button

        :param event: A matplotlib backend event object
        """
        self.__coordinates.append((event.xdata, event.ydata))
        self.__prev_x = event.x
        self.__prev_y = event.y

    def plot_point(self, event, fig):
        self.__coordinates.append((event.xdata, event.ydata))
        if len(self.__coordinates) > 1:
            logger.debug("Drawing line from plot")
            line = mlines.Line2D((self.__prev_x, self.__prev_y), (event.xdata, event.ydata))
            fig.add_patch(line)
        if len(self.__coordinates) > 3:
            index = self.__can_draw()
            if index > -1:
                logger.debug("Creating polygon from points")
                a1 = tuple_to_nparray(self.__coordinates[index])
                a2 = tuple_to_nparray(self.__coordinates[index+1])
                b1 = tuple_to_nparray(self.__coordinates[-1])
                b2 = tuple_to_nparray(self.__coordinates[-2])
                x = get_intersection(a1, a2, b1, b2)
                pair = nparray_to_tuple(x)
                self.__coordinates[index] = pair
                
                del self.__coordinates[:index]
                self.__coordinates.pop()
                self.__item_handler = Polygon(self.__coordinates)
                fig.add_patch(self.__item_handler)
                return True
        self.__prev_x = event.xdata
        self.__prev_y = event.ydata

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

    def fill_rectangle(self, event, fig, fill=False):
        """
        Draws the rectangle and stores the coordinates of the rectangle internally. Used
        in 'Draw Rect' button. Forwards argument parameters to ``draw``

        :param fig: Figure to draw canvas to
        :param bool fill: Whether to fill or no fill the shape
        """
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.__canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect

        logger.debug('Generating rectangular points')
        beg = self.__coordinates[0]
        self.__coordinates.append((event.xdata, beg[1]))
        self.__coordinates.append((event.xdata, event.ydata))
        self.__coordinates.append((beg[0], event.ydata))

        # Generate random color in a super cool way brah
        r = lambda: random.randint(0, 255)
        clr = '#%02X%02X%02X' % (r(), r(), r())

        self.__item_handler = \
            Polygon(self.__coordinates, facecolor=clr, fill=fill)
        fig.add_patch(self.__item_handler)

    def add_attribute(self, tag):
        self.__attributes.append(tag)

    def remove_attribute(self, tag):
        self.__attributes.remove(tag)

    def set_attribute(self, attributes):
        self.__attributes = attributes

    def set_tag(self, tag):
        self.__tag = tag

    def set_color(self, color):
        self.__color = color

    def set_vertices(self, vertex_list):
        pass

    def set_plot(self, plot):
        self.__plot = plot

    def set_coordinates(self, coordinates):
        self.__coordinates = coordinates

    def set_vertex(self, index, point):
        pass

    def set_id(self, _id):
        self.__id = id

    def set_notes(self, note):
        self.__note = note

    def get_coordinates(self):
        return self.__coordinates

    def get_notes(self):
        return self.__note

    def get_attributes(self):
        return self.__attributes

    def get_plot(self):
        return self.__plot

    def get_color(self):
        return self.__color

    def get_id(self):
        return self.__id

    def get_tag(self):
        return self.__tag

    def get_itemhandler(self):
        return self.__item_handler

    def is_attribute(self, tag):
        for item in self.__attributes:
            if tag == item:
                logger.info('Found attribute')
                return True
        return False

    def move(self, dx, dy, dmx, dmy):
        pass

    def __can_draw(self):
        b1 = tuple_to_nparray(self.__coordinates[-1])
        b2 = tuple_to_nparray(self.__coordinates[-2])
        for i in range(len(self.__coordinates)-3):
            a1 = tuple_to_nparray(self.__coordinates[i])
            a2 = tuple_to_nparray(self.__coordinates[i+1])
            if is_intersecting(a1, a2, b1, b2):
                logger.debug("Polygon labled for draw")
                return i
        return -1

    def draw(self, fig, plot=BASE_PLOT_STR, fill=False):
        pass

    def redraw(self):
        pass

    def is_empty(self):
        pass

    def __str__(self):
        logger.debug('Stringing shape')
        string = 'Coordinates:\n'
        for point in self.__coordinates:
            string += '  (%.4f,%.4f)\n' % (point[0], point[1])
        string += 'Attributes:\n'
        for item in self.__attributes:
            string += '  %s\n' % item
        string += 'Notes:\n  %s' % self.__note
        return string

    @staticmethod
    def toggle_drag(event):
        pass
