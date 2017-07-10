# Andrea Martinez
# Brian Magill
# 8/11/2014
#
import ccplot.utils
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from ccplot.algorithms import interp2d_12
from findLatIndex import findLatIndex
from ccplot.hdf import HDF
from ConfigParser import SafeConfigParser
from vfm_row2block import vfm_row2block
from uniform_alt_2 import uniform_alt_2
from regrid_lidar import regrid_lidar
from interpret_vfm_type import extract_type

def render_vfm(filename, x_range, y_range, fig, pfig):
    #constant variables
    alt_len = 545
    first_alt = y_range[0]
    last_alt = y_range[1]
    first_lat = x_range[0]
    last_lat = x_range [1]
    colormap = 'dat/calipso-vfm.cmap'

    print('xrange: ' + str(x_range) + ', yrange: ' + str(y_range))


    # 15 profiles are in 1 record of VFM data
    # At the highest altitudes 5 profiles are averaged
    # together.  In the mid altitudes 3 are averaged and
    # at roughly 8 km or less, there are separate profiles.
    prof_per_row = 15

    #naming products within the HDF file
    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][first_lat:last_lat, 0]
        minimum = min(product['Profile_UTC_Time'][::])[0]
        maximum = max(product['Profile_UTC_Time'][::])[0]

        #determines how far the file can be viewed
        if time [-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError

        height = product['metadata']['Lidar_Data_Altitudes'][33:-5:]
        dataset = product['Feature_Classification_Flags'][first_lat:last_lat]
        latitude1 = product['Latitude'][first_lat:last_lat,0]
        latitude2 = latitude1[::prof_per_row]
        latitude3 = product['Latitude'][::]
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])

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
        if latitude3[0] > latitude3[-1]:
            #Nighttime
            #min_indx = findLatIndex(start_lat, latitude3)
            #max_indx = findLatIndex(end_lat, latitude3)
            min_indx = 0
            max_indx = 1000

        else:
            #Daytime
            #min_indx = findLatIndex(end_lat, latitude3)
            #max_indx = findLatIndex(start_lat, latitude3)
            min_indx = 1000
            max_indx = 0


        vfm = unpacked_vfm[:, min_indx*prof_per_row:max_indx*prof_per_row]

        max_alt = 20
        unif_alt = uniform_alt_2(max_alt, height)
        print(np.shape(height))
        print(np.shape(vfm))
        print(np.shape(unif_alt))
        print(latitude2)

        regrid_vfm = regrid_lidar(height, vfm, unif_alt)

        #taken from backscatter plot
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors'] / 255.0)
        cm.set_under(cmap['under'] / 255.0)
        cm.set_over(cmap['over'] / 255.0)
        cm.set_bad(cmap['bad'] / 255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

        im = fig.imshow(
            regrid_vfm,
            extent=(latitude2[0], latitude2[-1], first_alt, last_alt),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )

        fig.set_ylabel('Altitude (km)')
        fig.set_xlabel('Latitude')
        fig.set_title("Vertical Feature Mask")
       
        cbar_label = 'Vertical Feature Mask Flags'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = fig.twiny()
        ax.set_xlabel('Time')
        ax.set_xlim(time[0], time[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
 
        fig.set_zorder(0)
        ax.set_zorder(1)

        title = fig.set_title('Vertical Feature Mask')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1]*1.07])

        return ax

        """
        fig.set_ylabel('Altitude (km)')
        #         fig.set_xlabel('Time')
        #         fig.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        fig.set_xlabel('Latitude')
        fig.set_title("Vertical Feature Mask")

        cbar_label = 'Vertical Feature Mask'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = fig.twiny()
        ax.set_xlabel('Latitude')
        ax.set_xlim(latitude2[0], latitude2[-1])
        ax.set_xlabel('Time')
        ax.set_xlim(time[0], time[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))

        fig.set_zorder(0)
        ax.set_zorder(1)

        title = fig.set_title('Vertical Feature Mask')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1] * 1.07])
        """
