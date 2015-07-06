#!/opt/local/bin/python2.7
#
# plot_depolarization.py
# Brian Magill
# 8/11/2014
#
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils

from PCF_genTimeUtils import extractDatetime
from avg_lidar_data import avg_horz_data
import matplotlib as mpl
import numpy as np


def drawDepolar(filename, x_range, y_range, fig, pfig):
    x1 = x_range[0]
    x2 = x_range[1]
    h1 = y_range[0]
    h2 = y_range[1]
    nz = 500
    colormap = 'dat/calipso-depolar.cmap'
    AVGING_WIDTH = 15

    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][x1:x2, 0]
        height = product['metadata']['Lidar_Data_Altitudes']
        tot_532 = product['Total_Attenuated_Backscatter_532'][x1:x2]
        perp_532 = product['Perpendicular_Attenuated_Backscatter_532'][x1:x2]
        alt = product['metadata']['Lidar_Data_Altitudes']
        
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
#         tot_532 = np.ma.masked_equal(tot_532, -9999)
#         perp_532 = np.ma.masked_equal(perp_532, -9999)
#         
        avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
        avg_perp_532 = avg_horz_data(perp_532, AVGING_WIDTH)
        avg_parallel_AB = avg_tot_532 - avg_perp_532
        depolar_ratio = avg_perp_532/avg_parallel_AB
        
        depolar_ratio = np.ma.masked_equal(depolar_ratio, -9999)
        
#         unif_alt = uniform_alt_2(20, alt)
#         regrid_depolar_ratio = regrid_lidar(alt, depolar_ratio, unif_alt)
        
        X = np.arange(x1, x2, dtype=np.float32)
        
        Z, null = np.meshgrid(height, X)
        data = interp2d_12(
            depolar_ratio[::], 
            X.astype(np.float32), 
            Z.astype(np.float32), 
            x1, x2, x2 - x1, 
            h2, h1, nz
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
       
        fig.set_ylabel('Altitute (km)')    
        fig.set_xlabel('Time')   
        fig.get_xaxis().set_major_locator(mpl.dates.AutoDateLocator())
        fig.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        
        granule = "%sZ%s" % extractDatetime(filename)
        title = 'Depolarized Ratio for granule %s' % granule
        fig.set_title(title)                 
        fig.set_title("Averaged 532 nm Depolarized Ratio")
       
        cbar_label = 'Depolarized Ratio 532nm (km$^{-1}$ sr$^{-1}$)'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)