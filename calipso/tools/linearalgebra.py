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
    if ((point[0] < max(min(a1[0], a2[0]), min(b1[0], b2[0]))) or
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
    return x, y
