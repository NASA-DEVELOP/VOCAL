######################################
#     Created on Jun 15, 2015
#
#     @author: nqian
#     @author: Grant Mercer
######################################
# import antigravity
import ast
import json
import constants

from constants import PLOTS
from log.log import logger
from polygon.shape import Shape
from tools.tools import byteify
from db import db


class ShapeReader(object):
    """
    Reads JSON files and transfers the data into PolygonDrawer objects

    :param str filename: Internal filename to write to
    """

    def __init__(self, filename=''):
        """
        Initializes attributes
        """
        self.filename = filename
        self.__data = {}

    def set_filename(self, filename):
        """
        Sets the file name destination

        :param str filename: the name of the file
        """
        self.filename = filename
        
    def read_from_file_json(self):
        """
        Reads the data from the JSON file
        """
        with open(self.filename, 'r') as infile:
            data = byteify(json.load(infile))
        self.__data = data	
        return self.__data
        
    def read_from_str_json(self, data):
        """
        Reads JSON as a string

        :param str data: string representation of a JSON object
        """
        self.__data = byteify(json.loads(data))
        keys = [x for x in self.__data if x in constants.plot_type_enum.keys()]
        if not keys:
            logger.error("Invalid JSON plot keys passed, you WILL get some error after this eventually...")
        for plt in keys:
            for shape in self.__data[plt]:
                if 'coordinates' in self.__data[plt][shape]:
                    self.__data[plt][shape]['coordinates'] = \
                        [[x[0], x[1]] for x in ast.literal_eval(
                            self.__data[plt][shape]['coordinates']) if len(x) == 2]
                if 'attributes' in self.__data[plt][shape]:
                    self.__data[plt][shape]['attributes'] = \
                        ast.literal_eval(self.__data[plt][shape]['attributes'])
        return self.__data

    def pack_shape(self, shape_list, plot_type, canvas, read_from_str=None):
        """
        Stores the data in the JSON into PolygonDrawers

        :param shape_list: a Python list of PolygonDrawers
        :param plot_type: the current plot being displayed
        :param canvas: a Tkinter canvas to initialize the blank PolygonDrawer in the shape_list
        """
        from polygon.manager import ShapeManager
        enum_plot_type = constants.plot_type_enum[plot_type]

        try:
            for shape in self.__data[plot_type]:
                entry = self.__data[plot_type][shape]['id']
                if entry is not None and int(entry) in [x.get_id() for x in shape_list]:
                    continue
                logger.info('Found data in %s, packing polygon with JSON data'
                        % PLOTS[enum_plot_type])
                color = self.__data[plot_type][shape]['color']
                coordinates = self.__data[plot_type][shape]['coordinates']
                attributes = self.__data[plot_type][shape]['attributes']
                notes = self.__data[plot_type][shape]['notes']
                _id = self.__data[plot_type][shape]['id']
                _uuid = self.__data[plot_type][shape]['uuid']
                name = self.__data[plot_type][shape]['name']
                if db.exists_tag(shape) and not read_from_str:
                    new = ShapeManager.generate_tag()
                    logger.warning(
                        'Shape tag already exists in database, creating new tag % s'
                        % new)
                    shape_list[-1].set_tag(new)
                else:
                    shape_list[-1].set_tag(shape)
                shape_list[-1].set_id(_id)
                shape_list[-1].set_uuid(_uuid)
                shape_list[-1].set_name(name)
                shape_list[-1].set_color(color)
                shape_list[-1].set_plot(enum_plot_type)
                shape_list[-1].set_attributes(attributes)
                shape_list[-1].set_coordinates(coordinates)
                shape_list[-1].set_notes(notes)
                shape_list[-1].save()
                shape_list.append(Shape(canvas))
        except KeyError:
            logger.error('Bad data in JSON file')
