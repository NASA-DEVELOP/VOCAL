#############################
# Created on Jul 2, 2015
#
# @author: nqian
#############################
from math import sqrt

from numpy import empty_like, dot, array


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
    """
    Find the distance between two points on an arbitrary scale

    :param x1: x coordinate 1
    :param y1: y coordinate 1
    :param x2: x coordinate 2
    :param y2: y coordinate 2

    :rtype: float
    """
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def is_in_segment(a, b, c):
    """
    Checks if the passed numpy arrays are in the segment

    :param a: numpy array of first endpoint of the line segment
    :param b: numpy array second endpoint of the line segment
    :param c: numpy array of the tested point
    """
    cross_product = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    if abs(cross_product) > 0.00001:
        return False
    dot_product = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
    if dot_product < 0:
        return False
    length2_ba = (b[0] - a[0])**2 + (b[1] - a[1])**2
    if dot_product > length2_ba:
        return False
    return True


def get_intersection(a1, a2, b1, b2):
    """
    Retrieves the point of intersection of two lines given two points
    on each line

    :param a1, a2: Two points on the first line
    :param b1, b1: Two points on the second line
    """
    # source of algorithm: http://stackoverflow.com/questions/3252194/numpy-and-line-intersections
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perpendicular(da)
    denom = dot(dap, db)
    num = dot(dap, dp)
    # if denom is 0, the line segments are parallel
    if denom == 0:
        return
    return (num / denom.astype(float)) * db + b1


def is_intersecting(a1, a2, b1, b2):
    """
    Determines if two line segments are intersecting by checking if the point of intersection
    exists on the line segments

    :param a1, a2: The endpoints of the first line segment
    :param b1, b2: The endpoints of the second line segment
    :rtype: :py:class:`bool`
    """
    point = get_intersection(a1, a2, b1, b2)
    # original check from: http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    if point is None or \
          (not is_in_segment(a1, a2, point) or 
           not is_in_segment(b1, b2, point)):
        return False
    else:
        return True


def tuple_to_nparray(pair):
    """
    Converts a tuple to a numpy array

    :param pair: Tuple
    :rtype: :py:class:`numpy.array`
    """
    return array([pair[0], pair[1]])


def nparray_to_tuple(nparray):
    """
    Converts a numpy array to a tuple

    :param nparray: Numpy array
    :rtype: (:py:class:`int`, :py:class:`int`)
    """
    x = nparray[0]
    y = nparray[1]
    return x, y


def ray_cast(coordinates, point):
    """
    Ray cast algorithm. Checks if the point lies inside of the polygon. If the
    number of intersections is odd, the point lies inside the polygon and
    returns true. Else, the point is outside of the polygon and returns false.

    :rtype: :py:class:`bool`
    """
    ray_start = tuple_to_nparray((point[0], 0))
    point = tuple_to_nparray(point)
    count = 0
    for i in range(-1, len(coordinates)-1):
        if is_intersecting(tuple_to_nparray(coordinates[i]), tuple_to_nparray(coordinates[i+1]), ray_start, point):
            count += 1
    if count % 2 == 1:
        return True
    else:
        return False
