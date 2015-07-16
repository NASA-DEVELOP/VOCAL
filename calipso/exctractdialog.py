################################
#   Created on Jul 9, 2015
#
#   @author: nqian
#   @author: Grant Mercer
###############################
from Tkinter import Toplevel

import ccplot
from ccplot.algorithms import interp2d_12
from ccplot.hdf import HDF
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from constants import TIME_VARIANCE

import matplotlib as mpl
import numpy as np
from tools.tools import interpolation_search
from log import logger


# noinspection PyUnresolvedReferences
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
        logger.info('Opening ExtractDialog')
        Toplevel.__init__(self, root)
        self.geometry('+%d+%d' % (root.winfo_rootx(), root.winfo_rooty()))
        self.transient(root)

        self.__root = root
        self.shape = shape
        self.filename = filename
        self.x_range = x_range
        self.y_range = y_range
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Altitude (km)')
        self.ax.set_title('%s' % shape.get_tag())
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0)
        self.title('Data Subplot')

        x = self.__root.winfo_rootx() + self.winfo_x()*2
        y = self.__root.winfo_rooty()
        """
        self.histogram_window = Toplevel(self)
        self.histogram_window.geometry('+%d+%d' % (x, y))
        self.histogram_window.protocol('WM_DELETE_WINDOW', ExtractDialog.ignore)
        self.histogram_window.transient(self.__root)
        self.histogram_window.update()

        self.hist_fig = Figure(figsize=(8, 5))
        self.hist_ax = self.hist_fig.add_subplot(1, 1, 1)
        self.hist_ax.set_xlabel('Time')
        self.hist_ax.set_ylabel('Altitude (km)')

        self.hist_canvas = FigureCanvasTkAgg(self.hist_fig, master=self)
        self.hist_canvas.show()
        self.hist_canvas.get_tk_widget().grid(row=0)
        self.histogram_window.title('Histogram')
        """
        logger.info('Reading shape data')
        self.read_shape_data()

    @staticmethod
    def ignore():
        pass
        
    def read_shape_data(self):
        """
        Read coordinate data from the shape to determine the new bounds of the subplot.
        Shape bounds are taken with simple ``max()`` and ``min()`` functions, however
        determining their location within the time array is much more difficult as matplotlib
        only handles *real* locations, not relative to the numpy data arrays. To solve this
        issue an algorithm called ``interpolation_search`` is used, which computes the nearest
        time coordinate for bounding, and with a complexity of only ``O(log log(n))``
        """

        cords = self.shape.get_coordinates()
        time_cords, altitude_cords = zip(*cords)
        print self.x_range
        x1 = self.x_range[0]
        x2 = self.x_range[1]
        h1 = min(altitude_cords)
        h2 = max(altitude_cords)
        nz = 500
        colormap = 'dat/calipso-backscatter.cmap'

        # TODO Show correct plot when depolarized starts working
        plot = self.shape.get_plot()
        with HDF(self.filename) as product:
            time = product['Profile_UTC_Time'][x1:x2, 0]
            height = product['metadata']['Lidar_Data_Altitudes']
            dataset = product['Total_Attenuated_Backscatter_532'][x1:x2]
            n_time = np.array([mpl.dates.date2num(ccplot.utils.calipso_time2dt(t)) for t in time])

            min_time = min(time_cords)
            max_time = max(time_cords)

            logger.info("Applying search algorithm to determine shape bounds")
            x1 = int(interpolation_search(n_time, min_time, TIME_VARIANCE))
            x2 = int(interpolation_search(n_time, max_time, TIME_VARIANCE))

            logger.info("Setting bounds for new subplot")
            time = time[x1:x2]
            dataset = dataset[x1:x2]
            time = np.array([ccplot.utils.calipso_time2dt(t) for t in time])

            dataset = np.ma.masked_equal(dataset, -9999)
            _x = np.arange(x1, x2, dtype=np.float32)
            _z, null = np.meshgrid(height, _x)
            data = interp2d_12(
                dataset[::],
                _x.astype(np.float32),
                _z.astype(np.float32),
                x1, x2, x2 - x1,
                h2, h1, nz)

            cmap = ccplot.utils.cmap(colormap)
            cm = mpl.colors.ListedColormap(cmap['colors']/255.0)
            cm.set_under(cmap['under']/255.0)
            cm.set_over(cmap['over']/255.0)
            cm.set_bad(cmap['bad']/255.0)
            norm = mpl.colors.BoundaryNorm(cmap['bounds'], cm.N)

            logger.info("Setting colormap, displaying")
            self.ax.imshow(
                data.T,
                extent=(mpl.dates.date2num(time[0]), mpl.dates.date2num(time[-1]), h1, h2),
                cmap=cm,
                aspect='auto',
                norm=norm,
                interpolation='nearest'
            )
            
            self.ax.get_xaxis().set_major_formatter(mpl.dates.DateFormatter('%H:%M:%S'))

