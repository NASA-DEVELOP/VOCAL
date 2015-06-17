'''
Created on Jun 15, 2015

@author: nqian
'''
# import antigravity
import json

import ast
import yaml
import Constants
from gui.Polygon import PolygonDrawer

class PolygonReader(object):
    '''
    Reads JSON files and transfers the data into PolygonDrawer objects
    '''

    # TODO: add exception handling
    def __init__(self, fileName="C:\\Users\\nqian\\Documents\\Carol.json"):
        '''
        Initializes attributes
        '''
        self.__fileName = fileName
        self.__data = {} 
        
    def setFileName(self, fileName):
        self.__fileName = fileName
        
    def readFromFileJSON(self):   
        with open(self.__fileName, 'r') as infile:
            data = json.load(infile)
            test = json.dumps(data, sort_keys=True,
                             indent=2, separators=(',', ': '))
#             print data["Backscattered"]
#             print data["Depolarized"]
            yaml.safe_load(test)
#             print type(test)
        self.__data = data
        
    def readFromStrJSON(self, data):
        self.__data = (json.loads(data))
        for plt in [x for x in self.__data if x in Constants.PLOTS]:
            for shape in self.__data[plt]:
                if "vertices" in self.__data[plt][shape]:
                    self.__data[plt][shape]["vertices"] = \
                        [[x[0],x[1]] for x in ast.literal_eval(self.__data[plt][shape]["vertices"])]
                
    # TODO: add exception
    def packPolygonDrawer(self, polygonList, plotType, canvas):
        for shape in self.__data[plotType]:
            color = self.__data[plotType][shape]['color']
            vertices = self.__data[plotType][shape]['vertices']
            polygonList[-1].setColor(color)
            polygonList[-1].setVertices(vertices)
            polygonList[-1].setPlot(plotType)
            polygonList.append(PolygonDrawer(canvas))
            
