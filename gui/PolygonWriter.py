'''
Created on Jun 11, 2015

@author: nqian
'''
# import antigravity
import json


class PolygonWriter(object):
    '''
    classdocs
    '''


    def __init__(self, fileName="objs/polygons.json"):
        '''
        Constructor
        '''
        self.__fileName = fileName
        self.__plotType = 0
        self.__hdf = ''
        self.__dict = {}
        
    def set(self, key, value):
#         try:
#             lst = self.__dict[key]
#             if type(value) is not list:
#                 lst.append(value)
#             else:
#                 for item in value:
#                     lst.append(item)
#         except KeyError:
#             self.__dict[key] = value
        self.__dict[key] = value
        
    def setJsonFile(self, fileName):
        self.__fileName = fileName
        
    def setPlotType(self, plotType):
        self.__plotType = plotType
        
    def setHDFFile(self, hdf):
        self.__hdf = hdf
        
    def getJsonFile(self):
        return self.__fileName
    
    def getPlotType(self):
        return self.__plotType
    
    def getHDFFile(self):
        return self.__hdf
        
    def getDictionary(self):
        return self.__dict
    
    def encode(self, data):
        with open(self.__fileName, 'w') as outfile:
            json.dump(data, outfile)
        
    def reset(self):
        for key in self.__dict:
            if key is not "HDFFile" or key is not "plotype":
                del key