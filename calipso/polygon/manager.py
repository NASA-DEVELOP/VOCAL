######################################
#    Created on Jul 5, 2015
#
#    @author: Nathan Qian
#    @author: Grant Mercer
######################################
import constants
import matplotlib as mpl
import tkMessageBox

from constants import DATEFORMAT, Plot, CONF
from datetime import datetime
from polygon.reader import ShapeReader
from polygon.shape import Shape
from propertiesdialog import PropertyDialog
from db import db
from log.log import logger


class ShapeManager(object):
    """
    Manages all shapes present on the screen, writes to database on
    call and provides other export functionality
    """

    outline_toggle = True                   # global var for setting fill of shapes
    hide_toggle = True                      # global var for hiding shapes
    shape_count = db.query_unique_tag()     # global shape_count for initial shape tag

    def __init__(self, figure, canvas,  master):
        self.__figure = figure                          # figure to draw to
        self.__canvas = canvas                          # canvas the figure lives on
        self.__master = master                          # CALIPSO
        self.__current_plot = Plot.baseplot             # default plot
        logger.info('Defining initial shape manager')
        self.__shape_list = [[Shape(canvas)],           # baseplot
                             [Shape(canvas)],           # backscattered
                             [Shape(canvas)],           # depolarized
                             [Shape(canvas)],			# vfm
                             [Shape(canvas)],			# iwp
                             [Shape(canvas)],           # horiz_avg
                             [Shape(canvas)]]           # aerosol_subtype

        logger.info("Instantiating Exporting Reader")
        self.__current_list = None          # aliases shape_list's current plot
        self.__current_file = ''            # current JSON file, NOT .hdf file!
        self.__hdf = ''                     # hdf file
        self.__shapereader = ShapeReader()  # internal reader object for exporting
        self.__data = {}                    # data to hold JSON data for exporting
        logger.info("Querying database for unique tag")
        self.__selected_shapes = []         # shapes that are currently selected

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

    def clear_lines(self):
        """
        Clear any existing lines or unfilled shapes when the 'Free Draw' button
        is unpressed. This is fix a bug that is caused by polygons not being
        finished but corrupting future shapes.
        """
        if self.__current_plot == Plot.baseplot:
            return
        self.__current_list[-1].clear_unfinished_data()
        self.__canvas.show()

    def clear_refs(self):
        """
        Clear all references to the current figure, this is called
        in the ``Calipso`` class when a plot is to be set as to ensure
        no dangling references are left
        """
        for shape in self.__current_list[:-1]:
            ih = shape.get_itemhandler()
            if ih is not None:
                ih.remove()

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
                logger.info('Deleting %s' % item.get_tag())
                self.__current_list.remove(item)
                break
        shape.remove()
        self.__canvas.show()

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
            self.__current_list[-1].fill_rectangle(event, self.__current_plot, self.__hdf,
                                                   self.__figure, ShapeManager.outline_toggle)
            self.__current_list[-1].set_tag(self.generate_tag())
            self.__current_list.append(Shape(self.__canvas))
            self.__canvas.show()
        else:
            logger.error('Bounds out of plot range, skipping')
            self.__current_list[-1].set_coordinates([])
            self.__canvas._tkcanvas.delete(self.__current_list[-1].lastrect)

    def find_shape(self, event):
        """
        Return the handle to the shape found via the user clicking on one

        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        target = event.artist
        for shape in self.__current_list:
            if shape.get_itemhandler() is target:
                return shape

    @staticmethod
    def generate_tag():
        """
        Produces a unique tag for each shape for each session

        :rtype: :py:class:`str`
        """
        string = "shape" + str(ShapeManager.shape_count)
        ShapeManager.shape_count += 1
        return string

    def get_count(self):
        """
        Get the total amount of objects in existence inside ShapeManager, adds
        all lists up and subtracts the empty objects that are always appended
        to the end of the lists.

        :rtype: :py:class:`int`
        """
        return len(self.__shape_list[0]) + len(self.__shape_list[1]) + \
               len(self.__shape_list[2]) + len(self.__shape_list[3]) + len(self.__shape_list[4]) + \
               len(self.__shape_list[5]) + len(self.__shape_list[6]) - 7

    def get_current_list(self):
        """
        Return the current list

        .. warning::
           This function should **never** be used for any write operation. Using
           this function should be for **read only**.

        :rtype: :py:class:`list`
        """
        return self.__current_list

    def get_hdf(self):
        """
        Return the hdf string that is currently being used

        :rtype: :py:class:`str`
        """
        return self.__hdf

    def get_filename(self):
        """
        Return JSON filename string

        :rtype: :py:class:`str`
        """
        return self.__current_file

    def get_selected_count(self):
        """
        Get the total amount of *selected* objects in existence inside ShapeManager
        """
        return len(self.__selected_shapes)

    def hide(self):
        """
        Hide all current shapes on the plot
        """

        logger.info('Settings hide option for all shapes to %s' % str(ShapeManager.hide_toggle))
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

    def is_all_saved(self, plot=None):
        """
        Checks if all the shapes have been saved. If plot is None, the method
        will check if all shapes in every plot has been saved. If a plot is
        specified, then it will only check the shapes in the specified plot.
        This method will automatically ignore the last blank shapes.

        :param plot: the plot of the shapes to check
        """
        if plot is None:
            for i in range(len(self.__shape_list)):
                for j in range(len(self.__shape_list[i])-1):
                    if not self.__shape_list[i][j].get_saved():
                        return False
            return True
        else:
            for i in range(len(self.__shape_list[plot.value])-1):
                if not self.__shape_list[plot.value][i].get_saved():
                    return False
            return True

    def outline(self):
        """
        Toggle whether current shapes should be outlined or remained filled on
        the screen
        """
        logger.info('setting all shape fill to %s' % str(ShapeManager.outline_toggle))
        ShapeManager.outline_toggle = not ShapeManager.outline_toggle
        for shape in self.__current_list:
            poly = shape.get_itemhandler()
            if poly is not None and ShapeManager.outline_toggle:
                poly.set_fill(True)
                poly.set_linewidth(1.0)
            elif poly is not None and not ShapeManager.outline_toggle:
                poly.set_fill(False)
                poly.set_linewidth(2.0)
        self.__canvas.show()

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
            check = self.__current_list[-1].plot_point(event, self.__current_plot, self.__hdf,
                                                       self.__figure, ShapeManager.outline_toggle)
            if check:
                self.__current_list[-1].set_tag(self.generate_tag())
                self.__current_list.append(Shape(self.__canvas))
                self.__canvas.show()
        else:
            logger.error("Point to plot is out or range, skipping")

    # noinspection PyProtectedMember
    def properties(self, event):
        """
        Return the properties of the shape clicked on by the user and create a small
        tooltip which displays these properties

        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        target = event.artist
        logger.debug("Creating property window")
        for shape in self.__current_list:
            if shape.get_itemhandler() is target:
                # if self.property_window is not None:
                #    self.destroy_property_window()
                PropertyDialog(self.__master.get_root(), shape)
                return
        logger.warning("Shape not found")

    def read_plot(self, filename='', read_from_str=''):
        """
        Reads shapes from either a string or a file in JSON format, and packs the screen
        with the shapes parsed. **note:** if a string is passed as *well* as a filename,
        the string takes priority

        :param str filename: The filename to read valid JSON shapes from
        :param str read_from_str: The string to read valid JSON shapes from
        """
        if read_from_str != '':
            logger.info('Reading JSON from string')
            read_data = self.__shapereader.read_from_str_json(read_from_str)
        else:
            logger.info('Reading JSON from file')
            self.__shapereader.set_filename(filename)
            read_data = self.__shapereader.read_from_file_json()

        if self.__hdf.rpartition('/')[2] != read_data['hdffile']:    # Do HDF files match?
            tkMessageBox.showerror('file',
            'Shape-associated HDF file \n and current HDF do not match')
            logger.error('Shape-associated HDF file and current HDF do not match')
            return

        for key in constants.plot_type_enum:
            lst = self.__shape_list[constants.plot_type_enum[key]]
            self.__shapereader.pack_shape(lst, key, self.__canvas, read_from_str,)
            # The "or CONF.persistent_shapes" allows shapes that don't match the plot to be shown
            if self.__current_plot == constants.plot_type_enum[key] or CONF.persistent_shapes:
                for shape in lst:
                    if not shape.is_empty():
                        logger.info('Shape found in \'%s\', drawing' % key)
                        shape.redraw(self.__figure, read_data['hdffile'],
                                     ShapeManager.outline_toggle)
            self.__canvas.show()

    def reset(self, all_=False):
        """
        Clear the screen of any shapes present from the current_list
        """
        if all_:
            logger.info('clearing all shapes')
            self.__shape_list = [[Shape(self.__canvas)],           # baseplot
                                 [Shape(self.__canvas)],           # backscattered
                                 [Shape(self.__canvas)],           # depolarized
                                 [Shape(self.__canvas)],           # vfm
                                 [Shape(self.__canvas)],           # iwp
                                 [Shape(self.__canvas)],           # horiz_avg
                                 [Shape(self.__canvas)]]           # aerosol_subtype
        else:
            logger.info('Resetting ShapeManager')
            for shape in self.__current_list:
                if not shape.is_empty():
                    shape.remove()
            self.__canvas.show()
            idx = self.__shape_list.index(self.__current_list)
            self.__shape_list[idx] = [Shape(self.__canvas)]
            self.__current_list = self.__shape_list[idx]

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
            self.__current_list[-1].rubberband(event)

    def save_db(self, only_selected=False):
        """
        Commit all polygons currently in display to the database. Existing database
        objects will simply be updated, while objects not present in the database
        will be assigned a new primary key and have an entry generated for them.
        Returns ``True`` if success, ``False`` otherwise

        :rtype: :py:class:`bool`
        """
        if len(self.__current_list) == 1:
            logger.error('No shapes found')
            return False
        today = datetime.utcnow().replace(microsecond=0)
        if(only_selected):
            db.commit_to_db(self.__selected_shapes, today, self.__hdf)
        else:
            # Must account for dummy object at end of current list
            db.commit_to_db(self.__current_list[:-1], today)
        return True

    def save_json(self, filename=''):
        """
        Save all shapes selected on the screen to a specified JSON object,
        if no file is passed the internal file variable is used. There should **never**
        arise a case where no file is passed either from the internal or external
        parameters, ``Calipso`` has proper error checking.

        :param str filename: custom filename to save JSON objects to
        """
        if filename != '':
            self.__current_file = filename
        if not self.__selected_shapes:
            logger.warning('No shapes selected, saving empty plot')
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data['hdffile'] = self.__hdf.rpartition('/')[2]
        shape_dict = {}
        for i in range(len(self.__shape_list)):
            self.__data[constants.PLOTS[i]] = {}
        i = self.__shape_list.index(self.__current_list)
        for j in range(len(self.__selected_shapes)):
            if not self.__selected_shapes[j].get_saved():
                self.__selected_shapes[j].save()
            tag = self.__selected_shapes[j].get_tag()
            coordinates = self.__selected_shapes[j].get_coordinates()
            color = self.__selected_shapes[j].get_color()
            attributes = self.__selected_shapes[j].get_attributes()
            note = self.__selected_shapes[j].get_notes()
            _id = self.__selected_shapes[j].get_id()

            time_cords = [mpl.dates.num2date(x[0]) for x in coordinates]
            alt_cords = [x[1] for x in coordinates]
            blat = self.__selected_shapes[j].get_min_lat()
            elat = self.__selected_shapes[j].get_max_lat()
            btime = min(time_cords).strftime(DATEFORMAT)
            etime = max(time_cords).strftime(DATEFORMAT)
            balt = min(alt_cords)
            ealt = max(alt_cords)

            value = {'coordinates': coordinates, 'blat': blat, 'elat': elat,
                     'btime': btime, 'etime': etime, 'balt': balt, 'ealt': ealt,
                     'color': color, 'attributes': attributes, 'notes': note, 'id': _id}
            shape_dict[tag] = value
        self.__data[constants.PLOTS[i]] = shape_dict
        logger.info('Encoding to JSON')
        db.encode(self.__current_file, self.__data)

    def save_all_json(self, filename=""):
        """
        Same as ``save_json``, but save **all** shapes across **all** plots instead.

        :param str filename: custom filename to save JSON objects to
        """
        logger.info("Saving all shapes to JSON")
        if filename is not None:
            self.__current_file = filename
        today = datetime.utcnow().replace(microsecond=0)
        self.__data['time'] = str(today)
        self.__data['hdffile'] = self.__hdf.rpartition('/')[2]
        for i in range(len(self.__shape_list)):
            shape_dict = {}
            for j in range(len(self.__shape_list[i])-1):
                if not self.__shape_list[i][j].get_saved():
                    self.__shape_list[i][j].save()
                tag = self.__shape_list[i][j].get_tag()
                coordinates = self.__shape_list[i][j].get_coordinates()
                lat = self.__shape_list[i][j].generate_lat_range()
                color = self.__shape_list[i][j].get_color()
                attributes = self.__shape_list[i][j].get_attributes()
                note = self.__shape_list[i][j].get_notes()
                _id = self.__shape_list[i][j].get_id()
                value = {'coordinates': coordinates, 'lat': lat, 'color': color,
                         'attributes': attributes, 'notes': note, 'id': _id}
            shape_dict[tag] = value
        self.__data[constants.PLOTS[i]] = shape_dict
        logger.info('Encoding to JSON')
        db.encode(self.__current_file, self.__data)

    def select_all(self):
        """
        Set all objects within the current list as selected. Loops through all
        shapes in the plot and sets their highlight as well as adding them to
        the internal selected list
        """
        logger.info('Selecting %d shapes', len(self.__current_list)-1)
        for i in self.__current_list[:-1]:
            i.set_highlight(True)
        self.__selected_shapes = (self.__current_list[:-1])
        self.__canvas.show()

    def deselect_all(self):
        """
        Remove selection from all objects on screen. Loops through all shapes
        in the plot and sets their highlight to default and resets the internal
        selected list
        """
        logger.info('Deselecting %d shapes', len(self.__current_list)-1)
        for i in self.__current_list[:-1]:
            i.set_highlight(False)
        self.__selected_shapes = []
        self.__canvas.show()

    def select_from_tag(self, tag):
        """
        Highlight the shape specified by ``tag``. Ensures to reset
        any other objects that may be highlighted. Not to be confused
        with ``select(self, event)``, which is for multiple selections
        via event objects

        :param str tag: The tag of the object
        """
        if tag == "" and self.__selected_shapes:
            logger.info('Disabling selection for all shapes')
            for x in self.__selected_shapes:
                # The shape may have been removed, so we should ensure it exists
                if x: x.set_highlight(False)
            self.__selected_shapes = []
            self.__canvas.show()
            return
        for shape in self.__current_list[:-1]:
            if shape.get_tag() == tag:
                logger.info('Selecting %s' % tag)
                for x in self.__selected_shapes:
                    if x: x.set_highlight(False)
                self.__selected_shapes.append(shape)
                shape.set_highlight(True)
                break
        self.__canvas.show()

    def select_from_event(self, event):
        """
        Highlight the selected object and add to internal list of highlighted objects

        :param event: A passed ``matplotlib.backend_bases.PickEvent`` object
        """
        shape = event.artist
        for item in self.__current_list:
            poly = item.get_itemhandler()
            if poly == shape:
                if not item.is_selected():
                    logger.info('Selecting %s' % item.get_tag())
                    item.set_highlight(True)
                    self.__selected_shapes.append(item)
                else:
                    logger.info('Deselecting %s' % item.get_tag())
                    item.set_highlight(False)
                    self.__selected_shapes.remove(item)
                break
        self.__canvas.show()

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
        # Check if persistent shapes, use backscatter as the shapes list if so
        if CONF.persistent_shapes:
            self.__current_list = self.__shape_list[Plot.backscattered]
        if len(self.__current_list) > 1:
            logger.info('Redrawing shapes')
            for shape in self.__current_list[:-1]:
                if not shape.is_empty():
                    shape.loaded_draw(self.__figure, ShapeManager.outline_toggle)
            self.__canvas.show()

    def set_hdf(self, hdf_filename):
        """
        Set the internal HDF filename variable

        :param str hdf_filename: Name of new HDF filename
        """
        self.__hdf = hdf_filename

    def set_plot(self, plot):
        """
        Determine which list current_list should alias, also set internal plot
        variable

        :param constants.Plot plot: Acceptable plot constant from ``constants.py``
        """
        if plot == Plot.baseplot:
            logger.warning('set_plot called for BASE_PLOT')
            self.__current_list = self.__shape_list[Plot.baseplot]
            self.__current_plot = Plot.baseplot
        elif plot == Plot.backscattered:
            logger.info('set_plot to BACKSCATTERED')
            self.__current_list = self.__shape_list[Plot.backscattered]
            self.__current_plot = Plot.backscattered
        elif plot == Plot.depolarized:
            logger.info('set_plot to DEPOLARIZED')
            self.__current_list = self.__shape_list[Plot.depolarized]
            self.__current_plot = Plot.depolarized
        elif plot == Plot.vfm:
            logger.info('set_plot to VFM')
            self.__current_list = self.__shape_list[Plot.vfm]
            self.__current_plot = Plot.vfm
        elif plot == Plot.iwp:
            logger.info('set_plot to IWP')
            self.__current_list = self.__shape_list[Plot.iwp]
            self.__current_plot = Plot.iwp
        elif plot == Plot.horiz_avg:
            logger.info('set_plot to HORIZ_AVG')
            self.__current_list = self.__shape_list[Plot.horiz_avg]
            self.__current_plot = Plot.horiz_avg
        elif plot == Plot.horiz_avg:
            logger.info('set_plot to AEROSOL SUBTYPE')
            self.__current_list = self.__shape_list[Plot.aerosol_subtype]
            self.__current_plot = Plot.aerosol_subtype
