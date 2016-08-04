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
    iwp = 4
    blend = 5
    parallel = 6
    colorratio = 8
    aerosol = 9
    not_available = 10

# DEBUG Switch Values
# Debug will eventually control the verboseness of the logger.info:
#   however, during integration testing it is very verbose
# 0 = Old versions of everything but adds printing of metadata 1064 converted to 532
# 1 = New versions of Backscatter and Depolarization +Backscatter1064
# 2 = uses non-datablock version of vfm & iwp
# 3 = Adds datablock version of vfm
# 4 = Adds datablock version of iwp
# 5 = Adds backscatter 1064
#10 = Runs the stress_test() functino as opposed to UI
debug_switch = 2

plot_type_enum = {'base_plot': Plot.baseplot,
                  'backscattered': Plot.backscattered,
                  'depolarized': Plot.depolarized,
                  'vfm': Plot.vfm,
                  'iwp': Plot.iwp,
                  'blend': Plot.blend,
                  'parallel': Plot.parallel}

PLOTS = ['base_plot', 'backscattered', 'depolarized', 'vfm','iwp','blend','parrallel]']

EFFECT_ON = {'relief': 'sunken'}
EFFECT_OFF = {'relief': 'raised'}

DATEFORMAT = '%Y-%m-%d %H:%M:%S'

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
