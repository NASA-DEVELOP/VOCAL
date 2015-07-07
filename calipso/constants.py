######################################
#    Created on Jun 11, 2015
#
#    @author: nqian
#
#    Module for all constants
######################################

from enum import Enum, IntEnum

class Plot(IntEnum):
        baseplot = 0
        backscattered = 1
        depolarized = 2
        vfm = 3


class Attributes(Enum):
    aerosol = 0
    aerosol_LC = 1
    clean = 2
    continental = 3
    clean_marine = 4
    cloud = 5
    cloud_LC = 6
    dust = 7
    polluted_continental = 8
    polluted_continental_dust = 9
    polluted_dust = 10
    polluted_marine = 11
    smoke = 12
    stratospheric_layer = 13

Attributes_fromstr = {'aerosol': Attributes.aerosol,
                      'aerosol_LC': Attributes.aerosol_LC,
                      'clean': Attributes.clean,
                      'continental': Attributes.continental,
                      'clean_marine': Attributes.clean_marine,
                      'cloud': Attributes.cloud,
                      'cloud_LC': Attributes.cloud_LC,
                      'dust': Attributes.dust,
                      'polluted_continental': Attributes.polluted_continental,
                      'polluted_continental_dust': Attributes.polluted_continental_dust,
                      'polluted_dust': Attributes.polluted_dust,
                      'polluted_marine': Attributes.polluted_marine,
                      'smoke': Attributes.smoke,
                      'stratospheric_layer': Attributes.stratospheric_layer}

HEIGHT = 665
WIDTH = 1265
CHILDWIDTH = 200
CHILDHEIGHT = 325
IMPORTWIDTH = 1000
IMPORTHEIGH = 500

BASE_PLOT = 0
BACKSCATTERED = 1
DEPOLARIZED = 2
VFM = 3

FILE_NAME = 0
COLOR = 1
ATTRIBUTES = 2
CUSTOM = 3

BASE_PLOT_STR = "base_plot"
BACKSCATTERED_STR = "backscattered"
DEPOLARIZED_STR = "depolarized"
VFM_STR = "vfm"

PLOTS = ["base_plot", "backscattered", "depolarized", "vfm"]

VERTICES = "vertices"
DATE = "date"

# READ ONLY
TAGS = ['aerosol', 'aerosol LC', 'clean continental', 'clean marine', 'cloud', 'cloud LC',
        'dust', 'polluted continental', 'polluted continental dust', 'polluted dust',
        'polluted marine', 'smoke', 'stratospheric layer']

TKXMID = 629.5
TKYMID = 314

LOG_FILENAME = 'log/CALIPSO_debug.log'
