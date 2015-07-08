#!/opt/local/bin/python2.7
#
# plot_depolarization.py
# Brian Magill
# 8/11/2014
#
import sys
import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np
from numpy import ma
from ccplot.hdf import HDF
import ccplot.utils
from avg_lidar_data import avg_horz_data
from uniform_alt_2 import uniform_alt_2
from regrid_lidar import regrid_lidar
from findLatIndex import findLatIndex
from PCF_genTimeUtils import calipsoISO_to_times, extractDatetime

AVGING_WIDTH = 15

MIN_SCATTER = -0.1
EXCESSIVE_SCATTER = 0.1

argv = sys.argv

filename = argv[0]
def drawDepolar(filename, x_range, y_range, fig, pfig):
    x1 = x_range[0]
    x2 = x_range[1]
    h1 = y_range[0]
    h2 = y_range[1]

    # Read CALIPSO Data from Level 1B file
    with HDF(filename) as product:

        time = product["Profile_UTC_Time"][x1:x2, 0]
        
        tot_532 = product["Total_Attenuated_Backscatter_532"][x1:x2]
        tot_532 = tot_532.T

        perp_532 = product["Perpendicular_Attenuated_Backscatter_532"][x1:x2]
        perp_532 = perp_532.T
  
        alt = product['metadata']['Lidar_Data_Altitudes']

    # Exclude negative values of backscatter and excessive amounts.
    # The latter are probably due to surface reflection and spikes.
  
    #tot_532 = ma.masked_where(tot_532 < MIN_SCATTER, tot_532)
    #perp_532 = ma.masked_where(perp_532 < MIN_SCATTER, perp_532)

# Average horizontally

    avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
    avg_perp_532 = avg_horz_data(perp_532, AVGING_WIDTH)
    time = time[::AVGING_WIDTH]

    avg_parallel_AB = avg_tot_532 - avg_perp_532
    depolar_ratio = avg_perp_532/avg_parallel_AB

    # Put altitudes above 8.2 km on same spacing as lower ones

    MAX_ALT = 20
    unif_alt = uniform_alt_2(MAX_ALT, alt)

    regrid_depolar_ratio = regrid_lidar(alt, depolar_ratio,  unif_alt)

    # Setup extent of axis values for image.  
    #   Note that altitude values are stored from top to bottom

    min_alt  = h1
    max_alt  = h2
    start_time   = time[0] 
    end_time     = time[-1]
    extents = [start_time, end_time, min_alt, max_alt]

    colormap = 'dat/calipso-depolar.cmap'

    cmap = ccplot.utils.cmap(colormap)
    cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
    plot_norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

    im = fig.imshow(regrid_depolar_ratio,
                    extent = extents, 
                    cmap = cm,
                    norm = plot_norm, 
                    aspect = 'auto',  
                    interpolation = 'nearest')

    fig.set_ylabel('Altitude (km)')
    fig.set_xlabel('Time')   
    fig.get_xaxis().set_major_locator(mpl.dates.AutoDateLocator())
    fig.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S')) 
     
    granule = "%sZ%s" % extractDatetime(filename)
    title = 'Depolarization Ratio %s' % granule
    fig.set_title(title)

    cbar_label = 'Depolarization Ratio'
    cbar = pfig.colorbar(im)
    cbar.set_label(cbar_label)