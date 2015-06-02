#!/opt/local/bin/python2.7
#
# plot_depolarization.py
# Brian Magill
# 8/11/2014
#
import sys
import matplotlib.pyplot as plt 
import matplotlib as mpl
from ccplot.hdf import HDF
import ccplot.utils
from avg_lidar_data import avg_horz_data
from uniform_alt_2 import uniform_alt_2
from regrid_lidar import regrid_lidar
from findLatIndex import findLatIndex
from PCF_genTimeUtils import extractDatetime

AVGING_WIDTH = 15

MIN_SCATTER = -0.1
EXCESSIVE_SCATTER = 0.1

argv = sys.argv

filename = argv[0]

# Read CALIPSO Data from Level 1B file
with HDF(filename) as product:

    latitude = product["Latitude"][::]

    #  start_lat = 60.
    #  end_lat = 0.

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

    tot_532 = product["Total_Attenuated_Backscatter_532"][min_indx:max_indx,:]
    tot_532 = tot_532.T

    perp_532 = product["Perpendicular_Attenuated_Backscatter_532"][min_indx:max_indx,:]
    perp_532 = perp_532.T
  
    alt = product['metadata']['Lidar_Data_Altitudes']

# Exclude negative values of backscatter and excessive amounts.
# The latter are probably due to surface reflection and spikes.
  
#tot_532 = ma.masked_where(tot_532 < MIN_SCATTER, tot_532)
#perp_532 = ma.masked_where(perp_532 < MIN_SCATTER, perp_532)

# Average horizontally

avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
avg_perp_532 = avg_horz_data(perp_532, AVGING_WIDTH)
latitude = latitude[::AVGING_WIDTH]

avg_parallel_AB = avg_tot_532 - avg_perp_532
depolar_ratio = avg_perp_532/avg_parallel_AB

# Put altitudes above 8.2 km on same spacing as lower ones

MAX_ALT = 20
unif_alt = uniform_alt_2(MAX_ALT, alt)

regrid_depolar_ratio = regrid_lidar(alt, depolar_ratio,  unif_alt)

#fig = plt.figure(figsize=(10,7))
fig = plt.figure(figsize=(12, 8))

# Setup extent of axis values for image.  
#   Note that altitude values are stored from top to bottom

min_alt  = unif_alt[-1]
max_alt  = unif_alt[0]
start_lat   = latitude[0][0] 
end_lat     = latitude[-1][0]
extents = [start_lat, end_lat, min_alt, max_alt]

colormap = 'calipso-depolar.cmap'

cmap = ccplot.utils.cmap(colormap)
cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
plot_norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
ax1 = fig.add_axes([0.07, 0.07, 0.85, 0.9, ])

im = plt.imshow(regrid_depolar_ratio, cmap = cm, aspect = 'auto',  
                        norm = plot_norm, extent = extents, interpolation = None)

plt.ylabel('Altitude (km)')    
plt.xlabel('Latitude (degrees)')  
granule = "%sZ%s" % extractDatetime(filename)
title = 'VFM Features for granule %s' % granule
                
plt.title(title)

cbar_label = 'Depolarization Ratio'
cbar = plt.colorbar(extend='both',use_gridspec=True)
cbar.set_label(cbar_label)

plt.savefig("depolarization_ratio.png")
#plt.show()


