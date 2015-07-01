#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from ccplot.hdf import HDF
from ccplot.algorithms import interp2d_12
import ccplot.utils

filename = 'C:/Users/nqian/Desktop/CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf'
name = 'Total_Attenuated_Backscatter_532'
label = 'Total Attenuated Backscatter 532nm (km$^{-1}$ sr$^{-1}$)'
colormap = 'C:/Users/nqian/git/Calipso_Visualization/calipso/dat/calipso-backscatter.cmap'
x1 = 0
x2 = 1000
h1 = 0  # km
h2 = 20  # km
nz = 500  # Number of pixels in the vertical.

if __name__ == '__main__':
    with HDF(filename) as product:
        # Import datasets.
        time = product['Profile_UTC_Time'][x1:x2, 0]
        height = product['metadata']['Lidar_Data_Altitudes']
        dataset = product[name][x1:x2]

        # Convert time to datetime.
        time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])

        # Mask missing values.
        dataset = np.ma.masked_equal(dataset, -9999)

        # Interpolate data on a regular grid.
        X = np.arange(x1, x2, dtype=np.float32)
        Z, null = np.meshgrid(height, X)
        data = interp2d_12(
            dataset[::],
            X.astype(np.float32),
            Z.astype(np.float32),
            x1, x2, x2 - x1,
            h2, h1, nz,
        )

        # Import colormap.
        cmap = ccplot.utils.cmap(colormap)
        cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
        cm.set_under(cmap['under']/255.0)
        cm.set_over(cmap['over']/255.0)
        cm.set_bad(cmap['bad']/255.0)
        norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

        # Plot figure.
        fig = plt.figure(figsize=(12, 6))
        TIME_FORMAT = '%e %b %Y %H:%M:%S UTC'
        im = plt.imshow(
            data.T,
            extent=(mpl.dates.date2num(time[0]), mpl.dates.date2num(time[-1]), h1, h2),
            cmap=cm,
            norm=norm,
            aspect='auto',
            interpolation='nearest',
        )
        ax = im.axes
        ax.set_title('CALIPSO')
        ax.set_xlabel('Time')
        ax.set_ylabel('Altitude (km)')
        ax.xaxis.set_major_locator(mpl.dates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
        cbar = plt.colorbar(
            extend='both',
            use_gridspec=True
        )
        cbar.set_label(label)
        fig.tight_layout()
        plt.savefig('calipso-plot.png')
        plt.show()
