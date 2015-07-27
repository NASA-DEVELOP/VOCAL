#!/opt/local/bin/python2.7
#
# plot_uniform_alt_lidar.py
# Nathan Qian
# Grant Mercer
# Brian Magill
# 8/11/2014
#
import tkMessageBox

from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils

import matplotlib as mpl
import numpy as np


# from gui.CALIPSO_Visualization_Tool import filename
# noinspection PyUnresolvedReferences
def render_backscattered(filename, x_range, y_range, fig, pfig):
    x1 = x_range[0]
    x2 = x_range[1]
    h1 = y_range[0]
    h2 = y_range[1]
    nz = 500
    colormap = 'dat/calipso-backscatter.cmap'

    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][x1:x2, 0]
        minimum = min(product['Profile_UTC_Time'][::])[0]
        maximum = max(product['Profile_UTC_Time'][::])[0]
        
        # lenght of time determines how far the file can be viewed
        if time[-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError
        height = product['metadata']['Lidar_Data_Altitudes']
        dataset = product['Total_Attenuated_Backscatter_532'][x1:x2]
        latitude = product['Latitude'][x1:x2, 0]
        longitude = product['Longitude'][x1:x2, 0]

        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
        dataset = np.ma.masked_equal(dataset, -9999)
        
        _x = np.arange(x1, x2, dtype=np.float32)
        _y, null = np.meshgrid(height, _x)
        data = interp2d_12(
            dataset[::],
            _x.astype(np.float32),
            _y.astype(np.float32),
            x1, x2, x2 - x1,
            h2, h1, nz,
        )
        
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
        cm.set_under(cmap['under']/255.0)
        cm.set_over(cmap['over']/255.0)
        cm.set_bad(cmap['bad']/255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
        
        im = fig.imshow(
            data.T,
            extent=(mpl.dates.date2num(time[0]), mpl.dates.date2num(time[-1]), h1, h2),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )
       
        fig.set_ylabel('Altitude (km)')
        fig.set_xlabel('Time')   
        fig.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        fig.set_title("Averaged 532 nm Total Attenuated Backscatter")
       
        cbar_label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)

        ax2 = fig.twiny()
        ax2.set_xlabel('Latitude')
        ax2.set_xlim(latitude[0], latitude[-1])

        title = fig.set_title('Averaged 532 nm Total Attenuated Backscatter')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1]*1.07])
