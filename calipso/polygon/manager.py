######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

import constants
from polygon.shape import Shape
from log import logger

class ShapeManager(object):
    """
    Manages all shapes present on the screen, writes to database on
    call and provides other export functionality
    """

    outline_toggle = True
    hide_toggle = True

    def __init__(self, canvas, master):
        self.__canvas = canvas
        self.__master = master
        self.__current_plot = constants.BASE_PLOT
        logger.info('Defining initial shape manager')
        self.__shape_dict = {constants.BACKSCATTERED_STR: [Shape()],
                             constants.DEPOLARIZED_STR: [Shape()],
                             constants.VFM_STR: [Shape()]}
        pass

    def on_token_buttonpress(self, event):
        pass

    def on_token_buttonrelease(self, event):
        pass

    def on_token_motion(self, event):
        pass

    def set_plot(self, plot):
        pass

    def anchor_rectangle(self, event):
        """
        Informs the correct shape list's blank object to plot a corner of a rectangle.

        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == constants.BASE_PLOT:
            return
        logger.info('Anchoring %d, %d' % (event.xdata, event.ydata))

    def get_count(self):
        pass

    def get_filename(self):
        pass

    def plot_point(self, event):
        pass

    def rubberband(self, event):
        """
        Uses a blank shape to draw 'helper rectangles' that outline the final shape of the
        object

        :param event: A backend passes ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == constants.BASE_PLOT:
            return
        if event.button == 1 and event.xdata and event.ydata:
            logger.info('Rubberbanding: %d, %d' % (event.xdata, event.ydata))

    def fill_rectangle(self, event):
        """
        Informs the correct shape list's blank object to draw a rectangle to the screen
        using the provided cooridnates

        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == constants.BASE_PLOT:
            return
        logger.info('Filling: %d, %d' % (event.xdata, event.ydata))

    def set_hdf(self, hdf_filename):
        pass

    def draw(self, figure, plot):
        self.__current_plot = plot
        pass

    def generate_tag(self, index=-1):
        pass

    def reset(self):
        pass

    def delete(self, event):
        pass

    def outline(self):
        pass

    def paint(self, event):
        pass

    def hide(self):
        pass

    def properties(self, event):
        pass

    def toggle_drag(self, event):
        pass

    def find_shape(self, event):
        pass

    def __find_shape_by_itemhandler(self, itemhandler):
        pass

    @staticmethod
    def __plot_into_string(plot):
        pass

    @staticmethod
    def plot_string_to_int(plot):
        pass

    def read_plot(self, filename='', read_from_str=''):
        pass

    def save_db(self):
        pass

    def save_json(self, filename=''):
        pass

    def save_all_json(self, filename):
        pass