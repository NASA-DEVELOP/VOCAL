###################################
#   Created on Jul 1, 2015
#
#   @author: Nathan Qian
###################################
from ccplot.hdf import HDF
from tools.linearalgebra import getVector
from polygon.drawer import PolygonDrawer

import datetime
import logging
import time


# TODO: find out what time standard the hdf file uses
def extract_data(polygon_drawer, fname):
    """
    Extracts the data bounded by the polygon
    """
    coordinates = polygon_drawer.getCoordinates()
    
    with HDF(fname) as product:
        # TODO: check if the plot is backscatter or deploarized ratio
        # dataset = product['Total_Attenuated_Backscatter_532'][::]
    
        if is_rectangle(coordinates):
            min_x = min(coordinates, key=lambda mx: mx[0])
            max_x = max(coordinates, key=lambda ax: ax[0])
            min_y = min(coordinates, key=lambda my: my[1])
            max_y = max(coordinates, key=lambda ay: ay[1])
            logging.debug('Minimum x: %s\n\t Maximum x: %s', min_x, max_x)
            logging.debug('Minimum y: %s\n\t Maximum y: %s', min_y, max_y)
            x_indices = find_idx_values(product, min_x, max_x, product['Profile_UTC_Time'][::], debug='Time')
            y_indices = \
                find_idx_values(product, min_y, max_y, product['metadata']['Lidar_Data_Altitudes'], debug='Altitude')
            for x in range(x_indices[0], x_indices[1]):
                for y in range(y_indices[0], y_indices[1]):
                    pass
        else:
            # TODO: algorithm if shape is not rectangular
            # min_x = min(coordinates, key=lambda x: x[0])
            # max_x = max(coordinates, key=lambda x: x[0])
            # min_y = min(coordinates, key=lambda y: y[1])
            # max_y = max(coordinates, key=lambda y: y[1])
            vectors = []
            for i in range(len(coordinates)-1):
                vectors.append(getVector(coordinates[i], coordinates[i+1]))
            
    
def is_rectangle(vertices):
    """
    Checks of the set of vertices produces a rectangle
    """
    if len(vertices) == 4 and (vertices[0][0] == vertices[1][0] or
                               vertices[0][0] == vertices[2][0] or
                               vertices[0][0] == vertices[3][0]):
        return True
    else:
        return False


def find_idx_values(product, low, high, p_lst, debug=''):
    """
    Find the corresponding indices based on the given values
    """
    # time is ascending order
    # time is two dimensional, altitude is just one dimensional

    logging.debug('%s list type %s', debug, type(p_lst))
    logging.debug('Sample of %s %s', debug, p_lst[0])
#     logging.debug('Low in list %s', low in lst)
#     logging.debug('High in list %s', high in list)
    min_index = 0
    max_index = 0
#    debug = ''
    for i in range(len(p_lst)):
        # try:
        p_lst[i][0] = time_to_seconds(p_lst[i][0])
        if i < 100:
            logging.debug('New time list %s', p_lst[i])
        if p_lst[i] is low:
            min_index = i
        elif p_lst[i] is max:
            max_index = i
#         except:
#             if lst[i] is low:
#                 min_index = i
#             elif lst[i] is max:
#                 max_index = i
    logging.debug('Min and max indices: (%s, %s)', min_index, max_index)
    return [min_index, max_index]


def time_to_seconds(t):
    logging.debug('Time entered: %s', t)
    t = str(t)[0:11]
    t = time.strptime(t, '%d%m%y.%H%M%S')
    return datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    poly = PolygonDrawer(None, None)
    lst = [(13364, 8.32803), (13376, 8.32803), (13376, 4.46656), (13364, 4.46656)]
    poly.setCoordinates(lst)
    filename = r'C:\Users\nqian\Desktop\CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf'
    extract_data(poly, filename)