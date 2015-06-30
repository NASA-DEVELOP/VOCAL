######################################
#     Created on Jun 15, 2015
#
#     @author: nqian
######################################
# import antigravity
import ast
import json
import logging
import sys

import constants
from polygon.drawer import PolygonDrawer
from tools.tools import byteify


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

class PolygonReader(object):
    '''
    Reads JSON files and transfers the data into PolygonDrawer objects
    
    :param str fileName: Internal filename to write to
    '''

    # TODO: add exception handling
    # TODO: go over possible use cases
    #            loading multiple JSONs and then saving them as one
    #            add error for corrupted or bad data
    def __init__(self, fileName=""):
        '''
        Initializes attributes
        '''
        logger.info("Instantiating PolygonReader")
        self.__fileName = fileName
        self.__data = {} 
        
    def setFileName(self, fileName):
        '''
        Sets the file name destination
        :param fileName: the name of the file
        '''
        logger.info("Setting file name")
        self.__fileName = fileName
        
    def readFromFileJSON(self):   
        '''
        Reads the data from the JSON file
        '''
        logger.info("Reading from JSON file")
        with open(self.__fileName, 'r') as infile:
            data = byteify(json.load(infile))
        self.__data = data
        
    def readFromStrJSON(self, data):
        '''
        Reads JSON as a string
        :param data: string representation of a JSON
        '''
        logger.info("Reading from string as JSON")
        self.__data = byteify(json.loads(data))
        for plt in [x for x in self.__data if x in constants.PLOTS]:
            for shape in self.__data[plt]:
                if "vertices" in self.__data[plt][shape]:
                    self.__data[plt][shape]["vertices"] = \
                        [[x[0],x[1]] for x in ast.literal_eval(self.__data[plt][shape]["vertices"]) if len(x) == 2]
                if "coordinates" in self.__data[plt][shape]:
                    self.__data[plt][shape]["coordinates"] = \
                        [[x[0],x[1]] for x in ast.literal_eval(self.__data[plt][shape]["coordinates"]) if len(x) == 2]
                if "attributes" in self.__data[plt][shape]:
                    self.__data[plt][shape]["attributes"] = \
                        ast.literal_eval(self.__data[plt][shape]["attributes"])
                        
    def packPolygonDrawer(self, polygonList, plotType, canvas, master):
        '''
        Stores the data in the JSON into PolygonDrawers
        :param polygonList: a Python list of PolygonDrawers
        :param plotType: the current plot being displayed
        :param canvas: a Tkinter canvas to initializes the blank PolygonDrawer in the polygonList
        :param master: an instance of Calipso to initialize the blank PolygonDrawer
        '''
        try:
            for shape in self.__data[plotType]:
                #print int(self.__data[plotType][shape]['id']) not in [x.getID() for x in polygonList]
                entry = self.__data[plotType][shape]['id']
                if entry is not None and int(entry) in [x.getID() for x in polygonList]: continue
                color = self.__data[plotType][shape]['color']
                vertices = self.__data[plotType][shape]['vertices']
                coordinates = self.__data[plotType][shape]['coordinates']
                attributes = self.__data[plotType][shape]['attributes']
                notes = self.__data[plotType][shape]['notes']
                _id = self.__data[plotType][shape]['id']
                polygonList[-1].setID(_id)
                polygonList[-1].setColor(color)
                polygonList[-1].setVertices(vertices)
                polygonList[-1].setPlot(plotType)
                polygonList[-1].setAttributes(attributes)
                polygonList[-1].setCoordinates(coordinates)
                polygonList[-1].setNotes(notes)
                polygonList.append(PolygonDrawer(canvas, master))
                logger.info("Packed polygon with JSON data")
        except KeyError:
            logger.error("Bad data in JSON file")
