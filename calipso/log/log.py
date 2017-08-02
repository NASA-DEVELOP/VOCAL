###################################
#   Created on June 29, 2015
#
#   @authors: Grant Mercer, Nathan Qian
###################################
import logging.config
import re
import shutil
import sys
import traceback
from time import strftime as time
import constants
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
                    'filename': PATH + '/log/trace.log',
                    'mode': 'w+',
                    'formatter': 'logfileformatter'
                    },
                'consoleHandler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'logfileformatter',
                    'level': 'NOTSET',
                    'stream': 'ext://sys.stdout'
                    },
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
    logging.exception('{0}: {1}'.format(exctype, value))
    logging.exception(''.join(traceback.format_tb(tb)))

def error_check():
    log = PATH + '/log/trace.log'
    error = False

    with open(log) as f:
        for line in f:
            error = re.search('ERROR', line)

        if error:
            logger.info('Error found, log copied')
            copy = PATH + '/log/error' + time("%Y-%m-%d-%H-%M-%S") + '.log'
            shutil.copy(log, copy)
            return
        else:
            logger.info('No Errors found')
            return

sys.excepthook = uncaught_exception
# logging.config.fileConfig(r'/home/gdev/Github/vocal/calipso/log/logging.ini',
# disable_existing_loggers=False)
logger = logging.getLogger('VOCAL')

logging.config.dictConfig(config)

if constants.MISMATCHED_VERSION:
    logger.warning('out of date runtime files detected, attempting to open')

if __name__ == '__main__':
    pass
