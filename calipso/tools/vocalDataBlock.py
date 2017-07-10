###################################
#   Created Summer 2016
#	
#
#   @author: Joseph Driscol
###################################

from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils
from plot.interpret_vfm_type import extract_type, extract_water_phase
from plot.vfm_row2block import vfm_row2block
from plot.findLatIndex import findLatIndex
import constants
import os

import numpy as np
from plot.avg_lidar_data import avg_horz_data
from plot.uniform_alt_2 import uniform_alt_2
from plot.regrid_lidar import regrid_lidar
from log.log import logger, error_check


class MetaData:
    """
    MetaData objects allow the transfer of rendering range and type info to and from Calipso and
    VocalDataBlock. The functions allow the code to call or set the current variables
    """
    def __init__(self, in_type=0, in_x_min=0, in_x_max=0, in_y_min=0, in_y_max=0, in_wavelength=532):
        self.__type = in_type                 # Type of plot (0 = backscatter, 1 = depolarization...)
        self.__x = [in_x_min, in_x_max]        # The x axis range (nominal units)
        self.__y = [in_y_min, in_y_max]        # The y axis range (in altitude)
        self.__wavelength = in_wavelength    # The wavelength the user wants (532 or 1064)

    def set_meta_type(self,in_type):
        if 0 <= in_type < 10:
            self.__type = in_type
            logger.info("Setting data type to " + str(in_type))

    def get_meta_type(self):
        return self.__type

    def set_meta_wavelength(self,in_wavelength):
        if in_wavelength == 532 or in_wavelength == 1064:
            self.__wavelength = in_wavelength
        else:
            self.__wavelength = 532

    def get_meta_wavelength(self):
        return self.__wavelength

    def set_meta_x(self,in_x=[0,15000]):
        if in_x[0] < in_x[1] and in_x[1]-in_x[0] >= 5:
            if in_x[0] % 5 == 0:
                self.__x[0] = in_x[0]
            else:
                self.__x[0] = in_x[0] - (in_x[0]%5)
            if in_x[1] % 5 == 0:
                self.__x[1] = in_x[1]
            else:
                self.__x[0] = in_x[0] + 5 - (in_x[0] % 5)
        else:
            logger.error('meta x is out of range')
            logger.info('Index Error')

    def set_meta_y(self, in_y=[0, 20]):
        if in_y[0] < in_y[1] and in_y[1] - in_y[0] >= 5 and in_y[1] <= 30:
            self.__y = in_y
        else:
            logger.error('meta y is out of range')
            logger.info('Index Error')

    def get_meta_x(self, it):
        if it == 0 or it == 1:
            return self.__x[it]
        elif it == 2:
            return self.__x
        else:
            logger.info('Index Error')

    def get_meta_y(self, it):
        if it == 0 or it == 1:
            return self.__y[it]
        elif it == 2:
            return self.__y
        else:
            logger.info('Index Error')

class DataSet:
    """
    Class of objects that contain data loaded from HDF files
    """

    def __init__(self, in_type, in_data_set, in_x_range=[0,5000], in_y_range=[0,20], in_wavelength=532):
        self.ds_type = int(in_type)            # Type of data (1 = backscatter, 2 = depolarization, etc.)
        self.ds_wavelength = in_wavelength    # Wavelength of the data (532 or 1064)
        self.ds_data_set = in_data_set         # The 2d block of data, i.e. the collection of profiles
        self.__ds_xrange = in_x_range        # The horizontal range we load in profiles, or vertical columns            
        self.ds_yrange = in_y_range            # The vertical range we load in altitude
        self.ds_x_label = 'Latitude'        # Lables for the plots
        self.ds_x_label2 = 'Time'
        self.ds_y_label = 'Altitude (km)'

        self.ds_cbar_label = ''
        self.ds_title = ''
        self.set_title()

    def ds_set_x(self, in_xrange):
        """
        Verify that a correct x rangee was put in, and prepare it for use later
        Not sure why it has to be a multiple of 5
        """
        if 0 <= in_xrange[0] < in_xrange[1] <= 15000 and in_xrange[0]+5 <= in_xrange[1]:
            if in_xrange[0] % 5 != 0:
                self.__ds_xrange[0] = int(in_xrange[0] - (in_xrange[0] % 5))
            if in_xrange[1] % 5 != 0:
                self.__ds_xrange[1] = int((in_xrange[1] - (in_xrange[1] % 5)))
        else:
            logger.warning('xrange is not in the correct format for dataset, setting to 0-5000')
            self.__ds_xrange = [0, self.ds_data_set.shape[0]-1]
        if constants.debug_switch > 0:
            logger.info('Data Set x range Translated from ' + str(in_xrange) + ' to ' + str(self.__ds_xrange))

    def ds_get_x(self,in_it):
        """
        Return either the start, end, or full x range 
        """
        if in_it == 0:
            return self.__ds_xrange[0]
        elif in_it == 1:
            return self.__ds_xrange[1]
        elif in_it == 2:
            return self.__ds_xrange
        else:
            logger.error("Incorrect iterator received by in_it")

    def set_title(self):
        """
        Sets the title and colorbar lables
        """
        if self.ds_type == 1:
            self.ds_title = 'Averaged ' + str(self.ds_wavelength) + 'nm Total Attenuated Backscatter'
            self.ds_cbar_label = 'Total Attenuated Backscatter ' \
                                  + str(self.ds_wavelength) + ' nm (km$^{-1}$ sr$^{-1}$)'
        elif self.ds_type == 2:
            self.ds_title = 'Averaged ' + str(self.ds_wavelength) + 'nm Depolarized Ratio'
            self.ds_cbar_label = 'Depolarized Ratio  ' \
                                  + str(self.ds_wavelength) + ' nm (km$^{-1}$ sr$^{-1}$)'
        elif self.ds_type == 3:
            self.ds_title = 'Vertical Feature Mask'
            self.ds_cbar_label = 'Vertical Feature Mask Flags'
        elif self.ds_type == 4:
            self.ds_title = 'Ice Water Phase'
            self.ds_cbar_label = 'Ice Water Phase Flags'
        elif self.ds_type == 5:
            self.ds_title = 'Horizontal Averaging'
            self.ds_cbar_label = 'Horizontal Averaging Flags'
        elif self.ds_type == 6:
            self.ds_title = ''
            self.ds_cbar_label = ''
        elif self.ds_type == 7:
            self.ds_title = ''
            self.ds_cbar_label = ''
        elif self.ds_type == 8:
            self.ds_title = ''
            self.ds_cbar_label = ''
        elif self.ds_type == 9:
            self.ds_title = ''
            self.ds_cbar_label = ''
        elif self.ds_type == 10:
            self.ds_title = ''
            self.ds_cbar_label = ''

    def get_ds_type(self):
        """
        Returns the type of data
        """
        return self.ds_type

class VocalDataBlock:
    """
    Loads the HDF files and replaces old functions for plotting each data type. 
    """
    def __init__(self, filename):
        logger.info("Intializing File: " + str(filename))
        self.__working_meta = MetaData()
        
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

        # Loads some necessary parts of the data held in the L1 HDF 
        with HDF(self.__filenameL1) as product:
            # 1D array of tmes for each profile in yymmdd.ffffffff
            self.__x_time = product['Profile_UTC_Time'][::, 0]
            self.__x_time = np.array([ccplot.utils.calipso_time2dt(t) for t in self.__x_time])

            # Number of profiles
            self.__record_count = len(self.__x_time)

            # 1D array of sample altitudes
            self.__y_altitude = np.array(product['metadata']['Lidar_Data_Altitudes'][::])

            # 1D array of profile longitudes
            self.__Longitude = np.array([product['Longitude'][::, 0]])
            self.__Longitude = np.array(self.__Longitude[0][::])

            # 1D array of profile latitudes
            self.__Latitude = np.array([product['Latitude'][::, 0]])
            self.__Latitude = np.array(self.__Latitude[0][::])

            # A 2D, 2 row array that lists longitude on top of the corresponding latitude
            self.__x_coordinates = np.array([self.__Longitude, self.__Latitude])

            # 1D array that lists either day or night
            self.__day_night_flag = np.array(product['Day_Night_Flag'][::])



    """Following is simple setters/getters associated with VocalDataBlock Class"""
    """Returns Shapes of time Array"""
    def get_time_shape(self):
        return np.shape(self.__x_time)

    """Returns Shapes of latitude Array"""
    def get_latitude_shape(self):
        return np.shape(self.__Latitude)

    """Returns Shapes of altitude Array"""
    def get_altitude_shape(self):
        return np.shape(self.__y_altitude)

    '''***Getters for y (Alititude***'''
    '''Get the altitude at iterator "in_y"'''
    def get_altitude(self, in_y):
        if -1 <= in_y < len(self.__y_altitude)-1:
            return self.__y_altitude[in_y]
        else:
            return 0
            logger.info('Index Error')

    def get_time(self, in_x):
        if -1 <= in_x <= self.__record_count-1:
            return self.__x_time[in_x]
        else:
            logger.info('Index Error')

    # return the value at the iterator (in_x) from the coordinates list -- returns Coordinate pair [long, lat]
    def get_coordinates(self, in_x):
        if -1 <= in_x < self.__record_count-1:
            return [self.get_longitude(in_x),self.get_latitude(in_x)]
        else:
            return [0,0]
            logger.info('Index Error')

    # return the value at the iterator (in_x) from the coordinates list -- returns Coordinate pair [long, lat]
    def get_latitude(self, in_x):
        if -1 <= in_x < self.__record_count-1:
            return self.__Latitude[in_x]
        else:
            return 0
            logger.info('Index Error')

    # return the value at the iterator (in_x) from the coordinates list -- returns Coordinate pair [long, lat]
    def get_longitude(self, in_x):
        if -1 <= in_x < self.__record_count-1:
            return self.__Longitude[in_x]
        else:
            return 0
            logger.info('Index Error')

    def get_y_min(self, in_iterator, in_type='iterator'):
        if in_type == 'iterator':
            return self.__data_sets[in_iterator].ds_yrange[0]
        elif in_type == 'altitude':
            return self.__y_altitude[self.__data_sets[in_iterator].ds_yrange[0]]
        else:
            return 0

    def get_y_max(self, in_iterator, in_type='iterator'):
        if in_type == 'iterator':
            return self.__data_sets[in_iterator].ds_yrange[1]
        elif in_type == 'altitude':
            return self.__y_altitude[self.__data_sets[in_iterator].ds_yrange[1]]
        else:
            return 0

    def get_x_min(self, in_iterator, in_type='iterator'):
        """
        Returns the minimum x value for a given data type (iter, lat, lon, time, %)
        for a given iterator in __data_sets
        """
        if in_type == 'iterator':
            return self.__data_sets[in_iterator].ds_get_x(0)
        elif in_type == 'latitude':
            return self.__Latitude[self.__data_sets[in_iterator].ds_get_x(0)]
        elif in_type == 'longitude':
            return self.__Longitude[self.__data_sets[in_iterator].ds_get_x(0)]
        elif in_type == 'time':
            return self.__x_time[self.__data_sets[in_iterator].ds_get_x(0)]
        else:
            return 0

    def get_x_max(self, in_iterator, it_type='iterator'):
        if it_type == 'iterator':
            return self.__data_sets[in_iterator].ds_get_x(1)
        elif it_type == 'latitude':
            return self.__Latitude[self.__data_sets[in_iterator].ds_get_x(1)]
        elif it_type == 'longitude':
            return self.__Longitude[self.__data_sets[in_iterator].ds_get_x(1)]
        elif it_type == 'time':
            return self.__x_time[self.__data_sets[in_iterator].ds_get_x(1)]
        else:
            return 0

    def get_data_set_type(self, in_iterator):
        return self.__data_sets[in_iterator].get_ds_type()

    def get_data_set(self, in_iterator, transpose='none'):
        if transpose == 'transpose':
            return self.__data_sets[in_iterator].ds_data_set.T
        else:
            return self.__data_sets[in_iterator].ds_data_set

    def get_data_set_x_label(self, in_iterator):
        return self.__data_sets[in_iterator].ds_x_label

    def get_data_set_x_label2(self, in_iterator):
        return self.__data_sets[in_iterator].ds_x_label2

    def get_data_set_y_label(self, in_iterator):
        return self.__data_sets[in_iterator].ds_y_label

    def get_data_set_title(self, in_iterator):
        return self.__data_sets[in_iterator].ds_title

    def get_data_set_cbar_label(self, in_iterator):
        return self.__data_sets[in_iterator].ds_cbar_label

    def get_alt_latitude(self, in_i):
        latitude1 = self.__Latitude[self.get_x_min(in_i):self.get_x_max(1)]
        latitude2 = latitude1[::15]
        return [latitude2[0],latitude2[-1]]

    def get_file_name(self, levelToGet=1):
        if levelToGet == 1:
            return self.__filenameL1
        elif levelToGet == 2:
            return self.__filenameL2
        else:
            logger.error('Out of range, Suppports Level 1 and 2 data files.')
            return ""

    # sets the working type as an integer - refer to constants.py for dictionary
    def set_working_type(self, in_type):
        if in_type >= 0 or in_type < 11:
            self.__working_meta.set_meta_type(in_type)
        else:
            logger.info('Index Error')

    # Accepts a 2-element list of integers for the x range of profiles
    def set_working_x(self, in_x):
        if 0 <= in_x[0] < in_x[1]  and in_x[1] - in_x[0] <= 15000:
            self.__working_meta.set_meta_x(in_x)
        else:
            logger.info('Index Error')

    # This allows the setting of the wavelength as some data_sets have 532 and 1064 wavelengths.
    #   The default is always 532
    def set_working_wavelength(self, in_wavelength):
        if in_wavelength == '1064':
            self.__working_meta.set_meta_wavelength(1064)
        else:
            self.__working_meta.set_meta_wavelength(532)

    # accepts a 2-element list of integers - This is the y range (altitude) for a new data_set based off the working data_set
    def set_working_altitude(self, in_altitude):
        if 0 <= in_altitude[0] < in_altitude[1] and in_altitude[1] - in_altitude[0] <= len(self.__y_altitude):
            self.__working_meta.set_meta_y(in_altitude)
        else:
            logger.info('Index Error')

    def set_working_meta(self, in_meta_data):
        self.set_working_type(in_meta_data.get_meta_type())
        self.set_working_x(in_meta_data.get_meta_x(2))
        self.set_working_altitude(in_meta_data.get_meta_y(2))
        self.set_working_wavelength(in_meta_data.get_meta_wavelength())

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

    def print_working_metadata(self):
        logger.info("*********************************************")
        logger.info("***************BEGIN META DATA***************")
        logger.info("Working MetaData:")
        logger.info("Level 1 Filename: %s" % str(self.__filenameL1))
        logger.info("Level 2 Filename: %s" % str(self.__filenameL2))
        if self.__data_level == 2:
            logger.info("Level 1 and Level 2 data available...")
        elif self.__data_level == 1:
            logger.info("ONLY Level 2 data available...")
        elif self.__data_level == 1:
            logger.info("ONLY Level 1 data available...")
        else:
            logger.info("No data available...or at least it will be tempermental")
        logger.info("*********SHAPE OF META DATA***********")
        logger.info("X Time Shape: %s" % str(np.shape(self.__x_time)))
        logger.info("X Latitude Shape: %s" % str(np.shape(self.__Latitude)))
        logger.info("X Longitude Shape: %s" % str(np.shape(self.__Latitude)))
        logger.info("Y Shape: %s" % str(self.__y_altitude.shape))
        logger.info("*********WORKING META DATA***********")
        logger.info("Type = %s" % str(self.__working_meta.get_meta_type()))
        logger.info("X-Working Min/Max in %: " + str(self.__working_meta.get_meta_x(0)) + ", " +
                    str(self.__working_meta.get_meta_x(1)))
        logger.info("Y-Working Min/Max in km: " + str(self.__working_meta.get_meta_y(0)) + ", " +
                    str(self.__working_meta.get_meta_y(1)))
        logger.info("*********MIN/MAX VALUES of DATA SET***********")
        logger.info("X-range Time will be, Min: " + str(self.get_time(0)) + " Max: " +str(self.get_time(-1)))
        logger.info("X-range Coords will be, Min: " + str(self.get_coordinates(0)) + " Max: " +
                    str(self.get_coordinates(-1)))
        logger.info("Y-range Altitude will be, Min: " + str(self.get_altitude(0)) + " Max: " +
                    str(self.get_altitude(-1)))
        logger.info("***************END META DATA*****************")
        logger.info("*********************************************")

    def print_data_set_info(self, in_iterator):
        logger.info("*********************************************")
        logger.info("***************BEGIN DATA SET****************")
        logger.info("Type: %s" % str(self.get_data_set_type(in_iterator)))
        logger.info("Iterator: %s" % str(in_iterator))
        logger.info("Data Shape: %s" % str(np.shape(self.__data_sets[in_iterator].ds_data_set)))
        logger.info("********************")
        logger.info("Real Iterators for x1, x2, y1, y2: (" +
            str(self.get_x_min(in_iterator, 'profile')) + ", " +
            str(self.get_x_max(in_iterator, 'profile')) + ", " +
            str(self.get_y_min(in_iterator, 'profile')) + ", " +
            str(self.get_y_max(in_iterator, 'profile')) +
        ")")
        logger.info("********************")
        logger.info("Data Set Iterators for x1, x2, y1, y2: (" +
            str(self.get_x_min(in_iterator, 'iterator')) + ", " +
            str(self.get_x_max(in_iterator, 'iterator')) + ", " +
            str(self.get_y_min(in_iterator, 'iterator')) + ", " +
            str(self.get_y_max(in_iterator, 'iterator')) +
        ")")
        logger.info("********************")
        logger.info("Time Values: " +
                    str(self.get_x_min(in_iterator, 'time')) + ", " +
                    str(self.get_x_max(in_iterator, 'time')))
        logger.info("Latitude Values: " +
                    str(self.get_x_min(in_iterator, 'latitude')) + ", " +
                    str(self.get_x_max(in_iterator, 'latitude')))
        logger.info("Longitude Values: " +
                    str(self.get_x_min(in_iterator, 'longitude')) + ", " +
                    str(self.get_x_max(in_iterator, 'longitude')))
        logger.info("Altitude Values: " +
                    str(self.get_y_min(in_iterator, 'altitude')) + ", " +
                    str(self.get_y_max(in_iterator, 'altitude')))
        logger.info("***************END DATA SET******************")
        logger.info("*********************************************")

    """
    This will find the iterator for the working data_set within the data_set.  It can also be used 
    to check to see if the working data_set has already been created or if the list is empty return
    codes ('empty' == empty, "False" == does not exist in data_set, positive integer is a positive
    match and returns the iterator needed to access the data_set and negative interger is an 
    iterator pointing to a data_set that the working data_set exists within
    """
    def find_data_set_iterator(self,in_type=-1, in_wavelength=532):
        if in_type == -1:
            in_type = self.__working_meta.get_meta_type()
        if in_wavelength != 1064:
            in_wavelength = 532
        if len(self.__data_sets) == 0:
            logger.warning('DATA SET IS EMPTY')
            return "Empty"
        else:
            for i in range(0, len(self.__data_sets)):
                if self.__data_sets[i].ds_type == in_type and self.__data_sets[i].ds_wavelength == in_wavelength:
                    logger.info('DATA SET FOUND: ' + str(i))
                    return i
        logger.warning('DATA SET NOT FOUND')
        return "False"


    def load_data_set(self, in_data_set_to_get, in_return_type='none'):
        if in_return_type == 'none':
            data_set_iterator = self.find_data_set_iterator(self.__working_meta.get_meta_type())
        else:
            data_set_iterator = "False"

        filename = ""
        if data_set_iterator == "False" or data_set_iterator == "Empty":
            if self.__working_meta.get_meta_type() == 3 or self.__working_meta.get_meta_type() == 4:
                filename = self.__filenameL2
            else:
                filename = self.__filenameL1

            if filename == "":
                logger.error('Data file not available')
                return -99
            else:
                if constants.debug_switch > 0:
                    logger.info('Attempting to open data set: ' + str(in_data_set_to_get))
                    logger.info('From File: ' + str(filename))

                with HDF(filename) as product:
                    if constants.debug_switch > 0:
                        logger.info("Loading data set: " + str(in_data_set_to_get))
                        logger.info("From: " + str(filename))
                    temp_data = product[in_data_set_to_get][::]

            if in_return_type == 'data only':
                return temp_data
            else:
                return self.append_data_sets(temp_data)
        else:
            if in_return_type == 'data only':
                return self.get_data_set(data_set_iterator)
            else:
                return data_set_iterator

    def append_data_sets(self, in_data_set):
        """
        Appends a DataSet to the end of __data_sets
        """
        self.__data_sets.append(DataSet(
            self.__working_meta.get_meta_type(), in_data_set,
            self.__working_meta.get_meta_x(2),
            self.__working_meta.get_meta_y(2),
            self.__working_meta.get_meta_wavelength()
        ))
        if constants.debug_switch > 0:
            logger.info('*****************Loaded data set****************')
            self.print_working_metadata()
            self.print_data_set_info(len(self.__data_sets) - 1)

        return len(self.__data_sets) - 1

    def remove_data_sets(self, in_data_set_iterator):
        # Need to manage the iterators if I am going to allow deletes
        # del self.__data_sets[in_data_set_iterator]
        return 0

    def get_figure(self, in_meta_data):
        self.set_working_meta(in_meta_data)
        if self.__working_meta.get_meta_type() == 1:
            i = self.back_scatter()
        elif self.__working_meta.get_meta_type() == 2:
            i = self.depolarization()
        elif self.__working_meta.get_meta_type() == 3:
            i = self.vfm()
        elif self.__working_meta.get_meta_type() == 4:
            i = self.iwp()
        elif self.__working_meta.get_meta_type() == 5:
            i = -99
        elif self.__working_meta.get_meta_type() == 6:
            i = -99
        elif self.__working_meta.get_meta_type() == 7:
            i = -99
        elif self.__working_meta.get_meta_type() == 8:
            i = -99
        elif self.__working_meta.get_meta_type() == 9:
            i = -99
        elif self.__working_meta.get_meta_type() == 10:
            i = -99
        else:
            i = -99

        if i == -99:
            logger.error('Data Set Failed to load: ' + str(self.__working_meta.get_meta_type))
            return -99
            # For types not yet implemented#
        else:
            return i

    
    def back_scatter(self):
        if self.__working_meta.get_meta_wavelength() == "1064":
            data_set_to_get = 'Total_Attenuated_Backscatter_1064'
        else:
            data_set_to_get = 'Total_Attenuated_Backscatter_532'

        temp_iterator = self.load_data_set(data_set_to_get)

        x0 = self.__working_meta.get_meta_x(0)
        x1 = self.__working_meta.get_meta_x(1)
        h0 = self.__working_meta.get_meta_y(0)
        h1 = self.__working_meta.get_meta_y(1)

        data = np.ma.masked_equal(self.__data_sets[temp_iterator].ds_data_set, -9999)

        temp_x = np.arange(x0, x1, dtype=np.float32)
        temp_y, null = np.meshgrid(self.__y_altitude[::], temp_x)

        if constants.debug_switch > 0:
            logger.info("***** Preparing 'interp2d_12' *****")
            self.print_data_set_info(temp_iterator)

        logger.info("***** Launching 'interp2d_12' on Backscatter data*****")

        self.__data_sets[temp_iterator].ds_data_set = interp2d_12(
            data[x0:x1],
            temp_x.astype(np.float32),
            temp_y.astype(np.float32),
            x0, x1, x1 - x0,
            h1, h0, 500
        )

        return temp_iterator

    def depolarization(self):
        AVGING_WIDTH = 15

        if self.__working_meta.get_meta_wavelength() == "1064":
            data_set_to_get_total = 'Total_Attenuated_Backscatter_1064'
            data_set_to_get_perp = 'Perpendicular_Attenuated_Backscatter_1064'
        else:
            data_set_to_get_total = 'Total_Attenuated_Backscatter_532'
            data_set_to_get_perp = 'Perpendicular_Attenuated_Backscatter_532'

        x0 = self.__working_meta.get_meta_x(0)
        x1 = self.__working_meta.get_meta_x(1)
        h0 = self.__working_meta.get_meta_y(0)
        h1 = self.__working_meta.get_meta_y(1)

        temp_iterator = self.load_data_set(data_set_to_get_total)

        total = self.load_data_set(data_set_to_get_total, 'data only')[x0:x1].T
        total = avg_horz_data(total, AVGING_WIDTH)
        
        perpendicular = self.load_data_set(data_set_to_get_perp, 'data only')[x0:x1].T
        perpendicular = avg_horz_data(perpendicular, AVGING_WIDTH)

        parallel = total - perpendicular

        latitude = self.__Latitude[x0:x1]
        latitude = latitude[::AVGING_WIDTH]

        depolar_ratio = perpendicular / parallel

        # Put altitudes above 8.2 km on same spacing as lower ones
        MAX_ALT = 20
        unif_alt = uniform_alt_2(MAX_ALT, self.__y_altitude)
        depolar_ratio = regrid_lidar(self.__y_altitude, depolar_ratio, unif_alt)

        self.__data_sets[temp_iterator].ds_data_set = depolar_ratio

        return temp_iterator

    def vfm(self):
        # Constant variables
        alt_len = 545

        # 15 profiles are in 1 record of VFM data. At the highest altitudes 5 profiles are averaged
        # together.  In the mid altitudes 3 are averaged and at roughly 8 km or less, there are 
        # separate profiles.
        prof_per_row = 15
        temp_iterator = self.load_data_set('Feature_Classification_Flags')

        x0 = self.__working_meta.get_meta_x(0)
        x1 = self.__working_meta.get_meta_x(1)
        h0 = self.__working_meta.get_meta_y(0)
        h1 = self.__working_meta.get_meta_y(1)

        t_time = self.__x_time[::]
        minimum = self.get_x_min(temp_iterator, 'time')
        maximum = self.get_x_max(temp_iterator, 'time')

        #determines how far the file can be viewed
        #if t_time [-1] >= maximum and len(t_time) < 950:
        #    raise IndexError
        #if t_time[0] < minimum:
        #    raise IndexError

        height = self.__y_altitude[33:-5:]

        if constants.debug_switch > 0:
            self.print_working_metadata()

        if temp_iterator <= -1:
            logger.error("Did not load vfm dataset correctly...")
            return -99

        latitude1 = self.__Latitude[::15] # L2 data has 15x less lat points
        latitude2 = latitude1[::prof_per_row]

        # Mask all unknown values
        data_set = np.ma.masked_equal(self.__data_sets[temp_iterator].ds_data_set, -999)

        # Give the number of rows in the dataset
        num_rows = data_set.shape[0]

        # Create an empty array that corresponds to the size of L1 data
        unpacked_vfm = np.zeros((alt_len, prof_per_row * num_rows),np.uint8)


        # Assigning the values from 0-7 to subtype (see CALIPSO data catalog)
        vfm = extract_type(data_set)

        # chaning the number of rows so that it can be plotted
        for i in range(num_rows):
            unpacked_vfm[:,prof_per_row*i:prof_per_row*(i+1)] = vfm_row2block(vfm[i,:])


        # Determining if day or nighttime
        # Doesn't do anything yet... reversing max and min breaks indices in unpacked_vfm       
        if self.__Latitude[0] > self.__Latitude[-1]:
            # Nighttime
            min_indx = x0
            max_indx = x1

        else:
            #Daytime
            min_indx = x0
            max_indx = x1


        vfm = unpacked_vfm[:, min_indx:max_indx]

        # Put altitudes above 8.2 km on same spacing as lower ones
        max_alt = 20
        unif_alt = uniform_alt_2(max_alt, height)
        
        self.__data_sets[temp_iterator].ds_data_set = regrid_lidar(height, vfm, unif_alt)

        return temp_iterator

    def iwp(self):
        # constant variables
        alt_len = 545
        
        # 15 profiles are in 1 record of VFM data
        # At the highest altitudes 5 profiles are averaged
        # together.  In the mid altitudes 3 are averaged and
        # at roughly 8 km or less, there are separate profiles.
        prof_per_row = 15
        temp_iterator = self.load_data_set('Feature_Classification_Flags')

        x0 = self.__working_meta.get_meta_x(0)
        x1 = self.__working_meta.get_meta_x(1)
        h0 = self.__working_meta.get_meta_y(0)
        h1 = self.__working_meta.get_meta_y(1)


        t_time = self.__x_time[::]
        minimum = self.get_x_min(temp_iterator, 'time')
        maximum = self.get_x_max(temp_iterator, 'time')

        # determines how far the file can be viewed
        #if t_time[-1] >= maximum and len(t_time) < 950:
        #    raise IndexError
        #if t_time[0] < minimum:
        #    raise IndexError

        height = self.__y_altitude[33:-5:]
        
        if temp_iterator != -99:
            data_set = self.get_data_set(temp_iterator)
        else:
            logger.error("Did not load iwp dataset correctly...")
            return -99
        
        latitude1 = self.__Latitude[::15] # L2 data has 15x less lat points
        latitude2 = latitude1[::prof_per_row]

        # mask all unknown values
        data_set = np.ma.masked_equal(self.__data_sets[temp_iterator].ds_data_set, -999)

        # giving the number of rows in the dataset
        num_rows = data_set.shape[0]

        # not sure why they are doing prof_per_row here, and the purpose of this
        unpacked_iwp = np.zeros((alt_len, prof_per_row * num_rows), np.uint8)

        # assigning the values from 0-7 to subtype
        iwp = extract_water_phase(data_set)

        # chaning the number of rows so that it can be plotted
        for i in range(num_rows):
            unpacked_iwp[:, prof_per_row * i:prof_per_row * (i + 1)] = vfm_row2block(iwp[i, :])

        # Determining if day or nighttime
        # Doesn't do anything yet... reversing max and min breaks indices in unpacked_vfm       
        if self.__Latitude[0] > self.__Latitude[-1]:
            # Nighttime
            min_indx = x0
            max_indx = x1

        else:
            #Daytime
            min_indx = x0
            max_indx = x1

        iwp = unpacked_iwp[:, min_indx:max_indx]

        # Put altitudes above 8.2 km on same spacing as lower ones
        max_alt = 20
        unif_alt = uniform_alt_2(max_alt, height)

        self.__data_sets[temp_iterator].ds_data_set = regrid_lidar(height, iwp, unif_alt)

        return temp_iterator
