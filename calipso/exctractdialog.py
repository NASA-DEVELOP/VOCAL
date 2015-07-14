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
        self.ax.set_title('Shape Subplot')
        
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
        colormap = 'dat/calipso-backscatter.cmap'
        
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
            second = []
#             test = np.ma.masked_equal(test, 0)

            bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
            width, height = bbox.width, bbox.height
            width *= self.fig.dpi
            height *= self.fig.dpi
            
            print "Pixel height: ", height
            
            min_x = min(self.shape.get_coordinates(), key=lambda x: x[0])
            max_x = max(self.shape.get_coordinates(), key=lambda x: x[0])
            min_y = min(self.shape.get_coordinates(), key=lambda y: y[1])
            max_y = max(self.shape.get_coordinates(), key=lambda y: y[1])
            min_xindex, min_yindex, max_xindex, max_yindex = 0, 0, 0, 0
            
            i = 0
            j = 0
            # TODO: trim data outside of the shape
            for x in range(x1, x2):
                if self.shape.in_x_extent(time[x]):
                    second.append([])
                    if abs(time[x] - min_x[0]) >= 0.00001:
                        min_xindex = x
                    elif abs(time[x] - max_x[0]) >= 0.00001:
                        max_xindex = x
                    for y in range(h1, h2):
                        # check if (i, j) is inside the shape with ray casting
                        # exclude points on the lines
#                         test = np.ma.masked_where(ray_cast(self.shape.get_coordinates(), (time[i], j)), data)
                        if ray_cast(self.shape.get_coordinates(), (time[x], y)):
                            if abs(y - min_y[1]) >= 0.00001:
                                min_yindex = y
                            elif abs(y - max_y[1]) >= 0.00001:
                                max_yindex = y
#                             print data[i][j]
                            test[x][y] = 1
#                             print "(%s, %s)" %(x, y)
                            second[i].append(data[x][y])
                            j += 1
                    i += 1
                            
#             data = np.ma.masked_where(test == 0.0, data)
            print data
            
            cmap = ccplot.utils.cmap(colormap)
            cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
            cm.set_under(cmap['under']/255.0)
            cm.set_over(cmap['over']/255.0)
            cm.set_bad(cmap['bad']/255.0)
            norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)
            
            print time[min_yindex]
            print time[max_yindex]
            
            im = self.ax.imshow(
                data.T,
                extent=(time[min_xindex], time[max_xindex], min_yindex, max_yindex), 
                cmap=cm,
                aspect='auto',
                norm=norm,
                interpolation='nearest'
            )
            
            self.ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))