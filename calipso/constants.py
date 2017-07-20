######################################
#    Created on Jun 11, 2015
#
#    @author: nqian
#
#    Module for all constants
######################################

import os
from sys import platform as _platform
from os.path import expanduser, dirname
import json


class Config(object):
    """
    Class holds constants from config.json. These variables are set and held from one vocal session
    to another to make the ux a little smoother. Use CONF below to access the class
    """
    def __init__(self, fl):
        self.__data = dict()
        self.__file = fl

        self.default_db = None
        self.default_db_dir = None
        self.session_db = None
        self.session_db_dir = None
        self.session_hdf = None
        self.session_hdf_dir = None
        self.opened = None

        self.get_config()
        self.get_variables()

    #####
    #  __init__ commands
    ####
    def get_config(self):
        """ Loads the config file and sets it as a dictionary """
        if self.__file != '':
            with open(self.__file) as json_data_file:
                data = json.load(json_data_file)
                self.__data = dict(data)
        else:
            # Create the config with defaults if there isn't one
            self.default_db = './../db/CALIPSOdb.db'
            self.session_db = './../db/CALIPSOdb.db'
            self.session_hdf = '.'
            self.write_config()

    def get_variables(self):
        """ Turn all of the entries in the dictionary into variables """
        self.default_db = self.__data['default_database']
        self.default_db_dir = dirname(self.default_db)
        self.session_db = self.__data['last_used_database']
        self.session_db_dir = dirname(self.session_db)
        self.session_hdf = self.__data['last_used_hdf']
        self.session_hdf_dir = dirname(self.session_hdf)
        self.opened = self.__data['has_opened_before']

    #####
    # External Commands
    #####
    def write_config(self):
        """
        Write all of the changes to variables to the dictionary, save the dictionary as a json
        :return: 
        """

        self.__data['default_database'] = self.default_db
        self.__data['last_used_database'] = self.session_db
        self.__data['last_used_hdf'] = self.session_hdf
        self.__data['has_opened_before'] = 'True'
        with open(self.__file, 'w') as outfile:
            json.dump(self.__data, outfile)

class Plot(object):
    baseplot = 0
    backscattered = 1
    depolarized = 2
    vfm = 3
    iwp = 4
    horiz_avg = 5
    aerosol_subtype = 6
    colorratio = 8
    parallel = 9
    not_available = 10

# DEBUG Switch Values
# Debug will eventually control the verboseness of the logger.info:
#   however, during integration testing it is very verbose
# 99 = Old versions of everything + vfm and iwp
# 0 = New datablock
# 1 = verbose logging
#10 = Runs the stress_test() functino as opposed to UI
debug_switch = 1

plot_type_enum = {'base_plot': Plot.baseplot,
                  'backscattered': Plot.backscattered,
                  'depolarized': Plot.depolarized,
                  'vfm': Plot.vfm,
                  'iwp': Plot.iwp,
                  'horiz_avg': Plot.horiz_avg,
                  'aerosol_subtype':Plot.aerosol_subtype}

PLOTS = ['base_plot', 'backscattered', 'depolarized', 'vfm','iwp','horiz_avg','parrallel]']

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
HELP_PAGE = 'http://nasa-develop.github.io/VOCAL/developer_index.html'

TIME_VARIANCE = 0.001
ALTITUDE_VARIANCE = 0.3
PATH = '.'
HOMEPATH = expanduser('~')

# Makes a single persistent instance of the config for VOCAL to grab
CONF = Config(PATH + '/dat/config.json')

ICO = PATH + '/ico/broadcasting.ico'
if _platform == 'linux' or _platform == 'linux2':
    ICO = ''

if os.name == 'posix':
    EFFECT_ON = {'highlightbackground': 'red'}
    EFFECT_OFF = {'highlightbackground': 'white'}

# Update every term
ABOUT = \
     "VOCAL v1.17.7\nBeta build\n\n" \
     " LaRC Summer 2017 Term\n  Project Lead: Collin Pampalone"
