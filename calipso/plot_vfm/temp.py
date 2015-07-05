"""
Demo of image that's been clipped by a circular patch.
"""
'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook

image_file = cbook.get_sample_data('grace_hopper.png')
image = plt.imread(image_file)

fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((260, 200), radius=200, transform=ax.transData)
im.set_clip_path(patch)

plt.axis('off')
plt.show()
'''


import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from numpy import arange, sin, pi
from matplotlib.figure import Figure
import Tkinter as Tk

root = Tk.Tk()

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

points = [[2, 1], [4, 5], [3, 2], [2, 1]]
polygon = plt.Polygon(points)

a.add_patch(polygon)
a.plot(t, s)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

button = Tk.Button(master=root, text='Quit')
button.pack(side=Tk.BOTTOM)

Tk.mainloop()