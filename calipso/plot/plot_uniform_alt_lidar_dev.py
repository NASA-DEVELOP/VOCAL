#!/opt/local/bin/python2.7
#
# plot_uniform_alt_lidar.py
# Brian Magill
# 8/11/2014
#
import ccplot.utils
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
from PCF_genTimeUtils import extractDatetime
import numpy as np
import matplotlib as mpl


# from gui.CALIPSO_Visualization_Tool import filename
def drawBackscattered(filename, x_range, y_range, fig, pfig):   
    x1 = x_range[0]
    x2 = x_range[1]
    h1 = y_range[0]
    h2 = y_range[1]
    nz = 500
    colormap = 'dat/calipso-backscatter.cmap'

    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][x1:x2, 0]
        height = product['metadata']['Lidar_Data_Altitudes']
        dataset = product['Total_Attenuated_Backscatter_532'][x1:x2]
        
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
        dataset = np.ma.masked_equal(dataset, -9999)
        
        X = np.arange(x1, x2, dtype=np.float32)
        Z, null = np.meshgrid(height, X)
        data = interp2d_12(
            dataset[::],
            X.astype(np.float32),
            Z.astype(np.float32),
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
            norm=norm,
            aspect='auto',
            interpolation='nearest',
        )
       
        fig.set_ylabel('Altitude (km)')
        fig.set_xlabel('Time')   
        fig.get_xaxis().set_major_locator(mpl.dates.AutoDateLocator())
        fig.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        
        granule = "%sZ%s" % extractDatetime(filename)
        title = 'Averaged 532 nm Total Attenuated Backscatter for granule %s' % granule
        fig.set_title(title)                 
        fig.set_title("Averaged 532 nm Total Attenuated Backscatter")
       
        cbar_label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)
