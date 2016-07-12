####################################
#    tools.py
#    @author: Grant Mercer
#    @author: Nathan Qian
#    6/3/2015
###################################
import sys
import ast
from datetime import datetime
import os
import matplotlib as mpl
import numpy as np
from log.log import logger

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def center(toplevel, size):
    """
    Center the window

    :param toplevel: Toplevel window to center
    :param size: Size dimensions in a tuple format *e.g.* ``(x,y)``
    """
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry('%dx%d+%d+%d' % (size[0], size[1], x, y))


def format_coord(axes, x, y, z):
    """
    Return a format string formatting the *x*, *y* coord
    """
    if x is None:
        xs = '???'
    else:
        xs = axes.format_xdata(x)
    if y is None:
        ys = '???'
    else:
        ys = axes.format_ydata(y)
    if z is None:
        zs = '???'
    else:
        zs = z
    return 'x=%s y=%s lat=%s' % (xs, ys, zs)

def coord_tuple_list(uni_str):
    """
    Takes as input Unicode string that ought to be list of tuples
    and returns an actual list of tuples (used in coordinate formatting)

    :param str inp: Unicode string to be converted
    """
    coords = uni_str.strip("[")
    coords = coords.strip("]")
    coords = coords.split(",")
    temp_list = [b.replace("(",'') for b in coords]
    temp_list2 = [b.replace(")",'') for b in temp_list]
    
    convert_list = list()
    for c in temp_list2:
        c = np.float64(c)
	convert_list.append(c)
    temp_iter = iter(convert_list)
    tup_coords = zip(temp_iter, temp_iter)

    time_list = [mpl.dates.num2date(x[0]).strftime('%H:%M:%S') for x in tup_coords]
    for i, (a, b) in enumerate(tup_coords):
        tup_coords[i] = (time_list[i], b)
    final_coord_list = ['(%s, %.3f)' % (a, b) for a, b in tup_coords]
    return final_coord_list



def byteify(inp):
    """
    Function to convert unicode string to ASCII string

    :param str inp: Unicode string to be converted
    """
    if isinstance(inp, dict):
        return {byteify(key): byteify(value) for key, value in inp.iteritems()}
    elif isinstance(inp, list):
        return [byteify(element) for element in inp]
    elif isinstance(inp, unicode):
        return inp.encode('utf-8')
    else:
        return inp


def time_to_seconds(t):
    """
    Convert a time string into a strings containing only seconds

    :param str t: time in *%Y-%m-%d %H:%M:%S.%f* format
    :rtype: :py:class:`str`
    """
    t = str(t)
    t = t[:-6]
    t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
    ret = datetime.timedelta(hours=t.hour, minutes=t.minute,
                             seconds=t.second, microseconds=t.microsecond).total_seconds()
    logger.debug("Seconds %s", ret)
    return ret


def in_time_range(t1, t2):
    return True


def in_lat_range(l1, l2):
    return True


def in_alt_range(a1, a2):
    return True


def get_shape_ranges(coordinates):
    """
    Given the list of coordinates , return a tuple containing formatted strings for
    the range of time and altitude

    :param list coordinates: The list of coordinates to determine the ranges from

    :rtype: (:py:class:`str`, :py:class:`str`)
    """
    cords = ast.literal_eval(coordinates)
    time_cords = [mpl.dates.num2date(x[0]).strftime('%H:%M:%S %p') for
                  x in cords]
    altitude_cords = [x[1] for x in cords]
    start_date = mpl.dates.num2date(cords[0][0]).strftime('%Y-%m-%d')

    return '%s, %s - %s' % (start_date, min(time_cords), max(time_cords)), \
           '%07.4f km - %07.4f km' % (min(altitude_cords), max(altitude_cords))


def interpolation_search(sorted_list, to_find, variance):
    """
    Interpolation  search algorithm for determining the location of the
    point according to sorted_list, the sorted_list has a constant step
    and can thus give this algorithm the complexity of just ``O(log log(n))``

    :param list sorted_list: The sorted list to search in
    :param float to_find: The point to find
    :param float variance: A constant variance allowed for finding the point

    :rtype: float
    """
    low = 0
    high = len(sorted_list) - 1

    while sorted_list[low] <= to_find <= sorted_list[high]:
        mid = (low + ((to_find - sorted_list[low]) * (high - low))
               / (sorted_list[high] - sorted_list[low]))

        if sorted_list[mid] < to_find:
            low = mid + 1
        elif sorted_list[mid] > to_find:
            high = mid - 1
        else:
            return mid
    t_var = variance
    while abs(sorted_list[low] - to_find) > variance:
        t_var += .001
    if variance != t_var:
        logger.warning("interpolation variance expanded to %f to meet requirements"
                       % variance)
    logger.debug("Interpolation low: %s", low)
    return low


def zipdir(path, ziph):
    """
    Zip the contents of a directory into the ZipFile object ziph,
    walks through the directory entered and will copy all files to
    the BASE directory of the ZipFile

    :param str path: The path of the folder to zip
    :param ZipFile ziph: A :py:class:`ZipFile` object
    """
    for root, dirs, files in os.walk(path):
        for file_ in files:
            ziph.write(os.path.join(root, file_), file_)


class Observer(object):
    """
    Observer pattern class for notifying remote partners of changes
    in data. This is a **base class*, so this *must* be inherited from
    as Observer doesn't actually contain any data, just the tools for
    notifying.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """
        Attach a parent to the observer, this will be notifid upon any changes
        made in the observer

        :param observer: The class you want to notify
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detach a parent from the observer, if you no longer wish to notify anymore

        :param observer: Detach an existing class
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        """
        Called when a a field is changed inside of the class inheriting Observer
        """
        for observer in self._observers:
            if modifier != observer:
                observer.receive(self)


class Catcher:
    """
    A Tkinter overloaded class for forwarding the exception output
    directly to the log
    """
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    # noinspection PyBroadException
    def __call__(self, *args):
        try:
            if self.subst:
                args = apply(self.subst, args)
            return apply(self.func, args)
        except SystemExit, msg:
            raise SystemExit(msg)
        except:
            etype, value, tb = sys.exc_info()
            logger.exception('Uncaught exception: ' + str(etype) + str(value) + str(tb))
