'''
Created on Jun 15, 2015

@author: nqian
'''
# import antigravity
import json

import yaml
from gui.Polygon import PolygonDrawer


class PolygonReader(object):
    '''
    Reads JSON files and transfers the data into PolygonDrawer objects
    '''


    def __init__(self, fileName="C:\\Users\\nqian\\git\\CALIPSO_Visualization\\gui\\objs\\test.json"):
        '''
        Initializes attributes
        '''
        self.__fileName = fileName
        self.__data = {} 
        
    def readJSON(self):   
        with open(self.__fileName, 'r') as infile:
            data = json.load(infile)
            test = json.dumps(data, sort_keys=True,
                             indent=2, separators=(',', ': '))
#             print test
#             print data["Backscattered"]
#             print data["Depolarized"]
            yaml.safe_load(test)
#             print type(test)
        self.__data = data
    
    # TODO: add exception
    def packPolygonDrawer(self, polygonList, plotType, canvas):
        for shape in self.__data[plotType]:
            color = self.__data[plotType][shape]['color']
            vertices = self.__data[plotType][shape]['vertices']
            polygonList[-1].setColor(color)
            polygonList[-1].setVertices(vertices)
            polygonList[-1].setPlot(plotType)
            polygonList.append(PolygonDrawer(canvas))