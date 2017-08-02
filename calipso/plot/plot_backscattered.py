#!/opt/local/bin/python2.7
#
# plot_uniform_alt_lidar.py
# Nathan Qian
# Grant Mercer
# Brian Magill
# 8/11/2014
#

from ccplot.hdf import HDF

import matplotlib as mpl
import numpy as np

from plot.avg_lidar_data import avg_horz_data
from plot.uniform_alt_2 import uniform_alt_2
from plot.regrid_lidar import regrid_lidar

# from gui.CALIPSO_Visualization_Tool import filename
# noinspection PyUnresolvedReferences
def render_backscattered(filename, x_range, y_range, fig, pfig):
    x1 = x_range[0]
    x2 = x_range[1]
    h1 = y_range[0]
    h2 = y_range[1]

    # averaging_width = 15
    # Adjust the averaging with so its uniform per range
    averaging_width = int((x2-x1)/1000)
    if averaging_width < 5:
        averaging_width = 5
    if averaging_width > 15:
        averaging_width = 15

    colormap = constants.PATH + 'dat/calipso-backscatter.cmap'


    print('xrange: ' + str(x_range) + ', yrange: ' + str(y_range))

    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][x1:x2, 0]
        minimum = min(product['Profile_UTC_Time'][::])[0]
        maximum = max(product['Profile_UTC_Time'][::])[0]
        
        # length of time determines how far the file can be viewed
        if time[-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError

        alt = product['metadata']['Lidar_Data_Altitudes']
        dataset = product['Total_Attenuated_Backscatter_532'][x1:x2].T
        latitude = product['Latitude'][x1:x2, 0]
        latitude = latitude[::averaging_width]


        print(np.shape(time))

        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
        dataset = np.ma.masked_equal(dataset, -9999)

        # The following method has been translated from MatLab code written by R. Kuehn 7/10/07
        # Translated by Collin Pampalone 7/19/17
        avg_dataset = avg_horz_data(dataset, averaging_width)
        # Put altitudes above 8.2 km on same spacing as lower ones
        MAX_ALT = 20
        unif_alt = uniform_alt_2(MAX_ALT, alt)
        regrid_dataset = regrid_lidar(alt, avg_dataset, unif_alt)
        data = regrid_dataset
        # End method
        
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
        cm.set_under(cmap['under']/255.0)
        cm.set_over(cmap['over']/255.0)
        cm.set_bad(cmap['bad']/255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
        
        im = fig.imshow(
            #data.T,
            data,
            extent=(latitude[0], latitude[-1], h1, h2),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )

        fig.set_ylabel('Altitude (km)')
        fig.set_xlabel('Latitude')
        fig.set_title("Averaged 532 nm Total Attenuated Backscatter")
       
        cbar_label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = fig.twiny()
        ax.set_xlabel('Time')
        ax.set_xlim(time[0], time[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
 
        fig.set_zorder(0)
        ax.set_zorder(1)

        title = fig.set_title('Averaged 532 nm Total Attenuated Backscatter')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1]*1.07])

        return ax
