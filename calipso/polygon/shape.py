######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

import random
import constants
import matplotlib as mpl
import matplotlib.lines as mlines

from constants import Plot, TAGS
from log import logger
from matplotlib.patches import Polygon
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
        self.__item_handler = None
        self.__plot = Plot.baseplot
        self.__attributes = []
        self.__note = ''
        self.__id = None
        self.lastrect = None
        self.__prev_x = 1.0
        self.__prev_y = 1.0
        self.__lines = []

    def anchor_rectangle(self, event):
        """
        Establishes a corner of a rectangle as an anchor for when the user drags the cursor to
        create a rectangle. Used in 'Draw Rect' button

        :param event: A matplotlib backend event object
        """
        self.__coordinates.append((event.xdata, event.ydata))
        self.__prev_x = event.x
        self.__prev_y = event.y

    def plot_point(self, event, plot, fig, fill=False):
        """
        Plot a single point to the shape, connect any previous existing
        points and fill to a shape if the current coordinate intersects
        the beginning point.
        :param event: A ``matplotlib.backend_bases.MouseEvent`` passed object
        :param fig: The figure to be drawing the canvas to
        :param bool fill: Whether the shape will have a solid fill or not
        """
        self.__coordinates.append((event.xdata, event.ydata))
        logger.debug("Plotted point at (%0.5f, %0.5f)", event.xdata, event.ydata)
        if len(self.__coordinates) > 1:
            logger.debug("Drawing line from plot")
            self.__lines.append(
                mlines.Line2D((self.__prev_x, event.xdata),
                              (self.__prev_y, event.ydata),
                              linewidth=2.0,
                              color='#000000'))
            fig.add_artist(self.__lines[-1])
            self.__canvas.show()
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
                for line in self.__lines:
                    line.remove()
                self.__lines = []
                self.draw(fig, plot, fill)
                self.__plot = plot
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
        if event.xdata and event.ydata:
            logger.debug('%f, %f', event.xdata, event.ydata)
        self.lastrect = self.__canvas._tkcanvas.create_rectangle(self.__prev_x,
                                                                 abs(constants.HEIGHT - self.__prev_y - 35),
                                                                 event.x,
                                                                 abs(constants.HEIGHT - event.y - 35))

    def fill_rectangle(self, event, plot, fig, fill=False):
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

        if event.xdata is not None and event.ydata is not None:
            logger.debug('Generating rectangular points')
            beg = self.__coordinates[0]
            self.__coordinates.append((event.xdata, beg[1]))
            self.__coordinates.append((event.xdata, event.ydata))
            self.__coordinates.append((beg[0], event.ydata))

            self.draw(fig, plot, fill)
        else:
            self.__coordinates = []

    def draw(self, fig, plot=Plot.baseplot, fill=False):
        logger.info("Drawing polygon")

        # Generates a gnarly random color brah
        r = lambda: random.randint(0, 255)
        clr = '#%02X%02X%02X' % (r(), r(), r())

        self.__color = clr
        self.__plot = plot
        self.__item_handler = \
            Polygon(self.__coordinates, facecolor=clr, fill=fill, picker=5)
        fig.add_patch(self.__item_handler)

    def redraw(self, fig, fill):
        """
        Function to draw the shape in the event the shape *may* or *may not* already
        be drawn. Checks if the image already exists, if not draws the image

        :param fig: A ``SubplotAxes`` object to add the patch to
        :param bool fill: Boolean value whether to have the shape filled in when
        drawn or not
        """
        if self.__item_handler.is_figure_set():
            self.__item_handler.remove()
        self.__item_handler = \
            Polygon(self.__coordinates, facecolor=self.__color, fill=fill, picker=5)
        fig.add_patch(self.__item_handler)

    def loaded_draw(self, fig, fill):
        """
        Called in the case of panning the plot, since panning the plot invalidates
        the previous figure, the figures must first be cleared and the shapes are removed.
        Loaded draw draws the shapes back into view using a new figure.

        :param fig: A ``SubplotAxes`` object to add the patch to
        :param bool fill: Boolean value whether to have the shape filled in when drawn to or not
        """
        self.__item_handler = \
            Polygon(self.__coordinates, facecolor=self.__color, fill=fill, picker=5)
        fig.add_patch(self.__item_handler)

    def add_attribute(self, attr):
        """
        Append a passed attribute onto the internal attribute list
        :param str attr: An attribute enum
        """
        if attr in TAGS:
            self.__attributes.append(attr)
        else:
            logger.error('Caught invalid attribute for adding \'%s\'' % attr)

    def remove_attribute(self, attr):
        """
        Remove an attribute as specified in ``constants.py`` from the internal attributes variable

        :param str attr:
        """
        if attr in TAGS:
            self.__attributes.remove(attr)
        else:
            logger.error('Caught invalid attribute for removal \'%s\'' % attr)

    def set_attributes(self, attributes_list):
        """
        Set the internal list of attributes to a custom passed list
        :param list attributes_list:
        """
        for i in attributes_list:
            if i not in TAGS:
                logger.error('Caught invalid attribute for setting \'%s\'' % i)
                return
        self.__attributes = attributes_list

    def set_tag(self, tag):
        """
        Set internal tag variable
        :param str tag:
        """
        self.__tag = tag

    def set_color(self, color):
        """
        Set internal color variable
        :param str color: Valid hexadecimal color value
        """
        self.__color = color

    def set_plot(self, plot):
        """
        Manually set the new value of the internal plot variable. **unsafe**
        :param constants.Plot plot: Plot value
        """
        self.__plot = plot

    def set_coordinates(self, coordinates):
        """
        Pass a list of coordinates to set to the shape to. *just because it exists
        does not mean you should use it* -me

        :param list coordinates:
        """
        self.__coordinates = coordinates

    def set_id(self, _id):
        """
        Set the database ID of the shape. **unsafe** to use outside letting
        database call this.

        :param int _id: Database primary key
        """
        self.__id = _id

    def set_notes(self, note):
        """
        Pass a string containing new notes to set the shape to

        :param str note: New note string
        """
        self.__note = note

    def get_coordinates(self):
        """
        Return the list of coordinates internally maintained by shape

        :rtype: list
        """
        return self.__coordinates

    def get_notes(self):
        """
        Return the notes string internally maintained by shape

        :rtype: str
        """
        return self.__note

    def get_attributes(self):
        """
        Return attributes list maintained by shape

        :rtype: list
        """
        return self.__attributes

    def get_plot(self):
        """
        Return the plot type

        :rtype: int
        """
        return self.__plot

    def get_color(self):
        """
        Return the hexdecimal color value

        :rtype: str
        """
        return self.__color

    def get_id(self):
        """
        Return the database ID of shape

        :rtype: int
        """
        return self.__id

    def get_tag(self):
        """
        Return the program Tag of shape

        :rtype: str
        """
        return self.__tag

    def get_itemhandler(self):
        """
        Return the item handler object to the actual backend base

        :rtype: ``matplotlib.patches.polygon``
        """
        return self.__item_handler

    def is_attribute(self, attr):
        """
        Return ``True`` if *attr* is inside the attributes list, ``False``
        otherwise.

        :param str attr:
        :rtype: bool
        """
        for item in self.__attributes:
            if attr == item:
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
                logger.debug("Polygon labeled for draw")
                return i
        return -1

    def remove(self):
        """
        Wrapper function to internally call matplotlib backend to remove
        the shape from the figure
        """
        self.__item_handler.remove()

    def is_empty(self):
        if len(self.__coordinates) == 0:
            return True
        return False

    def __str__(self):
        logger.debug('Stringing shape')
        time_cords = [mpl.dates.num2date(x[0]).strftime('%H:%M:%S %p') for
                      x in self.__coordinates]
        altitude_cords = [x[1] for x in self.__coordinates]
        string = 'Time Scale:\n\t%s - %s\n' % (min(time_cords), max(time_cords))
        string += 'Altitude Scale:\n\t%.4f km - %.4f km\n' % (min(altitude_cords), max(altitude_cords))
        if len(self.__attributes) > 0:
            string += 'Attributes:\n'
            for item in self.__attributes:
                string += '  %s\n' % item
        if self.__note != '':
            string += 'Notes:\n  %s' % self.__note
        return string

    @staticmethod
    def toggle_drag(event):
        pass
