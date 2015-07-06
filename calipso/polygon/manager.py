######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################

from constants import *
from polygon.shape import Shape
from log import logger
from polygon.reader import PolygonReader

class ShapeManager(object):
    """
    Manages all shapes present on the screen, writes to database on
    call and provides other export functionality
    """

    outline_toggle = True
    hide_toggle = True

    def __init__(self, figure, canvas,  master):
        self.__figure = figure
        self.__canvas = canvas
        self.__master = master
        self.__current_plot = BASE_PLOT_STR
        logger.info('Defining initial shape manager')
        self.__shape_list = [[Shape(canvas)],
                             [Shape(canvas)],
                             [Shape(canvas)],
                             [Shape(canvas)]]
        logger.info("Instantiating Exporting Reader")
        self.__current_list = None
        self.__current_file = ''
        self.__hdf = ''
        self.__polygonreader = PolygonReader()
        self.__shape_count = 0
        # logger.info("Querying database for unique tag")
        # self.__count = db.query.unique_tag()

    def on_token_buttonpress(self, event):
        pass

    def on_token_buttonrelease(self, event):
        pass

    def on_token_motion(self, event):
        pass

    def anchor_rectangle(self, event):
        """
        Informs the correct shape list's blank object to plot a corner of a rectangle.

        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == BASE_PLOT_STR:
            logger.warning("Cannot draw to BASE_PLOT")
            return
        logger.debug('Anchoring %d, %d' % (event.xdata, event.ydata))
        self.__current_list[-1].anchor_rectangle(event)

    def get_count(self):
        pass

    def get_filename(self):
        pass

    def plot_point(self, event):
        pass

    def rubberband(self, event):
        """
        Uses a blank shape to draw 'helper rectangles' that outline the final shape of the
        object. wrapper function for calling :py:class:`polygon.Shape` method.

        :param event: A backend passes ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == BASE_PLOT_STR:
            logger.warning("Cannot draw to BASE_PLOT")
            return
        if event.button == 1 and event.xdata and event.ydata:
            logger.debug('Rubberbanding: %f, %f' % (event.x, event.y))
            self.__current_list[-1].rubberband(event)

    def fill_rectangle(self, event):
        """
        Informs the correct shape list's blank object to draw a rectangle to the screen
        using the provided cooridnates

        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == BASE_PLOT_STR:
            logger.warning("Cannot draw to BASE_PLOT")
            return
        logger.debug('Filling: %d, %d' % (event.xdata, event.ydata))
        logger.info('Creating rectangle')
        self.__current_list[-1].fill_rectangle(event, self.__figure, ShapeManager.outline_toggle)
        self.__current_list[-1].set_tag(self.generate_tag())
        self.__current_list.append(Shape(self.__canvas))
        self.__canvas.show()

    def set_hdf(self, hdf_filename):
        """
        Set the internal HDF filename variable

        :param str hdf_filename: Name of new HDF filename
        """
        self.__hdf = hdf_filename

    def set_current(self, plot):
        """
        Set the current view to ``plot``, and draw any shapes that exist in the manager for
        this plot. This is called each time a new view is rendered to the screen by
        ``set_plot`` in *Calipso*

        :param int plot: Acceptable plot constant from ``constants.py``
        """
        self.set_plot(plot)
        if len(self.__current_list) > 1:
            logger.info('Redrawing shapes')
            for shape in self.__current_list:
                if not shape.is_empty():
                    shape.redraw(self.__figure)

    def set_plot(self, plot):
        """
        Determine which list current_list should alias

        :param int plot: Acceptable plot constant from ``constants.py``
        """
        if plot == BASE_PLOT:
            logger.warning('set_plot called for BASE_PLOT')
            self.__current_list = self.__shape_list[BASE_PLOT]
            self.__current_plot = BASE_PLOT_STR
        elif plot == BACKSCATTERED:
            logger.info('set_plot to BACKSCATTERED')
            self.__current_list = self.__shape_list[BACKSCATTERED]
            self.__current_plot = BACKSCATTERED_STR
        elif plot == DEPOLARIZED:
            logger.info('set_plot to DEPOLARIZED')
            self.__current_list = self.__shape_list[DEPOLARIZED]
            self.__current_plot = DEPOLARIZED_STR

    def generate_tag(self, index=-1):
        """
        Produces a unique tag for each shape for each session

        :param int index: Generate new tag for given index
        :rtype: str
        """
        string = "shape" + str(self.__shape_count)
        self.__shape_count += 1
        return string

    def reset(self):
        """
        Clear the screen of any shapes present from the current_list
        """
        logger.info("Resetting ShapeManager")
        for shape in self.__current_list:
            shape.remove()
        idx = self.__shape_list.index(self.__current_list)
        self.__shape_list[idx] = [Shape(self.__canvas)]
        self.__current_list = self.__shape_list[idx]

        self.__count = 0
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
