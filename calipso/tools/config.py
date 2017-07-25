#############################
#    Created July 21, 2017
#
#    @author Collin Pampalone
#
#############################

import json

from os.path import dirname

class ConfigFileSetting(object):
    """
    Simple class to make it easier to get file names and locations from the config file
    """
    def __init__(self, setting):
        self.__file = setting
        self.__dir = dirname(setting)

        self.__manual_setting = False

    def file(self):
        return self.__file

    def dir(self):
        return self.__dir

    def value(self):
        """ Makes it easier to iterate through a combination of config files and booleans """
        return self.__file

    def manual_setting(self):
        return self.__manual_setting

    def change(self, fl):
        if not self.__manual_setting:   # Does nothing if manual is set
            self.__file = fl
            self.__dir = dirname(fl)

    def force_change(self, fl):
        self.__file = fl
        self.__dir = dirname(fl)

    def change_manual(self, bl):
        self.__manual_setting = bl

    @staticmethod
    def get_type():
        return 'file'

class ConfigBooleanSetting(object):
    """
    Simple class to store and change booleans in the config file
    """
    def __init__(self, bl):
        self.__truefalse = bl
        self.__manual_setting = False

    def tf(self):
        return self.__truefalse

    def value(self):
        """ Makes it easier to iterate through a combination of config files and booleans """
        return self.__truefalse

    def manual_setting(self):
        return self.__manual_setting

    def change(self, bl):
        if not self.__manual_setting:  # Does nothing if manual is set
            self.__truefalse = bl

    def force_change(self, bl):
        self.__truefalse = bl

    def change_manual(self, bl):
        self.__manual_setting = bl

    @staticmethod
    def get_type():
        return 'bool'

class Config(object):
    """
    Class holds constants from config.json. These variables are set and held from one vocal session
    to another to make the ux a little smoother. Use CONF in constants.py to access the class. See
    self.get_variable_dict for adding config entries
    """
    def __init__(self, fl):
        self.__data = dict()
        self.__file = fl

        # The database that vocal opens with. This won't change unless its changed in this script
        self.default_db = ConfigFileSetting('./../../db/CALIPSOdb.db')
        # Changes whenever the user selects or creates a new database
        self.session_db = ConfigFileSetting('./../../db/CALIPSOdb.db')
        # Changes whenever a user opens a new hdf
        self.session_hdf = ConfigFileSetting('./..')
        # Changes to true after opening VOCAL 1st time
        self.opened = ConfigBooleanSetting(False)
        # True: shapes persist from one plot to the next, false: shapes appear on respective plots
        self.persistent_shapes = ConfigBooleanSetting(True)

        self.get_config()
        self.get_variables()

    ####################
    #  __init__ commands
    ####################
    def get_config(self):
        """ Loads the config file and sets it as a dictionary """
        try:
            with open(self.__file) as json_data_file:
                data = json.load(json_data_file)
                self.__data = dict(data)
        except IOError:
            # Create the config with defaults if there isn't one
            self.write_config()

    def get_variables(self):
        """ Turn all of the entries in the dictionary into variables """
        var_dict = self.get_variable_dict()
        for key, value in var_dict.iteritems():
            value.change(self.__data[key]['var_value'])
            value.change_manual(self.__data[key]['manual_setting'])

    #####
    # External Commands
    #####
    def write_config(self):
        """
        Write all of the changes to variables to the dictionary, save the dictionary as a json
        """
        var_dict = self.get_variable_dict()
        for key, value in var_dict.iteritems():
            self.__data[key] = dict()
            self.__data[key]['var_value'] = value.value()
            self.__data[key]['manual_setting'] = value.manual_setting()

        with open(self.__file, 'w') as outfile:
            json.dump(self.__data, outfile)

    def get_variable_dict(self):
        """
        Returns a dictionary of keys corresponding to keys in the config file and variables
        corresponding to the keys' respective values. To add an entry to the config, you must add an
        entry here and create the initial variable value in the __init__. Make sure to use
        descriptive keys
        """
        var_dict = {
            'default_database': self.default_db,
            'last_used_database': self.session_db,
            'last_used_hdf': self.session_hdf,
            'has_opened_before': self.opened,
            'use_persistent_shapes': self.persistent_shapes,
        }
        return var_dict
