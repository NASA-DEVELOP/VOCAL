"""
Demo of image that's been clipped by a circular patch.
"""

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from Tkinter import Tk, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

class min_example(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self, root)
        self.geometry('+%d+%d' % (200, 200))
        self.title('TEST')
        self.transient(root)

        self.__root = root
        self.fig = Figure(figsize=(8, 5))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Altitude (km)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.create_win()

    def create_win(self):

        time.sleep(2)

        test_win = Toplevel(self)
        test_win.title('LAGS')
        test_win.geometry('+%d+%d' % (800, 800))
        test_win.transient(self.__root)


rt = Tk()
rt.title('ROOT')
min_example(rt)
rt.mainloop()
