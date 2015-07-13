#############################
# Created on Jul 2, 2015
#
# @author: nqian
#############################
from numpy import empty_like, dot, array
from math import sqrt


def get_vector(point1, point2):
    return array([point1[0] - point2[0], point1[1] - point2[1]])


def perpendicular(a):
    """
    Returns a numpy array that's orthogonal to the param
    """
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_intersection(a1, a2, b1, b2):
    """
    Retrieves the point of intersection of two lines given two points
    on each line
    :param a1, a2: Two points on the first line
    :param b1, b1: Two points on the second line
    """
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    if denom == 0:
        return
#     print "Division: ", (num / denom.astype(float))
#     print "Multiplication: ", (num / denom.astype(float)) * db
    return (num / denom.astype(float)) * db + b1


def is_intersecting(a1, a2, b1, b2):
    """
    Determines if two line segments are intersecting by checking if the point of intersection
    exists on the line segments
    :param a1, a2: The endpoints of the first line segment
    :param b1, b2: The endpoints of the second line segment
    :rtype: bool
    """
    point = get_intersection(a1, a2, b1, b2)
    # fails when non intersecting line segments orthogonal to bases 
    # i.e. when
    # a1 = array([2, 0])
    # a2 = array([2, 2])
    # b1 = array([1, 3])
    # b2 = array([3, 3])
    if point is None or \
            ((point[0] < max(min(a1[0], a2[0]), min(b1[0], b2[0]))) or
            (point[0] > min(max(a1[0], a2[0]), max(b1[0], b2[0])))):
        return False
    else:
        return True


def tuple_to_nparray(pair):
    """
    Converts a tuple to a numpy array

    :param pair: Tuple
    :rtype: nparray
    """
    return array([pair[0], pair[1]])


def nparray_to_tuple(nparray):
    """
    Converts a numpy array to a tuple

    :param nparray: Numpy array
    :rtype: (int, int)
    """
    x = nparray[0]
    y = nparray[1]
    return (x, y)

def ray_cast(coordinates, point):
    '''
    Ray cast algorithm. Checks if the point lies inside of the polygon. If the
    number of intersections is odd, the point lies inside the polygon and 
    returns true. Else, the point is outside of the polygon and returns false.
    '''
    ray_start = tuple_to_nparray((point[0], 0))
    point = tuple_to_nparray(point)
    count = 0
    for i in range(-1, len(coordinates)-1):
        # incorrect outputs from is_intersecting
        if is_intersecting(tuple_to_nparray(coordinates[i]), tuple_to_nparray(coordinates[i+1]), ray_start, point):
            count += 1
    print count
    if count % 2 == 1:
        return True
    else:
        return False

if __name__=="__main__":
    a1 = array([0, 0])
    a2 = array([2, 2])
    b1 = array([1, 4])
    b2 = array([3, 2])
    print is_intersecting(a1, a2, b1, b2)
    
    a1 = array([2, 0])
    a2 = array([2, 2])
    b1 = array([1, 3])
    b2 = array([3, 3])
    print is_intersecting(a1, a2, b1, b2)
    
    coordinates = [[732475.03126909223, 8.0858515924085701], 
                   [732475.03136109223, 8.0858515924085701], 
                   [732475.03136109223, 2.990958703266271], 
                   [732475.03126909223, 2.990958703266271]]
    point = [732475.0313150922, 5.538405147837421]
    print ray_cast(coordinates, point)