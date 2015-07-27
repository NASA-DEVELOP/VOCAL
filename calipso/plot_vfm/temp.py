import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import numpy as np

def onclick(event):
    print event.xdata, event.ydata
    print y.transData.inverted().transform(a.transData.transform(np.array([event.xdata, event.ydata])))

root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

a.plot(t,s)

y = a.twiny()

a.set_zorder(1)
y.set_zorder(0)

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas.mpl_connect('button_press_event', onclick)

Tk.mainloop()
