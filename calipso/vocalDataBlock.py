from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils

import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure



class dataSet():

    def __init__(self, in_type, in_dataset, in_xrange, in_yrange, in_wavelength = 532):
        self._type = in_type
        self._wavelength = in_wavelength
        self._dataset = in_dataset
        self._xrange = in_xrange
        self._yrange = in_yrange
        self._fig = Figure






class vocalDataBlock():

    def __init__(self, filename):

        self.__filename = filename
        self.__datasets = list()

        with HDF(filename) as product:
            self.__x_time = np.array([ccplot.utils.calipso_time2dt(t) for t in product['Profile_UTC_Time'][::]])
            self.__record_count = len(self.__x_time)
            self.__y_altitude = product['metadata']['Lidar_Data_Altitudes'][::]
            self.__x_coordinates = [product['Longitude'][::],[product['Latitude'][::]]]
            self.__day_night_flag = product['Day_Night_Flag'][::]
            self.__working_type = [0,0]
            self.__working_time = [0,0]
            self.__working_coordinates = [0,0]
            self.__working_altitude = [0,0]
            self.__working_wavelength = 532

        if "V4" in filename:
            self.__version = "4"
        else:
            self.__file_version = "3"

        if "L1" in filename:
            self.__data_level = "1"
        else:
            self.__data_level = "2"

            self.__datasets = []


"""Following is simple setters/getters associated with vocalDataBlock Class"""
    #return the value of the minimum Y range (Altitude)
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
        return [self.__x_coordinates[0][0]],self.__x_coordinates[1][0]

    # return the value of the maximum X range (Coordinate pair [long, lat])
    def get_x_coordinates_max(self):
        return [self.__x_coordinates[0][-1]],self.__x_coordinates[1][-1]

    # return the value at the iterator (in_x) from the time list
    def get_time(self, in_x):
        if in_x >= -1 and in_x <= self.__record_count:
            return self.__x_time[in_x]
        else:
            '''Index Error'''

    # return the value at the iterator (in_x) from the coordinates list -- returns Coordinate pair [long, lat]
    def get_coordinates(self, in_x):
        if in_x >= -1 and in_x <= len(self.__record_count):
            return self.__x_coordinates[in_x]
        else:
            '''Index Error'''

    # return the value at the iterator (in_y) from the altitude list
    def get_altitude(self, in_y):
        if in_y >= -1 and in_y <= len(self.__y_altitude):
            return self.__y_altitude[in_y]
        else:
            '''Index Error'''

    # sets the working type as an integer - refer to constants.py for dictionary
    def set_working_type(self, in_type):
        if in_type >= 0 or in_type < 11:
            self.__working_type = in_type
        else:
            '''Index Error'''

    # accepts a 2-element list of integers - This is the x range for a new data_set based off the working dataset
    # since x can be represented by either coordinates (long,lat) or time, and setting of either working_time or
    #   working_coordinates updates both xtime and xcoordinates.  This could be consolidated into one, but I believe
    #   it is best to seperate them for readability
    def set_working_time(self, in_xtime):
        if in_xtime[0] >= 0 and in_xtime[1] <= self.__record_count:
            self.__working_coordinates = self.__working_time = in_xtime
        else:
            '''Index Error'''

    # accepts a 2-element list of integers - This is the x range for a new data_set based off the working dataset
    # since x can be represented by either coordinates (long,lat) or time, and setting of either working_time or
    #   working_coordinates updates both xtime and xcoordinates.  This could be consolidated into one, but I believe
    #   it is best to seperate them for readability
    def set_working_coordinates(self, in_coordinates):
        if in_coordinates[0] >= 0 and in_coordinates[1] <= self.__record_count:
            self.__working_coordinates = self.__working_time = in_coordinates

    # This allows the setting of the wavelength as some datasets have 532 and 1064 wavelengths.
    #   The default is always 532
    def set_working_wavelength(self, in_wavelength):
        if in_wavelength == '1064':
            self.__working_wavelength = "1064"
        else:
            self.__working_wavelength = "532"

    # accepts a 2-element list of integers - This is the y range (altitude) for a new data_set based off the working dataset
    def set_working_altitude(self, in_altitude):
        if in_altitude[0] >= 0 and in_altitude[1] <= len(self.__y_altitude):
            self.__working_altitude = in_altitude
        else:
            '''Index Error'''
    """End simple setters/getters associated with vocalDataBlock Class"""

    # This will find the iterator for the working dataset within the dataset.  It can also be used to check to see if the working dataset has already been created or if the list is empty
    #   return codes ('empty' == empty, "False" == does not exist in dataset, positive integer is a positive match and returns the iterator needed to access the dataset
    #   and negative interger is an iterator pointing to a dataset that the working dataset exists within
    def find_iterator_in_dataset(self):
        if len(self.__datasets) == 0
            return "Empty"
        else:
            for i in self.__datasets:
                if          self.__datasets[i]._type           == self.__working_type \
                        and self.__datasets[i]._wavelength     == self.__working_wavelength \
                        and self.__datasets[i]._xrange_time    == self.__working_time \
                        and self.__datasets[i]._yrange         == self.__working_altitude:
                    return i
                '''NOT IMPLEMENTED YET  Not sure if I can use the iterators to determine if a set is within a set
                elif
                    if (        self.__datasets[i]._type == self.__working_type \
                            and self.__datasets[i]._wavelength == self.__working_wavelength) \
                                and (   self.__working_altitude in self.__datasets[i]._yrange \
                                and     self.__working_time in self.__datasets[i]._xrange_time):
                        return (-1 * i)'''

        return "False"



    #Loads the needed color map
    def load_color_map(self, in_type):
        if in_type == 1:
            colormap = 'dat/calipso-backscatter.cmap'
        elif type == 2:
            colormap = 'dat/calipso-depolar.cmap'
        elif type == 3:
            colormap = 'dat/calipso-vfm.cmap'
        elif type == 4:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 5:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 6:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 7:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 8:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 9:
            #colormap = 'dat/calipso-undefined.cmap'
        elif type == 10:
            #colormap = 'dat/calipso-undefined.cmap'
        else:
            colormap = ""
            ###UNKNOWN COLORMAP###
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
        cm.set_under(cmap['under'] / 255.0)
        cm.set_over(cmap['over'] / 255.0)
        cm.set_bad(cmap['bad'] / 255.0)
        return [cm, mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)]


    def load_dataset(self, in_dataset_to_get):
        dataset_iterator = self.find_iterator_in_dataset()
        if dataset_iterator == "False" or dataset_iterator == "Empty":
            with HDF(self.__filename) as product:
                temp_data =  product[in_dataset_to_get][self.__working_time[0], self.__working_time[1]]

            return self.__dataset.append_DataSet(self, temp_data)
        else:
            return self.__datasetss.update_DataSet(self, self.__datasetss[dataset_iterator]._dataset[self.__working_time[0], self.__working_time[1]], dataset_iterator)
            

     def backscatter(self):
        if self.__working_wavelength == "1064":
            dataset_to_get = 'Total_Attenuated_Backscatter_1064'
        else:
            dataset_to_get = 'Total_Attenuated_Backscatter_532'

        temp_iterator = load_dataset(self, dataset_to_get)
        self.__datasets[temp_iterator]._dataset = np.ma.masked_equal(self.__datasets[temp_iterator]._dataset, -9999)
        
        temp_x = np.arange(self.__x_time[self.__working_time[0]], self.__working_time[1], dtype=np.float32)
        temp_y, null = np.meshgrid(self.__y_altitude, _x)
        
        interp2d_12(
            self.__datasets[temp_iterator]._dataset[::],
            temp_x.astype(np.float32),
            temp_y.astype(np.float32),
            self.__x_time[self.__working_time[0]], self.__working_time[1],
            self.__x_time[self.__working_time[1]] - self.__working_time[0],
            self.__y_altitude[self.__working_altitude[1]],
            self.__y_altitude[self.__working_altitude[0]], 500,
        )

        cm, norm = self.load_color_map(self, self.__datasets[temp_iterator]._type)

        im = self.__datasets[temp_iterator].fig.imshow(
            self.__datasets[temp_iterator].dataset.T,
            extent=(self.__datasets[temp_iterator]._xrange[0], self.__datasets[temp_iterator]._xrange[-1], self.__datasets[temp_iterator]._yrange[0], self.__datasets[temp_iterator]._yrange[-1]),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )

        self.__datasets[temp_iterator]._fig.set_ylabel('Altitude (km)')
        self.__datasets[temp_iterator]._fig.set_xlabel('Latitude')
        self.__datasets[temp_iterator]._fig.set_title("Averaged " + self.__datasets[temp_iterator]._wavelength + "nm Total Attenuated Backscatter")

        cbar_label = 'Total Attenuated Backscatter ' + self.__datasets[temp_iterator]._wavelength + 'nm (km$^{-1}$ sr$^{-1}$)'
        cbar = self.__datasets[temp_iterator]._fig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = self.__datasets[temp_iterator]._fig.twiny()
        ax.set_xlabel('Time')
        ax.set_xlim(self.__datasets[temp_iterator]._xrange[0], self.__datasets[temp_iterator]._xrange[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))

        fig.set_zorder(0)
        ax.set_zorder(1)

        title = self.__datasets[temp_iterator]._fig.set_title('Averaged ' + self.__datasets[temp_iterator]._wavelength + 'nm Total Attenuated Backscatter')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1] * 1.07])


        
        
        

'''TODO List
def append_datasets(self, in_dataset):
def remove_datasets(self, in_type, in_dataset, in_dataset_iterator):
def update_datasets(self, in_type, in_dataset, in_dataset_iterator):
def depolarization(self):
def vfm(self):
'''








