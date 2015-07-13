################################
#Created on Jul 9, 2015
#
#@author: nqian
###############################
from Tkinter import Toplevel

import ccplot
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import matplotlib as mpl
import numpy as np
from tools.linearalgebra import ray_cast


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
        self.ax.set_title('Horse Stable')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0)
#         toolbar = NavigationToolbar2TkAgg(self.canvas, self)
#         toolbar.grid(row=1)
#         toolbar.update()
        self.title("Data Subplot")
        self.read_shape_data()
        
    def read_shape_data(self):
        x1 = self.x_range[0]
        x2 = self.x_range[1]
        h1 = self.y_range[0]
        h2 = self.y_range[1]
        nz = 500
        
        plot = self.shape.get_plot()
        with HDF(self.filename) as product:
            time = product['Profile_UTC_Time'][x1:x2, 0]
            height = product['metadata']['Lidar_Data_Altitudes']
            dataset = product['Total_Attenuated_Backscatter_532'][x1:x2]
            
            time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])
            for i in range(len(time)):
                time[i] = mpl.dates.date2num(time[i])
            dataset = np.ma.masked_equal(dataset, -9999)
            X = np.arange(x1, x2, dtype=np.float32)
            Z, null = np.meshgrid(height, X)
            data = interp2d_12(
                               dataset[::],
                               X.astype(np.float32),
                               Z.astype(np.float32),
                               x1, x2, x2 - x1,
                               h2, h1, nz)
            test = np.empty_like(data)
#             test = np.ma.masked_equal(test, 0)
            
            for i in range(x1, x2):
                if self.shape.in_x_extent(time[i]):
                    for j in range(h1, h2):
                        # check if (i, j) is inside the shape with ray casting
                        # exclude points on the lines
#                         test = np.ma.masked_where(ray_cast(self.shape.get_coordinates(), (time[i], j)), data)
                        if ray_cast(self.shape.get_coordinates(), (time[i], j)):
#                             print data[i][j]
                            test[i][j] = 1
                            print test[i][j]
                            pass
            print test
#             print data