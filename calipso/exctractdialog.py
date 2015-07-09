################################
#Created on Jul 9, 2015
#
#@author: nqian
###############################
from Tkinter import Toplevel, Frame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tkconstants import TOP, BOTH


class ExtractDialog(Toplevel):
    """
    Displays a subplot containing the data bounded by a shape
    """


    def __init__(self, root, shape):
        """
        Instantiates attributes
        """
        Toplevel.__init__(self, root)
        self.shape = shape
        self.draw_frame = Frame(root)
        self.parent_fig = Figure(figsize=(8, 5))
        self.fig = self.parent_fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasTkAgg(self.parent_fig, master=self.draw_frame)
        
        self.title("Data Subplot")
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.draw_frame.pack()
        self.canvas.show()