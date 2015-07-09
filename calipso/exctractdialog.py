################################
#Created on Jul 9, 2015
#
#@author: nqian
###############################
from Tkinter import Toplevel

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class ExtractDialog(Toplevel):
    """
    Displays a subplot containing the data bounded by a shape
    """


    def __init__(self, root, shape):
        """
        Instantiates attributes
        """
        Toplevel.__init__(self, root)
        x_vals = [0, 3, 10, 15]
        y_vals = [232, 120, 45, 23]
        
        self.shape = shape
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.plot = self.ax.plot(x_vals, y_vals, 'k-')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Altitude (km)')
        self.ax.set_title('Horse Stable')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.grid(row=1)
        toolbar.update()
        
        self.title("Data Subplot")