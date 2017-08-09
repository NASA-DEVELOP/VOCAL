###################################
#   Created Summer 2016
#
#
#   @author: Joseph Driscol
###################################


from ccplot.hdf import HDF
import ccplot.utils
import constants
import os

import numpy as np
from log.log import logger, error_check


class LoadData:
    """
    Loads the HDF files and replaces old functions for plotting each data type. 
    """
    def __init__(self, filename):
        logger.info("Intializing File: " + str(filename))

        # Create an empty list to hold DataSet objects corresponding to indices
        # (0 = Backscatter,  1 = Depolarization, 2 = VFM, 3 = IWP, 4 = blend, 5 = Horz Avging). See 
        # DataSet Class for more information
        self.__data_sets = []
        
        if filename == 'Empty' or filename == '':
            logger.error('File not found or not useful...')
            return

        # Check version
        if "V4" in filename:
            self.__version = "4"
        else:
            self.__version = "3"

        # Find L1 and L2 data files? come back and edit comment. This command might be redundent
        # Also the logger is reporting that no files are found when both are
        # Ensure the file is useful 
        self.find_my_file(filename)
        if self.__filenameL1 != "" and self.__filenameL2 != "":
            self.__data_level = "2"
        elif self.__filenameL2 != "":
            self.__data_level = "1"
        elif self.__filenameL1 != "":
            self.__data_level = "0"
        else:
            logger.error('File not found or not useful...')

    def get_file_name(self, levelToGet=1):
        if levelToGet == 1:
            return self.__filenameL1
        elif levelToGet == 2:
            return self.__filenameL2
        else:
            logger.error('Out of range, Suppports Level 1 and 2 data files.')
            return ""

    def find_my_file(self, in_filename=""):

        if in_filename != "":
            logger.warning('We do not have a useful file, looking for both types')
            logger.warning("This is what we got: " + str(in_filename))
            self.__filenameL1 = in_filename
            self.__filenameL2 = ""
            x = self.find_my_file()
            if x != 2:
                self.__filenameL2 = in_filename
                self.__filenameL1 = ""
            else:
                self.__filenameL1 = ""

        if self.__filenameL1 != "" and self.__filenameL2 != "":
            logger.error("Both files are loaded...")
            return 0

        if self.__filenameL1 == "":
            search_for = "L1"
            good_file = self.__filenameL2
        else:
            search_for = "L2"
            good_file = self.__filenameL1

        search_sub_name = str(good_file[-25:-4])
        if good_file.find('/') != -1:
            my_str = good_file.split("/")
            slash = "/"
        else:
            my_str = good_file.split("\\")
            slash = "\\"

        search_path = ""
        vfm = "VFM"

        for i in range(0, len(my_str)-1):
            search_path = search_path + str(my_str[i]) + str(slash)

        search_extension = "hdf"
        if constants.debug_switch > 0:
            logger.info('Searching for %s' % search_for)
            logger.info('version of %s' % search_sub_name)
            logger.info('in path: %s' % search_path)

        for root, dirs_list, files_list in os.walk(search_path):
            for file_name in files_list:
                if (file_name.find(search_sub_name) != -1 and  # Must have same name as the file we know
                            file_name.find(search_extension) != -1 and  # must be an hdf file
                            file_name.find(search_for) != -1): # Must be the level of file
                    if constants.debug_switch > 0:
                        logger.info('This file looks promising: ' + str(file_name))
                    if search_for == 'L1':
                        self.__filenameL1 = str(search_path + file_name)
                        logger.info('Found missing L1 file %s' % str(file_name))
                        if constants.debug_switch > 0:
                            logger.info('Path = %s' % search_path)
                            logger.info('File = %s' % file_name)
                            logger.info('fileNameV1 = %s' % str(self.get_file_name(1)))
                        return 1
                    elif search_for == 'L2' and file_name.find(vfm) != -1:
                        self.__filenameL2 = str(search_path + file_name)
                        logger.info('Found missing L2 file %s' % str(file_name))
                        if constants.debug_switch > 0:
                            logger.info('Path = %s' % search_path)
                            logger.info('File = %s' % file_name)

                            logger.info('fileNameV2 = %s' % str(self.get_file_name(2)))

                        return 2
                    else:
                        if constants.debug_switch > 0:
                            logger.warning('What were we looking for?')

        logger.warning('Could not find matching %s in same dir...All features may not be available' % good_file)
        return 0
