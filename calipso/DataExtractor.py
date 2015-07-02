'''
Created on Jul 1, 2015

@author: nqian
'''
import logging

from ccplot.hdf import HDF

from polygon.drawer import PolygonDrawer


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
            findIndexValues(product, min_x, max_x, product['Profile_UTC_Time'][::], debug="Time")
            findIndexValues(product, min_y, max_y, product['metadata']['Lidar_Data_Altitudes'], debug="Altitude")
        else:
            # TODO: algorithm if shape is not rectangular
            pass
    
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
    logging.debug('%s list type %s', debug, type(lst))
    logging.debug('Sample of %s %s', debug, lst[1])
    try:
        logging.debug('Another sample %s', lst[1][0])
    except:
        pass
    logging.debug('Dimensions: %s', len(lst.shape))
    min_index = 0
    max_index = 0
    debug = ""
    for i in range(len(lst)):
        debug += str(lst) + " "
        try:
            if lst[i][0] is low:
                min_index = i
            elif lst[i][0] is max:
                max_index = i
        except:
            if lst[i] is low:
                min_index = i
            elif lst[i] is max:
                max_index = i
    logging.debug('Min and max indices: (%s, %s)', min_index, max_index)
    return [min_index, max_index]

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    poly = PolygonDrawer(None, None)
    lst = [(2, 4), (2, 5), (7, 4), (7, 5)]
    poly.setCoordinates(lst)
    filename = r'C:\Users\nqian\Desktop\CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf'
    extractData(poly, filename)