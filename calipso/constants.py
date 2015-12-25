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

EFFECT_ON = {'relief': 'sunken'}
EFFECT_OFF = {'relief': 'raised'}

HEIGHT = 665
WIDTH = 1265
CHILDWIDTH = 200
CHILDHEIGHT = 350
IMPORTWIDTH = 1000
IMPORTHEIGH = 500
IMADVWIDTH = 400
IMADVHEIGHT = 300

TXT = 0
CSV = 1

# READ ONLY
TAGS = ['aerosol', 'aerosol LC', 'clean continental', 'clean marine', 'cloud', 'cloud LC',
        'dust', 'polluted continental', 'polluted continental dust', 'polluted dust',
        'polluted marine', 'smoke', 'stratospheric layer', 'volcanic plume',
        'polar stratospheric cloud']

LOG_FILENAME = 'log/CALIPSO_debug.log'
HELP_PAGE = 'http://syntaf.github.io/vocal/'

TIME_VARIANCE = 0.001
ALTITUDE_VARIANCE = 0.3
PATH = '.'
#PATH = os.path.dirname(os.path.realpath(__file__))

ICO = PATH + '/ico/broadcasting.ico'
if _platform == 'linux' or _platform == 'linux2':
    ICO = ''

if os.name == 'posix':
    EFFECT_ON = {'highlightbackground': 'red'}
    EFFECT_OFF = {'highlightbackground': 'white'}

ABOUT = \
     "VOCAL v0.15.2.a\nInternal development build\n\n" \
     " LaRC Spring 2015 Term\n  Project Lead: Jordan Vaa\n  Courtney Duquette\n" \
     "  Ashna Aggarwal\n\n LaRC Summer 2015 Term\n  Project Lead: Grant Mercer\n" \
     "  Nathan Qian\n\n Fall & Spring EPSCOR 2015-2016:\n  Grant Mercer"
