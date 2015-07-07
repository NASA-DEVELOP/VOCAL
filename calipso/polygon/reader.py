######################################
#     Created on Jun 15, 2015
#
#     @author: nqian
######################################
# import antigravity
import ast
import json
import constants

from polygon.drawer import PolygonDrawer
from tools.tools import byteify
from log import logger


class PolygonReader(object):
    """
    Reads JSON files and transfers the data into PolygonDrawer objects

    :param str filename: Internal filename to write to
    """

    # TODO: add exception handling
    # TODO: go over possible use cases
    #            loading multiple JSONs and then saving them as one
    #            add error for corrupted or bad data
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
        
    def read_from_str_json(self, data):
        """
        Reads JSON as a string
        :param data: string representation of a JSON
        """
        self.__data = byteify(json.loads(data))
        for plt in [x for x in self.__data if x in constants.PLOTS]:
            for shape in self.__data[plt]:
                if 'coordinates' in self.__data[plt][shape]:
                    self.__data[plt][shape]['coordinates'] = \
                        [[x[0],x[1]] for x in ast.literal_eval(self.__data[plt][shape]['coordinates']) if len(x) == 2]
                if 'attributes' in self.__data[plt][shape]:
                    self.__data[plt][shape]['attributes'] = \
                        ast.literal_eval(self.__data[plt][shape]['attributes'])
                        
    def pack_shape(self, shape_list, plot_type, canvas, master):
        """
        Stores the data in the JSON into PolygonDrawers
        :param shape_list: a Python list of PolygonDrawers
        :param plot_type: the current plot being displayed
        :param canvas: a Tkinter canvas to initializes the blank PolygonDrawer in the polygonList
        :param master: an instance of Calipso to initialize the blank PolygonDrawer
        """
        try:
            for shape in self.__data[plot_type]:
                # print int(self.__data[plot_type][shape]['id']) not in [x.getID() for x in polygonList]
                entry = self.__data[plot_type][shape]['id']
                if entry is not None and int(entry) in [x.getID() for x in shape_list]: continue
                logger.info('Found data, packing polygon with JSON data')
                color = self.__data[plot_type][shape]['color']
                coordinates = self.__data[plot_type][shape]['coordinates']
                attributes = self.__data[plot_type][shape]['attributes']
                notes = self.__data[plot_type][shape]['notes']
                _id = self.__data[plot_type][shape]['id']
                shape_list[-1].setID(_id)
                shape_list[-1].setColor(color)
                shape_list[-1].setVertices(vertices)
                shape_list[-1].set_plot(plot_type)
                shape_list[-1].setAttributes(attributes)
                shape_list[-1].setCoordinates(coordinates)
                shape_list[-1].setNotes(notes)
                shape_list.append(PolygonDrawer(canvas, master))
        except KeyError:
            logger.error('Bad data in JSON file')
