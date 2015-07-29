######################################
#    Created on Jun 11, 2015
#
#    @author: nqian
#
#    Module for all constants
######################################

import os
from sys import platform as _platform

class Plot(object):
    baseplot = 0
    backscattered = 1
    depolarized = 2
    vfm = 3

plot_type_enum = {'base_plot': Plot.baseplot,
                  'backscattered': Plot.backscattered,
                  'depolarized': Plot.depolarized,
                  'vfm': Plot.vfm}

PLOTS = ['base_plot', 'backscattered', 'depolarized', 'vfm']

HEIGHT = 665
WIDTH = 1265
CHILDWIDTH = 200
CHILDHEIGHT = 350
IMPORTWIDTH = 1000
IMPORTHEIGH = 500
IMADVWIDTH = 400
IMADVHEIGHT = 230

# READ ONLY
TAGS = ['aerosol', 'aerosol LC', 'clean continental', 'clean marine', 'cloud', 'cloud LC',
        'dust', 'polluted continental', 'polluted continental dust', 'polluted dust',
        'polluted marine', 'smoke', 'stratospheric layer', 'volcanic plume',
        'polar stratospheric cloud']

OFFSET = 62

LOG_FILENAME = 'log/CALIPSO_debug.log'
HELP_PAGE = 'http://syntaf.github.io/vocal/'

TIME_VARIANCE = 0.001
ALTITUDE_VARIANCE = 0.3
PATH = os.path.dirname(os.path.realpath(__file__))

ICO = PATH + '/ico/broadcasting.ico'
if _platform == "linux" or _platform == "linux2":
    ICO = ''
    OFFSET = 41
