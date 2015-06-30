####################################
#    tools.py
#    @author: Grant Mercer
#    @author: Nathan Qian
#    6/3/2015
###################################
import logging

logger = logging.getLogger(__name__)

def center(toplevel, size):
    '''
    Center the window
    
    :param toplevel: Toplevel window to center
    :param size: Size dimensions in a tuple format *e.g.* ``(x,y)``
    '''
    logger.info("center")
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def byteify(inp):
    '''
    Function to convert unicode string to ASCII string
    
    :param str inp: Unicode string to be converted
    '''
    logger.info("byteify")
    if isinstance(inp, dict):
        return {byteify(key):byteify(value) for key,value in inp.iteritems()}
    elif isinstance(inp, list):
        return [byteify(element) for element in inp]
    elif isinstance(inp, unicode):
        return inp.encode('utf-8')
    else:
        return inp
    
class Observer(object):
    '''
    Class that allows signaling between classes
    '''
    def __init__(self, receiver):
        logger.info("Instantiating Observer")
        self.__receiver = receiver
        
    def update(self):
        logger.info("Update")
        self.__receiver.receive()
        
    def send(self):
        logger.info("Send")
        self.__receiver.send()
