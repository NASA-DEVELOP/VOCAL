######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################
from datetime import datetime
import tkMessageBox

from constants import Plot
import constants
from db import db
from log import logger
from polygon.reader import ShapeReader
from polygon.shape import Shape


class ShapeManager(object):
    """
    Manages all shapes present on the screen, writes to database on
    call and provides other export functionality
    """

    outline_toggle = True
    hide_toggle = True
    lock = None

    def __init__(self, figure, canvas,  master):
        self.__figure = figure
        self.__canvas = canvas
        self.__master = master
        self.__current_plot = Plot.baseplot
        logger.info('Defining initial shape manager')
        self.__shape_list = [[Shape(canvas)],
                             [Shape(canvas)],
                             [Shape(canvas)],
                             [Shape(canvas)]]
        logger.info("Instantiating Exporting Reader")
        self.__current_list = None
        self.__current_file = ''
        self.__hdf = ''
        self.__shapereader = ShapeReader()
        self.__data = {}
        logger.info("Querying database for unique tag")
        self.__shape_count = db.query_unique_tag()
        self.__moving_shape = None
        
    def anchor_rectangle(self, event):
        """
        Informs the correct shape list's blank object to plot a corner of a rectangle.
        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == Plot.baseplot:
            logger.warning("Cannot draw to BASE_PLOT")
            return
        if event.xdata and event.ydata:
            logger.info('Anchoring %d, %d' % (event.xdata, event.ydata))
            self.__current_list[-1].anchor_rectangle(event)
        else:
            logger.error('Anchor selected is out of range, skipping')

    def get_count(self):
        """
        Get the total amount of objects in existence inside ShapeManager, adds
        all lists up and subtracts the empty objects that are always appended
        to the end of the lists.

        :rtype: int
        """
        return len(self.__shape_list[0]) + len(self.__shape_list[1]) + \
            len(self.__shape_list[2]) + len(self.__shape_list[3]) - 4

    def get_filename(self):
        """
        Return JSON filename string

        :rtype: str
        """
        return self.__current_file

    def plot_point(self, event):
        """
        Plot a single point to the screen for the current shape object,
        if other points exist, a line is drawn between then until a
        polygon is formed
        :param event: A ``matplotlib.backend_bases.MouseEvent`` passed object
        """
        if self.__current_plot == Plot.baseplot:
            logger.warning('Cannot draw to the base plot')
            return
        if event.xdata and event.ydata:
            logger.info('Plotting point at %.5f, %.5f' % (event.xdata, event.ydata))
            check = self.__current_list[-1].plot_point(event, self.__current_plot,
                                                       self.__figure, ShapeManager.outline_toggle)
            if check:
                self.__current_list[-1].set_tag(self.generate_tag())
                self.__current_list.append(Shape(self.__canvas))
                self.__canvas.show()
        else:
            logger.error("Point to plot is out or range, skipping")

    def rubberband(self, event):
        """
        Uses a blank shape to draw 'helper rectangles' that outline the final shape of the
        object. wrapper function for calling :py:class:`polygon.Shape` method.
        :param event: A backend passes ``matplotlib.backend_bases.MouseEvent`` object
        """
        if event.button == 1:
            if self.__current_plot == Plot.baseplot:
                logger.warning("Cannot draw to BASE_PLOT")
                return
            if len(self.__current_list[-1].get_coordinates()) is 0:
                return
            logger.debug('Rubberbanding at %.5f, %.5f' % (event.x, event.y))
            self.__current_list[-1].rubberband(event)

    # noinspection PyProtectedMember
    def fill_rectangle(self, event):
        """
        Informs the correct shape list's blank object to draw a rectangle to the screen
        using the provided coordinates
        :param event: A backend passed ``matplotlib.backend_bases.MouseEvent`` object
        """
        if self.__current_plot == Plot.baseplot:
            logger.warning("Cannot draw to BASE_PLOT")
            return
        if event.xdata and event.ydata:
            if len(self.__current_list[-1].get_coordinates()) is 0:
                return
            logger.debug('Filling: %d, %d' % (event.xdata, event.ydata))
            logger.info('Creating rectangle')
            self.__current_list[-1].fill_rectangle(event, self.__current_plot,
                                                   self.__figure, ShapeManager.outline_toggle)
            self.__current_list[-1].set_tag(self.generate_tag())
            self.__current_list.append(Shape(self.__canvas))
            self.__canvas.show()
        else:
            logger.error('Bounds out of plot range, skipping')
            self.__current_list[-1].set_coordinates([])
            self.__canvas._tkcanvas.delete(self.__current_list[-1].lastrect)

    def set_hdf(self, hdf_filename):
        """
        Set the internal HDF filename variable
        :param str hdf_filename: Name of new HDF filename
        """
        self.__hdf = hdf_filename

    def set_current(self, plot, fig):
        """
        Set the current view to ``plot``, and draw any shapes that exist in the manager for
        this plot. This is called each time a new view is rendered to the screen by
        ``set_plot`` in *Calipso*
        :param int plot: Acceptable plot constant from ``constants.py``
        """
        logger.debug('Settings plot to %s' % plot)
        self.__figure = fig
        self.set_plot(plot)
        if len(self.__current_list) > 1:
            logger.info('Redrawing shapes')
            for shape in self.__current_list[:-1]:
                if not shape.is_empty():
                    shape.redraw(self.__figure, ShapeManager.outline_toggle)
            self.__canvas.show()

    def set_plot(self, plot):
        """
        Determine which list current_list should alias
        :param constants.Plot plot: Acceptable plot constant from ``constants.py``
        """
        if plot == Plot.baseplot:
            logger.warning('set_plot called for BASE_PLOT')
            self.__current_list = self.__shape_list[Plot.baseplot.value]
            self.__current_plot = Plot.baseplot
        elif plot == Plot.backscattered:
            logger.info('set_plot to BACKSCATTERED')
            self.__current_list = self.__shape_list[Plot.backscattered.value]
            self.__current_plot = Plot.backscattered
        elif plot == Plot.depolarized:
            logger.info('set_plot to DEPOLARIZED')
            self.__current_list = self.__shape_list[Plot.depolarized.value]
            self.__current_plot = Plot.depolarized

    def generate_tag(self):
        """
        Produces a unique tag for each shape for each session
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
        for shape in self.__current_list[:-1]:
            shape.remove()
        self.__canvas.show()
        idx = self.__shape_list.index(self.__current_list)
        self.__shape_list[idx] = [Shape(self.__canvas)]
        self.__current_list = self.__shape_list[idx]

        self.__shape_count = 0

    def delete(self, event):
        """
        Delete the specified object from the screen, searches through the
        current list to find the artist that was clicked on

        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        shape = event.artist
        for item in self.__current_list:
            poly = item.get_itemhandler()
            if poly == shape:
                self.__current_list.remove(item)
                break
        shape.remove()
        self.__canvas.show()

    def outline(self):
        """
        Toggle whether current shapes should be outlined or remained filled on
        the screen
        """
        ShapeManager.outline_toggle = not ShapeManager.outline_toggle
        for shape in self.__current_list:
            poly = shape.get_itemhandler()
            if poly is not None and ShapeManager.outline_toggle:
                poly.set_fill(True)
            elif poly is not None and not ShapeManager.outline_toggle:
                poly.set_fill(False)
        self.__canvas.show()

    def hide(self):
        """
        Hide all current shapes on the plot
        """
        ShapeManager.hide_toggle = not ShapeManager.hide_toggle
        for shape in self.__current_list:
            poly = shape.get_itemhandler()
            if poly is not None and ShapeManager.hide_toggle:
                color = shape.get_color()
                poly.set_fill(True)
                poly.set_facecolor(color)
                poly.set_edgecolor('#000000')
            elif poly is not None and not ShapeManager.hide_toggle:
                poly.set_fill(False)
                poly.set_facecolor('none')
                poly.set_edgecolor('none')
        self.__canvas.show()

    def properties(self, event):
        """
        Return the properties of the shape clicked on by the user
        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        target = event.artist
        for shape in self.__current_list:
            if shape.get_itemhandler() is target:
                tkMessageBox.showinfo("properties", str(shape))
                return
        logger.warning("Shape not found")
        
    def toggle_drag(self, event):
        pass

    def find_shape(self, event):
        """
        Return the handle to the shape found via the user clicking on one
        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        target = event.artist
        for shape in self.__current_list:
            if shape.get_itemhandler() is target:
                logger.info("Found shape")
                return shape
        logger.error("Shape not found")
        
    def read_plot(self, filename='', read_from_str=''):
        """
        Reads shapes from either a string or a file in JSON format, and packs the screen
        with the shapes parsed. **note:** if a string is passed as *well* as a filename,
        the string takes priority

        :param str filename: The filename to read valid JSON shapes from
        :param str read_from_str: The string to read valid JSON shapes from
        """
        if read_from_str != '':
            # TODO: shape is not being added to the list when importing from database
            logger.info('Reading JSON from string')
            self.__shapereader.read_from_str_json(read_from_str)
        else:
            logger.info('Reading JSON from file')
            self.__polygonreader.set_filename(filename)
            self.__polygonreader.read_from_file_json()
        plot = Plot.baseplot.value
        logger.info('Parse JSON data for new polygons')
        for lst in self.__shape_list:
            self.__polygonreader.pack_shape(lst, constants.PLOTS[plot], self.__canvas)
            if self.__current_plot.value == plot:
                for shape in lst:
                    if not shape.is_empty():
                        logger.info('Shape found in \'%s\', drawing' %
                                    constants.PLOTS[plot])
                        shape.redraw(self.__figure, ShapeManager.outline_toggle)
            plot += 1
        self.__canvas.show()

    def save_db(self):
        if len(self.__current_list) == 1:
            logger.error("No shapes to export to database")
            return False
        today = datetime.utcnow().replace(microsecond=0)
        db.commit_to_db(self.__current_list, str(today), self.__hdf)
        return True

    def save_json(self, filename=''):
        if filename != "":
            self.__current_file = filename
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data['hdffile'] = self.__hdf
        shapeDict = {}
        for i in range(len(self.__shape_list)):
            self.__data[constants.PLOTS[i]] = {}
        i = self.__shape_list.index(self.__current_list)
        for j in range(len(self.__current_list)-1):
            tag = self.__current_list[j].get_tag()
            coordinates = self.__current_list[j].get_coordinates()
            color = self.__current_list[j].get_color()
            attributes = self.__shape_list[i][j].get_attributes()
            note = self.__shape_list[i][j].get_notes()
            _id = self.__shape_list[i][j].get_id()
            value = {"coordinates": coordinates, "color": color, "attributes": attributes, "notes": note, "id": _id}
            shapeDict[tag] = value
        self.__data[constants.PLOTS[i]] = shapeDict
        logger.info("Encoding to JSON")
        db.encode(self.__current_file, self.__data)

    def save_all_json(self, filename=""):
        logger.info("Saving all shapes to JSON")
        if filename is not None:
            self.__current_file = filename
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data['hdffile'] = self.__hdf
        for i in range(len(self.__shape_list)):
            shapeDict = {}
            for j in range(len(self.__shape_list[i])-1):
                tag = self.__shape_list[i][j].get_tag()
                coordinates = self.__shape_list[i][j].get_coordinates()
                color = self.__shape_list[i][j].get_color()
                attributes = self.__shape_list[i][j].get_attributes()
                note = self.__shape_list[i][j].get_notes()
                _id = self.__shape_list[i][j].get_id()
                value = {"coordinates": coordinates, "color": color, "attributes": attributes, "notes": note, "id": _id}
            shapeDict[tag] = value
        self.__data[constants.PLOTS[i]] = shapeDict
        logger.info("Encoding to JSON")
        db.encode(self.__current_file, self.__data)
