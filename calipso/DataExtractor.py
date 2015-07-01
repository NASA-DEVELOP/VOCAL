'''
Created on Jul 1, 2015

@author: nqian
'''
from ccplot.hdf import HDF


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
        pass
    else:
        min_x = min(coordinates, key=lambda x: x[0])
        max_x = max(coordinates, key=lambda x: x[0])
        min_y = min(coordinates, key=lambda y: y[1])
        max_y = max(coordinates, key=lambda y: y[1])
    
def isRectangle(vertices):
    '''
    Checks of the set of vertices produces a rectangle
    '''
    if len(vertices) == 4 and (vertices[0][0] == vertices[1][0] or vertices[0][0] == vertices[2][0] or vertices[0][0] == vertices[3][0]):
        return True
    else:
        return False
    
def findIndexValues(dataset):
    '''
    Find the corresponding indices based on the given values
    '''
    pass