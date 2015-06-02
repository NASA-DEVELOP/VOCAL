#!/opt/local/bin/python2.7
#
#   plot_vfm.py
#   Brian Magill
#   8/4/2014
#
#   An example of extracting and plotting VFM data using Python.
#
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
from findLatIndex import findLatIndex

from ccplot.hdf import HDF
import ccplot.utils

from vfm_row2block import vfm_row2block
from ConfigParser import SafeConfigParser
from PCF_genTimeUtils import calipsoISO_to_times, extractDatetime
import interpret_vfm_type as interpVFM

from uniform_alt_2 import uniform_alt_2
from regrid_lidar import regrid_lidar

#
#   The altitude range for the VFM data is
#   38 values less than for the other data sets.
#   The first 33 values above 20 km are left off
#   as well as the last 5, which are below 
#   sea level. 

ALT_LEN         = 545
FIRST_ALT_INDEX = 33
LAST_ALT_INDEX = -5

#   15 profiles are packed into 1 record of VFM data
#   At the highest altitudes 5 profiles are averaged 
#   together.  In the mid altitudes 3 are averaged and
#   at roughly 8 km or less, there are separate profiles.

PROF_PER_ROW    = 15

#argv = sys.argv

#if len(argv) != 2:

#    print "Usage: ", argv[0], " <VFM file>"
#    sys.exit() 
    
#vfm_file = argv[1]
vfm_file = "CAL_LID_L2_VFM-ValStage1-V3-02.2011-11-01T01-30-12ZD.hdf"

parser = SafeConfigParser()
parser.read('plot_vfm.ini')

file_prefix = parser.get('main', 'file_prefix')
revision    = parser.get('main', 'revision') 
colormap = parser.get('main', 'color_map') 


with HDF(vfm_file) as product:

    vfm_flags = product["Feature_Classification_Flags"][::]
    vfm_alt = product['metadata']['Lidar_Data_Altitudes'][FIRST_ALT_INDEX:LAST_ALT_INDEX:] 
    latitude = product["Latitude"][::]   

num_rows = vfm_flags.shape[0]

unpacked_vfm = np.zeros((ALT_LEN, PROF_PER_ROW*num_rows),dtype=np.uint8)

#   Look at overall feature types

vfm_types = interpVFM.extract_type(vfm_flags)

for i in range(num_rows):

    unpacked_vfm[:, PROF_PER_ROW*i:PROF_PER_ROW*(i+1) ] = vfm_row2block(vfm_types[i,:])

#start_lat = -30.
#end_lat = -80.

start_lat = parser.getfloat('main', 'start_latitude')
end_lat   = parser.getfloat('main', 'end_latitude')

if latitude[0] > latitude[-1]:

#   Nighttime granule

    min_indx = findLatIndex(start_lat, latitude)
    max_indx = findLatIndex(end_lat, latitude)

else:

#   Daytime granule

    min_indx = findLatIndex(end_lat, latitude)
    max_indx = findLatIndex(start_lat, latitude)


#start_lat = latitude[min_indx][0]
#end_lat   = latitude[max_indx][0]

#unpacked_vfm = unpacked_vfm[FIRST_ALT_INDEX:LAST_ALT_INDEX, min_indx*PROF_PER_ROW:max_indx*PROF_PER_ROW]
unpacked_vfm = unpacked_vfm[:, min_indx*PROF_PER_ROW:max_indx*PROF_PER_ROW]

#MAX_ALT = 30
MAX_ALT = parser.getfloat('main', 'max_altitude')

unif_alt = uniform_alt_2(MAX_ALT, vfm_alt)

#print "#### unif_alt.shape = ", unif_alt.shape
#print "#### vfm_alt.shape = ", vfm_alt.shape
#print "#### unpacked_vfm.shape = ", unpacked_vfm.shape

regrid_vfm = regrid_lidar(vfm_alt, unpacked_vfm, unif_alt, method='nearest')

granule = "%sZ%s" % extractDatetime(vfm_file)
title = 'VFM Features for granule %s' % granule

type_descr = interpVFM.Feature_Type
   
num_profs = unpacked_vfm.shape[1]                                                                   

min_alt = vfm_alt[-1]
max_alt = vfm_alt[0]

extents = [start_lat, end_lat, min_alt, max_alt]

#fig = plt.figure(figsize=(14,6))
fig = plt.figure(figsize=(16,6))


#cmap = ccplot.utils.cmap(colormap)
#cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
#plot_norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)


#imgplot = plt.imshow(regrid_vfm, aspect='auto', cmap=cm, norm=plot_norm, extent=extents)
imgplot = plt.imshow(regrid_vfm)
#plt.title(title)
#plt.xlabel('Latitude (degrees)')
#plt.ylabel('Altitude (km)')
#ax2 = fig.add_axes([0.92, 0.1, 0.02, 0.8])

#cbar = mpl.colorbar.ColorbarBase(ax2, cmap=cm, norm=plot_norm)

#color_list = ['Invalid', 'Clear Air', 'Cloud', 'Aerosol', 'Stratospheric', 'Surface', 'Subsurface', 'No Signal']
#for j, lab in enumerate(color_list):
#    cbar.ax.text(1.2, (2 * j + 1) / 16.0, lab, ha='left', va='center', size=10)

#cbar.ax.set_yticklabels([''])
#cbar.ax.tick_params(labelsize='small')


#cbar.ax.text(.5, (2 * j + 1) / 8.0, lab, ha='center', va='center')
#cbar.ax.get_yaxis().labelpad = -25

#
#output_file = "%s_%s_%s_vfm.png" % (file_prefix, revision, granule)
#print "#### output_file = ", output_file
#    plt.savefig("calipso_vfm_example.png")
#plt.savefig(output_file)

plt.show()
