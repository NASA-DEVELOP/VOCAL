################################
#   Created on Jul 9, 2015
#
#   @author: nqian
###############################
from Tkinter import Toplevel

import ccplot
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from constants import TIME_VARIANCE, ALTITUDE_VARIANCE

import matplotlib as mpl
import numpy as np
from tools.tools import interpolation_search


class ExtractDialog(Toplevel):
    """
    Displays a subplot containing the data bounded by a shape
    """

    def __init__(self, root, shape, filename, x_range, y_range):
        """
        Instantiates attributes
        
        :param: root: root Tk widget
        :param: shape: The shape that bounds the data
        :param: filename: The name of the file on display 
        """
        Toplevel.__init__(self, root)
        x_vals = [0, 3, 10, 15]
        y_vals = [232, 120, 45, 23]
        
        self.shape = shape
        self.filename = filename
        self.x_range = x_range
        self.y_range = y_range
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.plot = self.ax.plot(x_vals, y_vals, 'k-')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Altitude (km)')
        self.ax.set_title('%s' % shape.get_tag())
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0)
        self.title("Data Subplot")
        self.read_shape_data()
        
    def read_shape_data(self):
        cords = self.shape.get_coordinates()
        time_cords, altitude_cords = zip(*cords)
        x1 = self.x_range[0]
        x2 = self.x_range[1]
        h1 = self.y_range[0]
        h2 = self.y_range[1]
        nz = 500
        colormap = 'dat/calipso-backscatter.cmap'
        
        plot = self.shape.get_plot()
        with HDF(self.filename) as product:
            time = product['Profile_UTC_Time'][x1:x2, 0]
            height = product['metadata']['Lidar_Data_Altitudes']
            n_time = np.array([mpl.dates.date2num(ccplot.utils.calipso_time2dt(t)) for t in time])

            min_time = min(time_cords)
            max_time = max(time_cords)

            x1 = int(interpolation_search(n_time, min_time, TIME_VARIANCE))
            x2 = int(interpolation_search(n_time, max_time, TIME_VARIANCE))

            h1 = min(altitude_cords)
            h2 = max(altitude_cords)

            print h1, h2

            time = product['Profile_UTC_Time'][x1:x2, 0]
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
                               h2, h1, nz)

            cmap = ccplot.utils.cmap(colormap)
            cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
            cm.set_under(cmap['under']/255.0)
            cm.set_over(cmap['over']/255.0)
            cm.set_bad(cmap['bad']/255.0)
            norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
            
            self.ax.imshow(
                data.T,
                extent=(mpl.dates.date2num(time[0]), mpl.dates.date2num(time[-1]), h1, h2),
                cmap=cm,
                aspect='auto',
                norm=norm,
                interpolation='nearest'
            )
            
            self.ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))
