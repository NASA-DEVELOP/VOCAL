from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils
from plot.interpret_vfm_type import extract_type
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
    def __init__(self, in_type=0, in_x_min=0, in_x_max=0, in_y_min=0, in_y_max=0, in_wavelength=532):
        self._type = in_type
        self._x = [in_x_min, in_x_max]
        self._y = [in_y_min, in_y_max]
        self._wavelength = in_wavelength


class Data_Set:
    def __init__(self, in_type, in_data_set, in_xrange, in_yrange, in_time, in_alt, in_lat, in_wavelength=532):
        self.ds_type = int(in_type)
        self.ds_wavelength = in_wavelength
        self.ds_data_set = in_data_set
        self.ds_xrange = in_xrange
        self.ds_yrange = in_yrange
        self.ds_x_label = 'Latitude'
        self.ds_x_label2 = 'Time'
        self.ds_y_label = 'Altitude (km)'
        self.ds_time = in_time
        self.ds_alt = in_alt
        self.ds_lat = in_lat

        self.ds_cbar_label = ''
        self.ds_title = ''
        self.set_title()

    def set_title(self):
        if self.ds_type == 1:
            self._title = "Averaged ", self.ds_wavelength, "nm Total Attenuated Backscatter"
            self._cbar_label = 'Total Attenuated Backscatter ', self.ds_wavelength, 'nm (km$^{-1}$ sr$^{-1}$)'
        elif self.ds_type == 2:
            self._title = "Averaged ", self.ds_wavelength, "nm Depolarized Ratio"
            self._cbar_label = 'Depolarized Ratio  ', self.ds_wavelength , 'nm (km$^{-1}$ sr$^{-1}$)'
        elif self.ds_type == 3:
            self._title = 'Vertical Feature Mask'
            self._cbar_label = 'Vertical Feature Mask'
        elif self.ds_type == 4:
            self._title = 'Ice Water Phase'
            self._cbar_label = 'Ice Water Phase'
        elif self.ds_type == 5:
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 6:
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 7:
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 8:
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 9:
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 10:
            self._title = ''
            self._cbar_label = ''

    def get_ds_type(self):
        return self.ds_type


class VocalDataBlock:
    def __init__(self, filename):

        self.__filenameL1 = filename
        self.__filenameL2 = ''
        self.__data_sets = list()
        self._working_meta = MetaData()

        if filename == 'Empty':
            return
        else:
            logger.info("Intializing File: " + str(filename))
            with HDF(filename) as product:
                time = product['Profile_UTC_Time'][::, 0]
                self.__x_time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
                self.__record_count = len(self.__x_time)
                self.__y_altitude = np.array(product['metadata']['Lidar_Data_Altitudes'][::])
                self.__Longitude = np.array([product['Longitude'][::, 0]])
                self.__Longitude = np.array(self.__Longitude[0][::])
                self.__Latitude = np.array([product['Latitude'][::, 0]])
                self.__Latitude = np.array(self.__Latitude[0][::])
                self.__x_coordinates = np.array([self.__Longitude, self.__Latitude])
                self.__day_night_flag = np.array(product['Day_Night_Flag'][::])

            if "V4" in filename:
                self.__version = "4"
            else:
                self.__version = "3"

            if "L1" in filename:
                self.__data_level = "1"
                self.__filenameL2 = ""
            else:
                self.__data_level = "2"
                self.__filenameL2 = filename
                self.__filenameL1 = ""

            self.find_my_file()

            self.__data_sets = []

    """Following is simple setters/getters associated with vocalDataBlock Class"""

    # return the value of the minimum Y range (Altitude)#

    def get_time_shape(self):
        return np.shape(self.__x_time)

    def get_latitude_shape(self):
        return np.shape(self.__Latitude)

    def get_altitude_shape(self):
        return np.shape(self.__y_altitude)

    def get_y_min(self):
        return self.__y_altitude[0]

    # return the value of the maximum Y range (Altitude)
    def get_y_max(self):
        return self.__y_altitude[-1]

    # return the value of the minimum X range (Time)
    def get_x_time_min(self):
        return self.__x_time[0]

    # return the value of the maximum X range (Time)
    def get_x_time_max(self):
        return self.__x_time[-1]

    # return the value of the minimum X range (Coordinate pair [long, lat])
    def get_x_coordinates_min(self):
        return [self.__x_coordinates[0][0]], self.__x_coordinates[1][0]

    # return the value of the maximum X range (Coordinate pair [long, lat])
    def get_x_coordinates_max(self):
        return [self.__x_coordinates[0][-1]], self.__x_coordinates[1][-1]

    def get_x_latitude(self,in_value):
        return self.__Latitude[in_value]

    # return the value at the iterator (in_x) from the time list
    def get_time(self, in_x):
        if -1 <= in_x <= self.__record_count:
            return self.__x_time[in_x]
        else:
            '''Index Error'''

    # return the value at the iterator (in_x) from the coordinates list -- returns Coordinate pair [long, lat]
    def get_coordinates(self, in_x):
        if -1 <= in_x < self.__record_count:
            return self.__x_coordinates[0][in_x],self.__x_coordinates[1][in_x]
        else:
            '''Index Error'''

    # return the value at the iterator (in_y) from the altitude list
    def get_altitude(self, in_y):
        if -1 <= in_y < len(self.__y_altitude):
            return self.__y_altitude[in_y]
        else:
            '''Index Error'''

    # sets the working type as an integer - refer to constants.py for dictionary
    def set_working_type(self, in_type):
        if in_type >= 0 or in_type < 11:
            self._working_meta._type = in_type
        else:
            '''Index Error'''

    # accepts a 2-element list of integers - This is the x range for a new data_set based off the working data_set
    # since x can be represented by either coordinates (long,lat) or time, and setting of either working_time or
    #   working_coordinates updates both xtime and xcoordinates.  This could be consolidated into one, but I believe
    #   it is best to seperate them for readability
    def set_working_time(self, in_xtime):

        if 0 <= in_xtime[0] < in_xtime[1] <= self.__record_count:
            self._working_meta._x = in_xtime
        else:
            '''Index Error'''

    # accepts a 2-element list of integers - This is the x range for a new data_set based off the working data_set
    # since x can be represented by either coordinates (long,lat) or time, and setting of either working_time or
    #   working_coordinates updates both xtime and xcoordinates.  This could be consolidated into one, but I believe
    #   it is best to seperate them for readability
    def set_working_coordinates(self, in_coordinates):
        if 0 <= in_coordinates[0] < in_coordinates[1] <= self.__record_count:
            self._working_meta._x = in_coordinates

    # This allows the setting of the wavelength as some data_sets have 532 and 1064 wavelengths.
    #   The default is always 532
    def set_working_wavelength(self, in_wavelength):
        if in_wavelength == '1064':
            self._working_meta._wavelength = "1064"
        else:
            self._working_meta._wavelength = "532"

    # accepts a 2-element list of integers - This is the y range (altitude) for a new data_set based off the working data_set
    def set_working_altitude(self, in_altitude):
        if 0 <= in_altitude[0] < in_altitude[1] <= len(self.__y_altitude):
            self._working_meta._y = in_altitude
        else:
            '''Index Error'''

    def get_data_set_type(self, in_iterator):
        return self.__data_sets[in_iterator].get_ds_type()

    def get_data_set(self, in_iterator, transpose='none'):
        if transpose == 'transpose':
            return self.__data_sets[in_iterator].ds_data_set.T
        else:
            return self.__data_sets[in_iterator].ds_data_set

    def get_data_set_x_min(self, in_iterator, in_type='time'):
        if in_type == 'iterator':
            return 0
        elif in_type == 'latitude':
            return self.__data_sets[in_iterator].ds_lat[0]
        elif in_type == 'real':
            return self.__data_sets[in_iterator].ds_xrange[0]
        else:
            return self.__data_sets[in_iterator].ds_time[0]

    def get_data_set_x_max(self, in_iterator, in_type='iterator'):
        if in_type == 'iterator':
            return len(self.__data_sets[in_iterator].ds_time) - 1
        elif in_type == 'latitude':
            return self.__data_sets[in_iterator].ds_lat[-1]
        elif in_type == 'real':
            return self.__data_sets[in_iterator].ds_xrange[1]
        else:
            return self.__data_sets[in_iterator].ds_time[-1]

    def get_data_set_y_min(self, in_iterator, in_type='iterator'):
        if in_type == 'iterator':
            return 0
        elif in_type == 'real':
            return self.__data_sets[in_iterator].ds_yrange[0]
        else:
            return self.__data_sets[in_iterator].ds_alt[0]

    def get_data_set_y_max(self, in_iterator, in_type='iterator'):
        if in_type == 'iterator':
            return len(self.__data_sets[in_iterator].ds_alt)-1
        elif in_type == 'real':
            return self.__data_sets[in_iterator].ds_yrange[1]
        else:
            return self.__data_sets[in_iterator].ds_alt[-1]

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

    # This will find the iterator for the working data_set within the data_set.  It can also be used to check to see if the working data_set has already been created or if the list is empty
    #   return codes ('empty' == empty, "False" == does not exist in data_set, positive integer is a positive match and returns the iterator needed to access the data_set
    #   and negative interger is an iterator pointing to a data_set that the working data_set exists within
    def find_iterator_in_data_set(self):
        if len(self.__data_sets) == 0:
            return "Empty"
        else:
            for i in range(0, len(self.__data_sets)):
                if self.__data_sets[i].ds_type == self._working_meta._type \
                        and self.__data_sets[i].ds_wavelength == self._working_meta._wavelength \
                        and self.__data_sets[i].ds_xrange == self._working_meta._x \
                        and self.__data_sets[i].ds_yrange == self._working_meta._y:
                    return i
                '''NOT IMPLEMENTED YET  Not sure if I can use the iterators to determine if a set is within a set
                elif
                    if (        self.__data_sets[i]._type == self.__working_meta._type \
                            and self.__data_sets[i]._wavelength == self.__working_meta._wavelength) \
                                and (   self.__working_meta._altitude in self.__data_sets[i]._yrange \
                                and     [self.__working_meta._x_min in self.__data_sets[i]._xrange_time):
                        return (-1 * i)'''

        return "False"

    def set_working_meta(self, in_meta_data):
        self.set_working_type(in_meta_data._type)
        self.set_working_time(in_meta_data._x)
        self.set_working_coordinates(in_meta_data._x)
        self.set_working_altitude(in_meta_data._y)
        self.set_working_wavelength(in_meta_data._wavelength)

    def load_data_set(self, in_data_set_to_get):
        data_set_iterator = self.find_iterator_in_data_set()
        if self._working_meta._type == 3 or self._working_meta._type == 4:
            fname = self.__filenameL2
        else:
            fname = self.__filenameL1

        if fname == "":
            logger.error('Data file not available')
            return -99
        else:
            if constants.debug_switch > 0:
                logger.info('Attempting to open data set: ' + str(in_data_set_to_get))
                logger.info('From File: ' + str(fname))

            with HDF(fname) as product:
                if constants.debug_switch > 0:
                    logger.info("Loading data set: " + in_data_set_to_get)
                    logger.info("From: " + str(fname))
                temp_data = product[in_data_set_to_get][self._working_meta._x[0]:self._working_meta._x[1]]

            if data_set_iterator == "False" or data_set_iterator == "Empty":
                return self.append_data_sets(temp_data)
            else:
                return self.update_data_sets(temp_data, data_set_iterator)

    def append_data_sets(self, in_data_set):
        self.__data_sets.append(Data_Set(
            self._working_meta._type, in_data_set,
            self._working_meta._x,
            self._working_meta._y,
            self.__x_time[self._working_meta._x[0]:self._working_meta._x[1]],
            self.__y_altitude[self._working_meta._y[0]:self._working_meta._y[1]],
            self.__Latitude[self._working_meta._x[0]:self._working_meta._x[1]],
            self._working_meta._wavelength,

        ))
        if constants.debug_switch > 0:
            logger.info("***** Successfully created dataset from:*****")
            self.print_working_metadata()
            logger.info("***** Resulting data set:  *****")
            self.print_data_set_info(len(self.__data_sets)-1)
            return len(self.__data_sets)-1

    def remove_data_sets(self, in_data_set_iterator):
        #Need to manage the iterators if I am going to allow deletes
        #del self.__data_sets[in_data_set_iterator]
        return 0

    def update_data_sets(self, in_data_set, in_data_set_iterator):
        self.__data_sets[in_data_set_iterator] = Data_Set(
            self._working_meta._type, in_data_set,
            self._working_meta._x,
            self._working_meta._y,
            self.__x_time[self._working_meta._x[0]:self._working_meta._x[1]],
            self.__y_altitude[self._working_meta._y[0]:self._working_meta._y[1]],
            self.__Latitude[self._working_meta._x[0]:self._working_meta._x[1]],
            self._working_meta._wavelength,

        )
        return in_data_set_iterator

    def get_figure(self, in_meta_data):
        self.set_working_meta(in_meta_data)
        if self._working_meta._type == 1:
            i = self.back_scatter()
        elif self._working_meta._type == 2:
            i = self.depolarization()
        elif self._working_meta._type == 3:
            i = self.vfm()
        elif self._working_meta._type == 4:
            i = self.iwp()
        elif self._working_meta._type == 5:
            i = -99
        elif self._working_meta._type == 6:
            i = -99
        elif self._working_meta._type == 7:
            i = -99
        elif self._working_meta._type == 8:
            i = -99
        elif self._working_meta._type == 9:
            i = -99
        elif self._working_meta._type == 10:
            i = -99
        else:
            i = -99

        if i == -99:
            logger.error('Type not implemented...yet: ' + self._working_meta._type)
            tkMessageBox.showerror('Blend plot type not yet implemented')
            return -99
            # For types not yet implemented#
        else:
            return i

    def get_iterator(self, in_type, in_range):
        if in_type == 'altitude':
            return self.__y_altitude.searchsorted(self, in_range)
        elif in_type == 'time':
            return self.__x_time.searchsorted(self, in_range)
        elif in_type == 'latitude':
            return self.__x_coordinates[1].searchsorted(self, in_range)
        elif in_type == 'longitude':
            return self.__x_coordinates[0].searchsorted(self, in_range)

    def check_iterators(self, in_type, in_range):
        if in_range[0] is not float:
            in_range[0] = self.get_iterator(in_type, in_range[0])
        if in_range[1] is not float:
            in_range[1] = self.get_iterator(in_type, in_range[1])
        return [in_range]

    def get_file_name(self, levelToGet):
        if levelToGet == 1:
            return self.__filenameL1
        elif levelToGet == 2:
            return self.__filenameL2
        else:
            logger.error('Out of range, Suppports Level 1 and 2 data files.')
            return ""

    def find_my_file(self):

        if self.__filenameL1 == "" and self.__filenameL2 == "":
            logger.error("Need to load at least one file...")
            return 0
        elif self.__filenameL1 != "" and self.__filenameL2 != "":
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

        for i in range(0, len(my_str)-1):
            search_path = search_path + str(my_str[i]) + str(slash)

        search_extension = "hdf"

        logger.info('Searching for %s' % search_for)
        logger.info('version of %s' % search_sub_name)
        logger.info('in path: %s' % search_path)

        for root, dirs_list, files_list in os.walk(search_path):
            for file_name in files_list:
                if (file_name.find(search_sub_name) != -1 and  # Must have same name as the file we know
                            file_name.find(search_extension) != -1 and  # must be an hdf file
                            file_name.find(search_for) != -1):  # Must be the level of file
                    if search_for == 'L1':
                        self.__filenameL1 = str(search_path + file_name)
                        logger.info('Found missing L1 file %s' % str(file_name))
                        if constants.debug_switch > 0:
                            logger.info('Path = %s' % search_path)
                            logger.info('File = %s' % file_name)
                            logger.info('fileNameV1 = %s' % str(self.get_file_name(1)))
                        return 1
                    elif search_for == 'L2':
                        self.__filenameL2 = str(search_path + file_name)
                        logger.info('Found missing L2 file %s' % str(file_name))
                        if constants.debug_switch > 0:
                            logger.info('Path = %s' % search_path)
                            logger.info('File = %s' % file_name)

                            logger.info('fileNameV2 = %s' % str(self.get_file_name(2)))

                        return 2
                    else:
                        logger.warning('What were we looking for?')
                        return 0

        logger.warning('Could not find matching %s in same dir...All features may not be available' % good_file)
        return 0

    def print_working_metadata(self):
        logger.info("***************BEGIN META DATA***************")
        logger.info("Working MetaData for: %s" % str(self.__filenameL1))
        logger.info("Type = %s" % str(self._working_meta._type))
        logger.info("X Count: %s" % str(self.__record_count))
        logger.info("X Time Shape: %s" % str(np.shape(self.__x_time)))
        logger.info("X Latitude Shape: %s" % str(np.shape(self.__Latitude)))
        logger.info("X Longitude Shape: %s" % str(np.shape(self.__Latitude)))
        logger.info("X-Working Min/Max: " + str(self._working_meta._x[0]) + "/" + str(self._working_meta._x[1]))
        logger.info("X-range Time will be, Min: " + str(self.get_time(0)) + " Max: " +str(self.get_time(-1)))
        logger.info("X-range Coords will be, Min: " + str(self.get_coordinates(0)) + " Max: " + str(self.get_coordinates(-1)))
        logger.info("Y Shape: %s" % str(self.__y_altitude.shape))
        logger.info("Y Count: %s" % str(len(self.__y_altitude)))
        logger.info("Y-range Altitude will be, Min: " + str(self.get_altitude(0)) + " Max: " + str(self.get_altitude(-1)))
        logger.info("***************END META DATA***************")

    def print_data_set_info(self, in_iterator):
        logger.info("***************BEGIN DATA SET***************")
        logger.info("Iterator: %s" % str(in_iterator))
        logger.info("Data Shape: %s" % str(np.shape(self.__data_sets[in_iterator].ds_data_set)))
        logger.info("Time Shape: %s" % str(np.shape(self.__data_sets[in_iterator].ds_time)))
        logger.info("Latitude Shape: %s" % str(np.shape(self.__data_sets[in_iterator].ds_lat)))
        logger.info("Altitude Shape: %s" % str(np.shape(self.__data_sets[in_iterator].ds_alt)))
        logger.info("********************")
        logger.info("Real Iterators for x1, x2, y1, y2: (" +
            str(self.get_data_set_x_min(in_iterator, 'real')) + ", " +
            str(self.get_data_set_x_max(in_iterator, 'real')) + ", " +
            str(self.get_data_set_y_min(in_iterator, 'real')) + ", " +
            str(self.get_data_set_y_max(in_iterator, 'real')) +
        ")")
        logger.info("Data Set Iterators for x1, x2, y1, y2: (" +
            str(self.get_data_set_x_min(in_iterator, 'iterator')) + ", " +
            str(self.get_data_set_x_max(in_iterator, 'iterator')) + ", " +
            str(self.get_data_set_y_min(in_iterator, 'iterator')) + ", " +
            str(self.get_data_set_y_max(in_iterator, 'iterator')) +
        ")")
        logger.info("********************")
        logger.info("Values for x1, x2, y1, y2: (" +
            str(self.get_data_set_x_min(in_iterator, 'time')) + ", " +
            str(self.get_data_set_x_max(in_iterator, 'time')) + ", " +
            str(self.get_data_set_y_min(in_iterator, 'value')) + ", " +
            str(self.get_data_set_y_max(in_iterator, 'value')) +
            ")")
        logger.info("***************END DATA SET***************")

    def back_scatter(self):
        if self._working_meta._wavelength == "1064":
            data_set_to_get = 'Total_Attenuated_Backscatter_1064'
        else:
            data_set_to_get = 'Total_Attenuated_Backscatter_532'

        temp_iterator = self.load_data_set(data_set_to_get)
        self.__data_sets[temp_iterator].ds_data_set = np.ma.masked_equal(self.__data_sets[temp_iterator].ds_data_set, -9999)

        temp_x = np.arange(self._working_meta._x[0],self._working_meta._x[1], dtype=np.float32)
        temp_y, null = np.meshgrid(self.__y_altitude[::], temp_x)

        if constants.debug_switch > 0:
            logger.info("***** Preparing 'interp2d_12' *****")
            self.print_data_set_info(temp_iterator)

        logger.info("***** Launching 'interp2d_12' on Backscatter data*****")

        self.__data_sets[temp_iterator].ds_data_set = interp2d_12(
            self.__data_sets[temp_iterator].ds_data_set[::],
            temp_x.astype(np.float32),
            temp_y.astype(np.float32),
            self._working_meta._x[0], self._working_meta._x[1],
            self._working_meta._x[1] - self._working_meta._x[0],
            self._working_meta._y[1], self._working_meta._y[0], 500
        )

        return temp_iterator

    def depolarization(self):
        AVGING_WIDTH = 15

        if self._working_meta._wavelength == "1064":
            data_set_to_get_total = 'Total_Attenuated_Backscatter_1064'
            data_set_to_get_perp = 'Perpendicular_Attenuated_Backscatter_1064'
        else:
            data_set_to_get_total = 'Total_Attenuated_Backscatter_532'
            data_set_to_get_perp = 'Perpendicular_Attenuated_Backscatter_532'
        i_tot = self.load_data_set(data_set_to_get_total)
        total = self.get_data_set(i_tot, 'transpose')
        i_perp = self.load_data_set(data_set_to_get_perp)
        perpendicular = self.get_data_set(i_perp, 'transpose')

        self.remove_data_sets(i_tot)
        self.remove_data_sets(i_perp)

        latitude = self.__Latitude[self._working_meta._x[0]:self._working_meta._x[1]]
        total = avg_horz_data(total, AVGING_WIDTH)
        perpendicular = avg_horz_data(perpendicular, AVGING_WIDTH)
        latitude = latitude[::AVGING_WIDTH]
        parrallel = total - perpendicular

        depolar_ratio = perpendicular / parrallel

        # Put altitudes above 8.2 km on same spacing as lower ones
        MAX_ALT = 30
        unif_alt = uniform_alt_2(MAX_ALT, self.__y_altitude)
        depolar_ratio = regrid_lidar(self.__y_altitude, depolar_ratio, unif_alt)

        return self.append_data_sets(depolar_ratio)

    def vfm(self):
        #constant variables
        alt_len = 545
        data_set_to_get = 'Feature_Classification_Flags'

        # 15 profiles are in 1 record of VFM data
        # At the highest altitudes 5 profiles are averaged
        # together.  In the mid altitudes 3 are averaged and
        # at roughly 8 km or less, there are separate profiles.
        prof_per_row = 15

        t_time = self.__x_time[self._working_meta._x[0]:self._working_meta._x[1]]
        minimum = self.get_x_time_min()
        maximum = self.get_x_time_max()

        #determines how far the file can be viewed
        if t_time [-1] >= maximum and len(t_time) < 950:
            raise IndexError
        if t_time[0] < minimum:
            raise IndexError

        height = self.__y_altitude[33:-5:]
        #height = self.__y_altitude[self._working_meta._y[0]:self._working_meta._y[1]]
        if constants.debug_switch > 0:
            self.print_working_metadata()

        my_iterator = self.load_data_set(data_set_to_get)

        print my_iterator
        print type(my_iterator)

        if my_iterator > -1:
            dataset = self.get_data_set(my_iterator)
        else:
            logger.error("Did not load vfm dataset correctly...")
            return -99

        latitude1 = self.__Latitude[self._working_meta._x[0]:self._working_meta._x[1]]
        latitude2 = latitude1[::prof_per_row]

        # mask all unknown values
        dataset = np.ma.masked_equal(dataset, -999)

        #giving the number of rows in the dataset
        num_rows = dataset.shape[0]

        #not sure why they are doing prof_per_row here, and the purpose of this
        unpacked_vfm = np.zeros((alt_len, prof_per_row*num_rows),np.uint8)


        #assigning the values from 0-7 to subtype
        vfm = extract_type(dataset)

        #chaning the number of rows so that it can be plotted
        for i in range(num_rows):
            unpacked_vfm[:,prof_per_row*i:prof_per_row*(i+1)] = vfm_row2block(vfm[i,:])

        start_lat =-30
        end_lat = -80

        #Determining if day or nighttime
        if self.__Latitude[0] > self.__Latitude[-1]:
            #Nighttime
            min_indx = findLatIndex(start_lat, self.__Latitude[::])
            max_indx = findLatIndex(end_lat, self.__Latitude[::])
        else:
            #Daytime
            min_indx = findLatIndex(end_lat, self.__Latitude[::])
            max_indx = findLatIndex(start_lat, self.__Latitude[::])

        vfm = unpacked_vfm[:, min_indx*prof_per_row:max_indx*prof_per_row]

        max_alt = 30
        unif_alt = uniform_alt_2(max_alt, height)
        regrid_lidar(height, vfm, unif_alt)

        return self.update_data_sets(regrid_lidar(height, vfm, unif_alt), my_iterator)

    def render_iwp(self):
        # constant variables
        alt_len = 545
        first_alt = self._working_meta._y[0]
        last_alt = self._working_meta._y[1]
        first_lat = self._working_meta._x[0]
        last_lat = self._working_meta._x[1]
        colormap = 'dat/calipso-icewaterphase.cmap'
        data_set_to_get = "Feature_Classification_Flags"

        # 15 profiles are in 1 record of VFM data
        # At the highest altitudes 5 profiles are averaged
        # together.  In the mid altitudes 3 are averaged and
        # at roughly 8 km or less, there are separate profiles.
        prof_per_row = 15


        time = self.__x_time[first_lat:last_lat, 0]
        minimum = self.get_x_time_min()
        maximum = self.get_x_time_max()

        # determines how far the file can be viewed
        if time[-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError

        height = self.__y_altitude[33:-5:]
        my_iterator = self.load_data_set('Feature_Classification_Flags')

        if my_iterator != -99:
            dataset = self.load_data_set(my_iterator)
        else:
            logger.error("Did not load iwp dataset correctly...")
            return -99

        latitude1 = self.__Latitude[first_lat:last_lat, 0]
        latitude2 = latitude1[::prof_per_row]
        latitude3 = self.__Latitude
        #time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])

        # mask all unknown values
        dataset = np.ma.masked_equal(dataset, -999)

        # giving the number of rows in the dataset
        num_rows = dataset.shape[0]

        # not sure why they are doing prof_per_row here, and the purpose of this
        unpacked_iwp = np.zeros((alt_len, prof_per_row * num_rows), np.uint8)

        # assigning the values from 0-7 to subtype
        iwp = extract_water_phase(dataset)

        # chaning the number of rows so that it can be plotted
        for i in range(num_rows):
            unpacked_iwp[:, prof_per_row * i:prof_per_row * (i + 1)] = vfm_row2block(iwp[i, :])

        start_lat = -30
        end_lat = -80

        # Determining if day or nighttime
        if latitude3[0] > latitude3[-1]:
            # Nighttime
            min_indx = findLatIndex(start_lat, latitude3)
            max_indx = findLatIndex(end_lat, latitude3)
        else:
            # Daytime
            min_indx = findLatIndex(end_lat, latitude3)
            max_indx = findLatIndex(start_lat, latitude3)

        iwp = unpacked_iwp[:, min_indx * prof_per_row:max_indx * prof_per_row]

        max_alt = 30
        unif_alt = uniform_alt_2(max_alt, height)

        return self.update_data_sets(regrid_lidar(height, iwp, unif_alt), my_iterator)


