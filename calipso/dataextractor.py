###################################
#   Created on Jul 1, 2015
#
#   @author: Nathan Qian
###################################
import datetime
import logging
import time

from ccplot.hdf import HDF

from polygon.LinearAlgebra import getVector
from polygon.drawer import PolygonDrawer


# TODO: find out what time standard the hdf file uses
def extractData(polygonDrawer, filename):
    '''
    Extracts the data bounded by the polygon
    '''
    coordinates = polygonDrawer.getCoordinates()
    dataset = None
    
    with HDF(filename) as product:
        # TODO: check if the plot is backscatter or deploarized ratio
        dataset = product['Total_Attenuated_Backscatter_532'][::]
    
        if isRectangle(coordinates):
            min_x = min(coordinates, key=lambda x: x[0])
            max_x = max(coordinates, key=lambda x: x[0])
            min_y = min(coordinates, key=lambda y: y[1])
            max_y = max(coordinates, key=lambda y: y[1])
            logging.debug('Minimum x: %s\n\t Maximum x: %s', min_x, max_x)
            logging.debug('Minimum y: %s\n\t Maximum y: %s', min_y, max_y)
            x_indices = findIndexValues(product, min_x, max_x, product['Profile_UTC_Time'][::], debug="Time")
            y_indices = findIndexValues(product, min_y, max_y, product['metadata']['Lidar_Data_Altitudes'], debug="Altitude")
            for x in range(x_indices[0], x_indices[1]):
                for y in range(y_indices[0], y_indices[1]):
                    pass
        else:
            # TODO: algorithm if shape is not rectangular
            min_x = min(coordinates, key=lambda x: x[0])
            max_x = max(coordinates, key=lambda x: x[0])
            min_y = min(coordinates, key=lambda y: y[1])
            max_y = max(coordinates, key=lambda y: y[1])
            vectors = []
            for i in range(len(coordinates)-1):
                vectors.append(getVector(coordinates[i], coordinates[i+1]))
            
    
def isRectangle(vertices):
    '''
    Checks of the set of vertices produces a rectangle
    '''
    if len(vertices) == 4 and (vertices[0][0] == vertices[1][0] or vertices[0][0] == vertices[2][0] or vertices[0][0] == vertices[3][0]):
        return True
    else:
        return False
    
def findIndexValues(product, low, high, lst, debug=""):
    '''
    Find the corresponding indices based on the given values
    '''
    # time is ascending order
    # time is two dimensional, altitude is just one dimensional
    logging.debug('%s list type %s', debug, type(lst))
    logging.debug('Sample of %s %s', debug, lst[0])
#     logging.debug('Low in list %s', low in lst)
#     logging.debug('High in list %s', high in list)
    min_index = 0
    max_index = 0
    debug = ""
    for i in range(len(lst)):
#         try:
        lst[i][0] = timeToSeconds(lst[i][0])
        if i < 100:
            logging.debug("New time list %s", lst[i])
        if lst[i] is low:
            min_index = i
        elif lst[i] is max:
            max_index = i
#         except:
#             if lst[i] is low:
#                 min_index = i
#             elif lst[i] is max:
#                 max_index = i
    logging.debug('Min and max indices: (%s, %s)', min_index, max_index)
    return [min_index, max_index]

def timeToSeconds(t):
    logging.debug("Time entered: %s", t)
    t = str(t)[0:11]
    t = time.strptime(t, '%d%m%y.%H%M%S')
    return datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds()

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    poly = PolygonDrawer(None, None)
    lst = [(13364, 8.32803), (13376, 8.32803), (13376, 4.46656), (13364, 4.46656)]
    poly.setCoordinates(lst)
    filename = r'C:\Users\nqian\Desktop\CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf'
    extractData(poly, filename)