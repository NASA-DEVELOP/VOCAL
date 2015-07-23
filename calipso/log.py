###################################
#   Created on June 29, 2015
#
#   @authors: Grant Mercer, Nathan Qian
###################################
import logging.config
import sys
import os
from constants import PATH


def uncaught_exception(exctype, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    sys.__excepthook__(exctype, value, tb)
    
sys.excepthook = uncaught_exception
# logging.config.fileConfig(r'/home/gdev/Github/vocal/calipso/log/logging.ini',
# disable_existing_loggers=False)
logger = logging.getLogger('VOCAL')

path = PATH + '/log/logging.ini'
logging.config.fileConfig(path, disable_existing_loggers=False)

if __name__ == '__main__':
    pass
