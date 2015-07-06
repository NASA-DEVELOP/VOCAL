######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

import constants

class Shape(object):
    """
    Displays the polygon objects onto the canvas by supplying draw methods
    and maintaining internal information on the shape. Draws to matplotlib
    backend
    """

    drag_toggle= False
    color_counter = 0
    COLORS = ['snow', 'light cyan']

    def __init__(self, tag='', color=''):
        self.__vertices = []
        self.__coordinates = []
        self.__tag = tag
        self.__color = color
        self.__item_handler = 0
        self.__plot = constants.BASE_PLOT
        self.__attributes = []
        self.__note = ''
        self.__id = None

    def anchor_rectangle(self, event):
        """
        Establishes a corner of a rectangle as an anchor for when the user drags the cursor to create
        a rectangle. Used in 'Draw Rect' button

        :param event: A matplotlib backend event object
        """
        self.__vertices.append((event.x, event.y))
        self.__coordinates.append((event.xdata, event.ydata))


    def plot_point(self, event):
        pass

    def rubberband(self, event):
        pass

    def fill_rectangle(self, event):
        pass

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

    def draw(self):
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