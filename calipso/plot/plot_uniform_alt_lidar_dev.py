#!/opt/local/bin/python2.7
#
# plot_uniform_alt_lidar.py
# Brian Magill
# 8/11/2014
#
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
import ccplot.utils

from PCF_genTimeUtils import extractDatetime
from avg_lidar_data import avg_horz_data
from findLatIndex import findLatIndex
import matplotlib as mpl
import numpy as np
from regrid_lidar import regrid_lidar
from uniform_alt_2 import uniform_alt_2


#from gui.CALIPSO_Visualization_Tool import filename
def drawBackscattered(filename, fig, pfig):
    AVGING_WIDTH = 15
      
    MIN_SCATTER = -0.1
    EXCESSIVE_SCATTER = 0.1
      
    # Read CALIPSO Data from Level 1B file
    with HDF(filename) as product:
        latitude = product["Latitude"][::]
        time = product['Profile_UTC_Time'][0:1000, 0]
      
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
      
        start_lat = 35.
        end_lat = -15.
      
        # Retrieve only latitudes of interest
        if latitude[0] > latitude[-1]:
            # Nighttime granule
            min_indx = findLatIndex(start_lat, latitude)
            max_indx = findLatIndex(end_lat, latitude)
        else:
            # Daytime granule
            min_indx = findLatIndex(end_lat, latitude)
            max_indx = findLatIndex(start_lat, latitude)
      
        latitude = latitude[min_indx:max_indx]
      
        tot_532 = product["Total_Attenuated_Backscatter_532"][min_indx:max_indx,:]
        tot_532 = tot_532.T
        
        alt = product['metadata']['Lidar_Data_Altitudes']
        
    # Exclude negative values of backscatter and excessive amounts.
    # The latter are probably due to surface reflection and spikes.
        
    tot_532 = np.ma.masked_where(tot_532 < MIN_SCATTER, tot_532)
    tot_532 = np.ma.masked_where(tot_532 > EXCESSIVE_SCATTER, tot_532)
      
    # Average horizontally
      
    avg_tot_532 = avg_horz_data(tot_532, AVGING_WIDTH)
    latitude = latitude[::AVGING_WIDTH]
      
    # Put altitudes above 8.2 km on same spacing as lower ones
      
    MAX_ALT = 20
    unif_alt = uniform_alt_2(MAX_ALT, alt)
      
    regrid_atten_back = regrid_lidar(alt, avg_tot_532, unif_alt)
      
    # Setup extent of axis values for image.  
    # Note that altitude values are stored from top to bottom
      
    min_alt  = unif_alt[-1]
    max_alt  = unif_alt[0]
    start_lat   = latitude[0][0] 
    end_lat     = latitude[-1][0]
    extents = [start_lat, end_lat, min_alt, max_alt]
      
    colormap = 'dat/calipso-backscatter.cmap'
       
    cmap = ccplot.utils.cmap(colormap)
    cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
    cm.set_under(cmap['under']/255.0)
    cm.set_over(cmap['over']/255.0)
    cm.set_bad(cmap['bad']/255.0)
    plot_norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
       
    im = fig.imshow(regrid_atten_back, cmap = cm, aspect = 'auto',  
                    norm = plot_norm, extent = extents, interpolation = None)
       
    fig.set_ylabel('Altitude (km)')    
    fig.set_xlabel('Latitude (degrees)')   
    granule = "%sZ%s" % extractDatetime(filename)
    title = 'Averaged 532 nm Total Attenuated Backscatter for granule %s' % granule
    fig.set_title(title)                 
    fig.set_title("Averaged 532 nm Total Attenuated Backscatter")
   
    cbar_label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
    cbar = pfig.colorbar(im)
    #cbar = plt.colorbar(extend='both',use_gridspec=True)
    cbar.set_label(cbar_label)        

#     with HDF(filename) as product:
#         x1 = 0
#         x2 = 1000
#         h1 = 0  # km
#         h2 = 20  # km
#         nz = 500  # Number of pixels in the vertical.
#         name = 'Total_Attenuated_Backscatter_532'
#         # Import datasets.
#         time = product['Profile_UTC_Time'][x1:x2, 0]
#         height = product['metadata']['Lidar_Data_Altitudes']
#         dataset = product[name][x1:x2]
#         colormap = 'dat/calipso-backscatter.cmap'
# 
#         # Convert time to datetime.
#         time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
# 
#         # Mask missing values.
#         dataset = np.ma.masked_equal(dataset, -9999)
# 
#         # Interpolate data on a regular grid.
#         X = np.arange(x1, x2, dtype=np.float32)
#         Z, null = np.meshgrid(height, X)
#         data = interp2d_12(
#             dataset[::],
#             X.astype(np.float32),
#             Z.astype(np.float32),
#             x1, x2, x2 - x1,
#             h2, h1, nz,
#         )
# 
#         # Import colormap.
#         cmap = ccplot.utils.cmap(colormap)
#         cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
#         cm.set_under(cmap['under']/255.0)
#         cm.set_over(cmap['over']/255.0)
#         cm.set_bad(cmap['bad']/255.0)
#         norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
# 
#         # Plot figure.
# #         TIME_FORMAT = '%e %b %Y %H:%M:%S UTC'
#         im = fig.imshow(
#             data.T,
#             extent=(mpl.dates.date2num(time[0]), mpl.dates.date2num(time[-1]), h1, h2),
#             cmap=cm,
#             norm=norm,
#             aspect='auto',
#             interpolation='nearest',
#         )
#         fig.set_ylabel('Altitude (km)')    
#         fig.set_xlabel('Latitude (degrees)')   
#         granule = "%sZ%s" % extractDatetime(filename)
#         title = 'Averaged 532 nm Total Attenuated Backscatter for granule %s' % granule
#         fig.set_title(title)                 
#         fig.set_title("Averaged 532 nm Total Attenuated Backscatter")
#    
#         cbar_label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
#         cbar = pfig.colorbar(im)
#         #cbar = plt.colorbar(extend='both',use_gridspec=True)
#         cbar.set_label(cbar_label)       