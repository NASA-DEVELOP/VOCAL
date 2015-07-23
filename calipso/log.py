###################################
#   Created on June 29, 2015
#
#   @authors: Grant Mercer, Nathan Qian
###################################
import logging.config
import sys
import os
from constants import PATH

config = {
          'version': 1,
          'disable_existing_loggers': False,
          'formatters': {
                'logfileformatter': {
                    'format': '[%(asctime)s] [%(levelname)8s] --- %(message)s... (%(filename)s:%(lineno)s)'
                    },
                },
          'handlers': {
                'logfile': {
                    'class': 'logging.FileHandler',
                    'level': 'NOTSET',
                    'filename': 'log/trace.log',
                    'mode': 'w+',
                    'formatter': 'logfileformatter'
                    },
                'consoleHandler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'logfileformatter',
                    'level': 'NOTSET',
                    'stream': 'ext://sys.stdout'}
                },
          'loggers': {
                '': {
                     'handlers': ['logfile', 'consoleHandler'],
                     'level': 'DEBUG',
                     'propagate': True
                     }
                }
          }

def uncaught_exception(exctype, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    sys.__excepthook__(exctype, value, tb)
    
sys.excepthook = uncaught_exception
# logging.config.fileConfig(r'/home/gdev/Github/vocal/calipso/log/logging.ini',
# disable_existing_loggers=False)
logger = logging.getLogger('VOCAL')

path = PATH + '/log/logging.ini'
# logging.config.fileConfig(path, disable_existing_loggers=False)
logging.config.dictConfig(config)

if __name__ == '__main__':
    pass
