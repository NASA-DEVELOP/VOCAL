from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils
import sys

import numpy as np
import matplotlib as mpl


class MetaData:
    def __init__(self, in_type=0, in_x_min=0, in_x_max=0, in_y_min=0, in_y_max=0, in_wavelength=532):
        self._type = in_type
        self._x = [in_x_min, in_x_max]
        self._y = [in_y_min, in_y_max]
        self._wavelength = in_wavelength


class Data_Set:
    def __init__(self, in_type, in_data_set, in_xrange, in_yrange, in_wavelength=532):
        self.ds_type = int(in_type)
        self.ds_wavelength = in_wavelength
        self.ds_data_set = in_data_set
        self.ds_xrange = in_xrange
        self.ds_yrange = in_yrange
        self.ds_x_label = 'Latitude'
        self.ds_x_label2 = 'Time'
        self.ds_y_label = 'Altitude (km)'

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
            self._title = ''
            self._cbar_label = ''
        elif self.ds_type == 4:
            self._title = ''
            self._cbar_label = ''
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

        if filename == 'Empty':
            return
        else:
            print("Intializing File: " + filename)
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
                self._working_meta = MetaData()

            if "V4" in filename:
                self.__version = "4"
            else:
                self.__version = "3"

            if "L1" in filename:
                self.__data_level = "1"
                #self.__filenameL2 = get_file_name(self, 1)
            else:
                self.__data_level = "2"
                self.__filenameL2 = filename
                #self.__filenameL1 = get_file_name(self, 2)

            self.__data_sets = []

    """Following is simple setters/getters associated with vocalDataBlock Class"""

    # return the value of the minimum Y range (Altitude)#
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
        print in_iterator
        print self.__data_sets[in_iterator].get_ds_type()
        return self.__data_sets[in_iterator].get_ds_type()

    def get_data_set_t(self, in_iterator):
        return self.__data_sets[in_iterator].ds_data_set.T

    def get_data_set_x_min(self, in_iterator):
        return self.__data_sets[in_iterator].ds_xrange[0]

    def get_data_set_x_max(self, in_iterator):
        return self.__data_sets[in_iterator].ds_xrange[-1]

    def get_data_set_y_min(self, in_iterator):
        return self.__data_sets[in_iterator].ds_yrange[0]

    def get_data_set_y_max(self, in_iterator):
        return self.__data_sets[in_iterator].ds_yrange[-1]

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
            for i in self.__data_sets:
                if self.__data_sets[i]._type == self._working_meta._type \
                        and self.__data_sets[i]._wavelength == self._working_meta._wavelength \
                        and self.__data_sets[i]._xrange_time == self._working_meta._x \
                        and self.__data_sets[i]._yrange == self._working_meta._y:
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

    '''# Loads the needed color map
    def load_colormap(self, in_type):

        colormap = ""

        if in_type == 1:
            colormap = 'dat/calipso-backscatter.cmap'
        elif in_type == 2:
            colormap = 'dat/calipso-depolar.cmap'
        elif in_type == 3:
            colormap = 'dat/calipso-vfm.cmap'
        elif in_type == 4:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 5:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 6:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 7:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 8:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 9:
            colormap = 'dat/calipso-undefined.cmap'
        elif in_type == 10:
            colormap = 'dat/calipso-undefined.cmap'
        else:
            colormap = 'dat/calipso-undefined.cmap'
            #index error unknown colormap###

        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors'] / 255.0)
        cm.set_under(cmap['under'] / 255.0)
        cm.set_over(cmap['over'] / 255.0)
        cm.set_bad(cmap['bad'] / 255.0)
        return cm, mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
        '''

    def load_data_set(self, in_data_set_to_get):
        data_set_iterator = self.find_iterator_in_data_set()
        if data_set_iterator == "False" or data_set_iterator == "Empty":
            with HDF(self.__filenameL1) as product:
                temp_data = product[in_data_set_to_get][::]
                temp_data = product[in_data_set_to_get][self._working_meta._x[0]:self._working_meta._x[1]]

            return self.append_data_sets(temp_data)
        else:
            return self.update_data_sets(self.__data_sets[data_set_iterator]._data_set[self._working_meta._x[0], self._working_meta._x[1]], data_set_iterator)

    def back_scatter(self):
        if self._working_meta._wavelength == "1064":
            data_set_to_get = 'Total_Attenuated_Backscatter_1064'
        else:
            data_set_to_get = 'Total_Attenuated_Backscatter_532'

        temp_iterator = self.load_data_set(data_set_to_get)
        self.__data_sets[temp_iterator].ds_data_set = np.ma.masked_equal(self.__data_sets[temp_iterator].ds_data_set, -9999)

        temp_x = np.arange(self._working_meta._x[0], self._working_meta._x[1], dtype=np.float32)

        temp_y, null = np.meshgrid(self.__y_altitude, temp_x)

        self.__data_sets[temp_iterator].ds_data_set = interp2d_12(
            self.__data_sets[temp_iterator].ds_data_set[::],
            temp_x.astype(np.float32),
            temp_y.astype(np.float32),
            self._working_meta._x[0], self._working_meta._x[1],
            self._working_meta._x[1] - self._working_meta._x[0],
            self._working_meta._y[1], self._working_meta._y[0], 500,
        )

        return temp_iterator

    '''
        #cm, norm = self.load_colormap(self.__data_sets[temp_iterator]._type)

        im = in_fig.imshow(
            self.__data_sets[temp_iterator].data_set.T,
            extent=
            (
                self.__data_sets[temp_iterator]._xrange[0], self.__data_sets[temp_iterator]._xrange[-1],
                self.__data_sets[temp_iterator]._yrange[0], self.__data_sets[temp_iterator]._yrange[-1]
            ),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest
        )

        self.__data_sets[temp_iterator]._fig.set_ylabel('Altitude (km)')
        self.__data_sets[temp_iterator]._fig.set_xlabel('Latitude')
        self.__data_sets[temp_iterator]._fig.set_title(
            "Averaged " + self.__data_sets[temp_iterator]._wavelength + "nm Total Attenuated Backscatter")

        cbar_label = 'Total Attenuated Backscatter ' + self.__data_sets[
            temp_iterator]._wavelength + 'nm (km$^{-1}$ sr$^{-1}$)'
        cbar = self.__data_sets[temp_iterator]._fig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = self.__data_sets[temp_iterator]._fig.twiny()
        ax.set_xlabel('Time')
        ax.set_xlim(self.__data_sets[temp_iterator]._xrange[0], self.__data_sets[temp_iterator]._xrange[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))

        in_fig.set_zorder(0)
        ax.set_zorder(1)

        title = in_fig.set_title('Averaged ' + self.__data_sets[temp_iterator]._wavelength + 'nm Total Attenuated Backscatter')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1] * 1.07])

        in_fig = ax
    '''


    def append_data_sets(self, in_data_set):
        self.__data_sets.append(Data_Set(self._working_meta._type, in_data_set, self._working_meta._x, self._working_meta._y, self._working_meta._wavelength))
        return len(self.__data_sets)-1

    def remove_data_sets(self, in_data_set_iterator):
        self.__data_sets.remove(in_data_set_iterator)
        return 0

    def update_data_sets(self, in_data_set, in_data_set_iterator):
        self.__data_sets[in_data_set_iterator] = Data_Set(self._working_meta._type, in_data_set, self._working_meta._x,
                                                          self._working_meta._y, self._working_meta._wavelength)
        return in_data_set_iterator

    def get_figure(self, in_meta_data):
        self.set_working_meta(in_meta_data)
        if self._working_meta._type == 1:
            i = self.back_scatter()
        elif self._working_meta._type == 2:
            i = self.depolarization()
        elif self._working_meta._type == 3:
            i = -99
        elif self._working_meta._type == 4:
            i = -99
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
            # INDEX ERROR#

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
        """TODO"""
        return ""

    def print_working_metadata(self):
        print 'Working MetaData for: ', self.__filenameL1
        print "Type = ", self._working_meta._type
        print
        print "X Count: ", self.__record_count
        print "X-Working Min/Max: ", self._working_meta._x[0], " , ", self._working_meta._x[1]
        print "X-range Time Min: ", self.get_time(0), ' Max: ', self.get_time(-1)
        print "X-range Coords Min: ", self.get_coordinates(0), ' Max: ', self.get_coordinates(-1)
        print
        print "Y Shape: ", self.__y_altitude.shape
        print "Y Count: ", len(self.__y_altitude)
        print "Y-range Altitude Min: ", self.get_altitude(0), ' Max: ', self.get_altitude(-1)
        #print self.__y_altitude
        #wait = input("PRESS ENTER TO CONTINUE.")


"""Needs to be completed and need to load a Perpendicular as well
    def depolarization(self):
        AVGING_WIDTH = 15
        MIN_SCATTER = -0.1
        EXCESSIVE_SCATTER = 0.1
        # Read CALIPSO Data from Level 1B file
        latitude = product["Latitude"][::]
        start_lat = 10.
        end_lat = -30.
        if latitude[0] > latitude[-1]:
            #   Nighttime granule
            min_indx = findLatIndex(start_lat, latitude)
            max_indx = findLatIndex(end_lat, latitude)
        else:
            #   Daytime granule
            min_indx = findLatIndex(end_lat, latitude)
            max_indx = findLatIndex(start_lat, latitude)
        latitude = latitude[min_indx:max_indx]
        tot_532 = product["Total_Attenuated_Backscatter_532"][min_indx:max_indx, :]
        tot_532 = tot_532.T
        perp_532 = product["Perpendicular_Attenuated_Backscatter_532"][min_indx:max_indx, :]
        perp_532 = perp_532.T
        alt = product['metadata']['Lidar_Data_Altitudes']
        # Exclude negative values of backscatter and excessive amounts.
        # The latter are probably due to surface reflection and spikes.
        # tot_532 = ma.masked_where(tot_532 < MIN_SCATTER, tot_532)
        # perp_532 = ma.masked_where(perp_532 < MIN_SCATTER, perp_532)
        # Average horizontally
        avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
        avg_perp_532 = avg_horz_data(perp_532, AVGING_WIDTH)
        latitude = latitude[::AVGING_WIDTH]
        avg_parallel_AB = avg_tot_532 - avg_perp_532
        depolar_ratio = avg_perp_532 / avg_parallel_AB
        # Put altitudes above 8.2 km on same spacing as lower ones
        MAX_ALT = 20
        unif_alt = uniform_alt_2(MAX_ALT, alt)
        regrid_depolar_ratio = regrid_lidar(alt, depolar_ratio, unif_alt)
        # fig = plt.figure(figsize=(10,7))
        fig = plt.figure(figsize=(12, 8))
        # Setup extent of axis values for image.
        #   Note that altitude values are stored from top to bottom
        min_alt = unif_alt[-1]
        max_alt = unif_alt[0]
        start_lat = latitude[0][0]
        end_lat = latitude[-1][0]
        extents = [start_lat, end_lat, min_alt, max_alt]
        colormap = 'calipso-depolar.cmap'
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors'] / 255.0)
        plot_norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
        ax1 = fig.add_axes([0.07, 0.07, 0.85, 0.9, ])
        im = plt.imshow(regrid_depolar_ratio, cmap=cm, aspect='auto',
                        norm=plot_norm, extent=extents, interpolation=None)
        plt.ylabel('Altitude (km)')
        plt.xlabel('Latitude (degrees)')
        granule = "%sZ%s" % extractDatetime(filename)
        title = 'VFM Features for granule %s' % granule
        plt.title(title)
        cbar_label = 'Depolarization Ratio'
        cbar = plt.colorbar(extend='both', use_gridspec=True)
        cbar.set_label(cbar_label)
        plt.savefig("depolarization_ratio.png")
        # plt.show()
"""

'''TODO List
def vfm(self):
def waterIce(self):
'''

