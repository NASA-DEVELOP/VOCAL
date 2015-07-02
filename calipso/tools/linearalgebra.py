'''
Created on Jul 2, 2015

@author: nqian
'''
from numpy import empty_like, dot, array
from math import sqrt

def getVector(point1, point2):
    return array([point1[0] - point2[0], point1[1] - point2[1]])

def perpendicular(a):
    '''
    Returns a numpy array that's orthogonal to the param
    '''
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def getIntersection(a1, a2, b1, b2):
    '''
    Retrieves the point of intersection of two lines given two points
    on each line
    :param a1, a2: Two points on the first line
    :param b1, b1: Two points on the second line
    '''
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    return (num /denom.astype(float))*db + b1

def isIntersecting(a1, a2, b1, b2):
    '''
    Determines if two line segments are intersecting by checking if the point of intersection
    exists on the line segments
    :param a1, a2: The endpoints of the first line segment
    :param b1, b2: The endpoints of the second line segment
    '''
    point = getIntersection(a1, a2, b1, b2)
    if ((point[0] < max(min(a1[0], a2[0]), min(b1[0], b2[0]))) or
        (point[0] > min(max(a1[0], a2[0]), max(b1[0], b2[0])))):
        return False
    else:
        return True
    
def tupleToNpArray(pair):
    '''
    Converts a tuple to a numpy array
    
    :param pair: Tuple
    '''
    return array([pair[0], pair[1]])
    
def npArrayToTuple(array):
    '''
    Converts a numpy array to a tuple
    
    :param array: Numpy array
    '''
    x = array[0]
    y = array[1]
    return (x, y)