import logging.config
import sys

def uncaughtException(exctype, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
    sys.__excepthook__(exctype, value, tb)
    
sys.excepthook = uncaughtException
logger = logging.getLogger('VOCAL')    
logging.config.fileConfig('log/logging.ini', disable_existing_loggers=False)
