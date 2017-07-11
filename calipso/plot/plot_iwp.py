# Andrea Martinez
# Brian Magill
# 8/11/2014
#
import ccplot.utils
import numpy as np
import matplotlib as mpl
from ccplot.hdf import HDF
from vfm_row2block import vfm_row2block
from uniform_alt_2 import uniform_alt_2
from regrid_lidar import regrid_lidar
from interpret_vfm_type import extract_water_phase

def render_iwp(filename, x_range, y_range, fig, pfig):
    """
    Renders the Vertical Feature Mask on the current plot. Note that L2 data is organized
    differently than L1. See comments below and the CALIPSO data product catalogue for more
    information before editing

    :param filename: L2 HDF file
    :param x_range: Tuple of first and last profile index to load from ToolsWindow
    :param y_range: Tuple of first and last altitude index to load from ToolsWindow
    :param fig: Matplotlib backend object
    :param pfig: Matplotlib backend object
    """

    # 15 profiles are in 1 record of VFM data. At the highest altitudes 5 profiles are averaged
    # together. In the mid altitudes 3 are averaged and at roughly 8 km or less, there are
    # separate profiles.
    prof_per_row = 15

    # constant variables
    alt_len = 545
    first_alt = y_range[0]
    last_alt = y_range[1]
    first_lat = int(x_range[0]/prof_per_row)
    last_lat = int(x_range[1]/prof_per_row)
    colormap = 'dat/calipso-icewaterphase.cmap'

    # naming products within the HDF file
    with HDF(filename) as product:
        time = product['Profile_UTC_Time'][first_lat:last_lat, 0]
        minimum = min(product['Profile_UTC_Time'][::])[0]
        maximum = max(product['Profile_UTC_Time'][::])[0]

        # Determine how far the file can be viewed
        if time[-1] >= maximum and len(time) < 950:
            raise IndexError
        if time[0] < minimum:
            raise IndexError

        height = product['metadata']['Lidar_Data_Altitudes'][33:-5:]
        dataset = product['Feature_Classification_Flags'][first_lat:last_lat]
        latitude = product['Latitude'][first_lat:last_lat, 0]
        latitude = latitude[::prof_per_row]
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])

        # Mask all unknown values
        dataset = np.ma.masked_equal(dataset, -999)

        # Give the number of rows in the dataset
        num_rows = dataset.shape[0]

        # Create an empty array the size of of L1 array so they match on the plot
        unpacked_iwp = np.zeros((alt_len, prof_per_row * num_rows), np.uint8)

        # Assign the values from 0-7 to subtype
        iwp = extract_water_phase(dataset)

        # Place 15-wide, alt_len-tall blocks of data into the
        for i in range(num_rows):
            unpacked_iwp[:, prof_per_row * i:prof_per_row * (i + 1)] = vfm_row2block(iwp[i, :])

        # Determine if day or nighttime
        if latitude[0] >latitude[-1]:
            print('Nighttime')
            iwp = np.flip(unpacked_iwp[:, (first_lat * prof_per_row):(last_lat * prof_per_row)], 1)

        else:
            print('Daytime')
            iwp = unpacked_iwp[:, (first_lat*prof_per_row):(last_lat*prof_per_row)]

        max_alt = 20
        unif_alt = uniform_alt_2(max_alt, height)
        regrid_iwp = regrid_lidar(height, iwp, unif_alt)

        # Format color map
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors'] / 255.0)
        cm.set_under(cmap['under'] / 255.0)
        cm.set_over(cmap['over'] / 255.0)
        cm.set_bad(cmap['bad'] / 255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

        im = fig.imshow(
            regrid_iwp,
            extent=(latitude[0], latitude[-1], first_alt, last_alt),
            cmap=cm,
            aspect='auto',
            norm=norm,
            interpolation='nearest',
        )

        fig.set_ylabel('Altitude (km)')
        fig.set_xlabel('Latitude')
        fig.set_title("Ice Water Phase")

        cbar_label = 'Ice Water Phase'
        cbar = pfig.colorbar(im)
        cbar.set_label(cbar_label)
        cbar.ax.set_yticklabels(['N/a', 'Unknown', 'Ice', 'Water', 'Oriented Ice'])

        ax = fig.twiny()
        ax.set_xlabel('Time')
        ax.set_xlim(time[0], time[-1])
        ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))

        fig.set_zorder(0)
        ax.set_zorder(1)

        title = fig.set_title('Ice Water Phase')
        title_xy = title.get_position()
        title.set_position([title_xy[0], title_xy[1] * 1.07])

        return ax