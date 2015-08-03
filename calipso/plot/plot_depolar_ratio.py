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
import matplotlib as mpl
import numpy as np
from plot.avg_lidar_data import avg_horz_data
from plot.uniform_alt_2 import uniform_alt_2
from plot.regrid_lidar import regrid_lidar
from plot.findLatIndex import findLatIndex
from plot.PCF_genTimeUtils import extractDatetime


def render_depolarized(filename, x_range, y_range, fig, pfig):
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
        alt = product['metadata']['Lidar_Data_Altitudes']
        minimum = min(product['Profile_UTC_Time'][::])[0]
        maximum = max(product['Profile_UTC_Time'][::])[0]
        latitude = product['Latitude'][x1:x2, 0]

        # length of time determines how far the file can be viewed
        if time[-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError

        # Depolarization_Gain_Ratio_532
        # Depolarization_Gain_Ratio_Uncertainty_532
        #for key in product.keys:
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
        tot_532 = product['Total_Attenuated_Backscatter_532'][x1:x2].T
        perp_532 = product['Perpendicular_Attenuated_Backscatter_532'][x1:x2].T

        """
        tot_532 = product["Total_Attenuated_Backscatter_532"][min_indx:max_indx:]
        tot_532 = tot_532.T
        perp_532 = product["Perpendicular_Attenuated_Backscatter_532"][min_indx:max_indx:]
        perp_532 = perp_532.T
        """
        alt = product['metadata']['Lidar_Data_Altitudes']

        avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
        avg_perp_532 = avg_horz_data(perp_532, AVGING_WIDTH)
        latitude = latitude[::AVGING_WIDTH]
        # avg_parallel_AB = avg_tot_532 - avg_perp_532
        # depolar_ratio = avg_perp_532/avg_parallel_AB

        avg_parallel_AB = tot_532 - perp_532
        depolar_ratio = perp_532 / avg_parallel_AB

        # Put altitudes above 8.2 km on same spacing as lower ones
        MAX_ALT = 20
        unif_alt = uniform_alt_2(MAX_ALT, alt)
        regrid_depolar_ratio = regrid_lidar(alt, depolar_ratio, unif_alt)

        
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
        cm.set_under(cmap['under']/255.0)
        cm.set_over(cmap['over']/255.0)
        cm.set_bad(cmap['bad']/255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

        im = fig.imshow(
            regrid_depolar_ratio,
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
        
        # granule = "%sZ%s" % extractDatetime(filename)
        # title = 'Depolarized Ratio for granule %s' % granule
        # fig.set_title(title)                 
       
        cbar_label = 'Depolarized Ratio 532nm (km$^{-1}$ sr$^{-1}$)'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)

        ax = fig.twiny()
        ax.set_xlabel('Latitude')
        ax.set_xlim(latitude[0], latitude[-1])

        fig.set_zorder(1)
        ax.set_zorder(0)

        title = fig.set_title("Averaged 532 nm Depolarized Ratio")
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1]*1.07])
