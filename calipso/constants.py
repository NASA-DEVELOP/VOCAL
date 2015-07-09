######################################
#    Created on Jun 11, 2015
#
#    @author: nqian
#
#    Module for all constants
######################################

from enum import Enum

class Plot(Enum):
    baseplot = 0
    backscattered = 1
    depolarized = 2
    vfm = 3

HEIGHT = 665
WIDTH = 1265
CHILDWIDTH = 200
CHILDHEIGHT = 325
IMPORTWIDTH = 1000
IMPORTHEIGH = 500

# READ ONLY
TAGS = ['aerosol', 'aerosol LC', 'clean continental', 'clean marine', 'cloud', 'cloud LC',
        'dust', 'polluted continental', 'polluted continental dust', 'polluted dust',
        'polluted marine', 'smoke', 'stratospheric layer']

LOG_FILENAME = 'log/CALIPSO_debug.log'
HELP_PAGE = 'http://syntaf.github.io/vocal/'
