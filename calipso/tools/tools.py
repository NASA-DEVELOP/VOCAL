####################################
#    tools.py
#    @author: Grant Mercer
#    @author: Nathan Qian
#    6/3/2015
###################################
import sys
import datetime

from log import logger

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
    # trouble with getting microseconds to display
    t = str(t)
    # logging.debug("Converting time: %s", t)
    t = t[:-6]
    t = datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
    ret = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond).total_seconds()
    logger.debug("Seconds %s", ret)
    return ret



class Catcher:
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
            print 'except'
            etype, value, tb = sys.exc_info()
            logger.exception('Uncaught exception: ' + str(etype) + str(value) + str(tb))
