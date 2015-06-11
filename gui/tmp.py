#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

import os
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import NavigationToolbar2, FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import Tkinter as Tk

class NavBar(NavigationToolbar2, Tk.Frame):
    """
    Public attributes

      canvas   - the FigureCanvas  (gtk.DrawingArea)
      win   - the gtk.Window
    """
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.window = window
        self._idle = True
        #Tk.Frame.__init__(self, master=self.canvas._tkcanvas)
        NavigationToolbar2.__init__(self, canvas)

    def destroy(self, *args):
        #del self.message
        Tk.Frame.destroy(self, *args)

    def set_message(self, s):
        self.message.set(s)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y0 =  height-y0
        y1 =  height-y1
        try: self.lastrect
        except AttributeError: pass
        else: self.canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.canvas._tkcanvas.create_rectangle(x0, y0, x1, y1)

        #self.canvas.draw()

    def release(self, event):
        try: self.lastrect
        except AttributeError: pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect

    def set_cursor(self, cursor):
        pass
        #self.window.configure(cursor=cursord[cursor])

    def _Button(self, text, file, command, extension='.ppm'):
        #img_file = os.path.join(rcParams['datapath'], 'images', file + extension)
        #im = Tk.PhotoImage(master=self, file=img_file)
        b = Tk.Button(
            master=self, text=text, padx=2, pady=2, command=command)
        #b._ntimage = im
        b.pack(side=Tk.LEFT)
        return b

    def _init_toolbar(self):
        
        xmin, xmax = self.canvas.figure.bbox.intervalx
        height, width = 50, xmax-xmin
        Tk.Frame.__init__(self, master=self.window,
                          width=int(width), height=int(height),
                          borderwidth=2)

        #self.update()  # Make axes menu
        """
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                # spacer, unhandled in Tk
                pass
            else:
                button = self._Button(text=text, file=image_file,
                                   command=getattr(self, callback))
                #if tooltip_text is not None:
                    #ToolTip.createToolTip(button, tooltip_text)

        """
        self.message = Tk.StringVar(master=self)
        self._message_label = Tk.Label(master=self, textvariable=self.message)
        self._message_label.pack(side=Tk.RIGHT)
        self.pack(side=Tk.BOTTOM, fill=Tk.X)
        
        


    def configure_subplots(self):
        pass
    """
        toolfig = Figure(figsize=(6,3))
        window = Tk.Tk()
        canvas = FigureCanvasTkAgg(toolfig, master=window)
        toolfig.subplots_adjust(top=0.9)
        #tool =  SubplotTool(self.canvas.figure, toolfig)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        """

    def save_figure(self, *args):
        pass
        """
        #from six.moves import tkinter_tkfiledialog, tkinter_messagebox
        filetypes = self.canvas.get_supported_filetypes().copy()
        default_filetype = self.canvas.get_default_filetype()

        # Tk doesn't provide a way to choose a default filetype,
        # so we just have to put it first
        default_filetype_name = filetypes[default_filetype]
        del filetypes[default_filetype]

        sorted_filetypes = list(six.iteritems(filetypes))
        sorted_filetypes.sort()
        sorted_filetypes.insert(0, (default_filetype, default_filetype_name))

        tk_filetypes = [
            (name, '*.%s' % ext) for (ext, name) in sorted_filetypes]

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        #defaultextension = self.canvas.get_default_filetype()
        defaultextension = ''
        initialdir = rcParams.get('savefig.directory', '')
        initialdir = os.path.expanduser(initialdir)
        initialfile = self.canvas.get_default_filename()
        fname = tkinter_tkfiledialog.asksaveasfilename(
            master=self.window,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            )

        if fname == "" or fname == ():
            return
        else:
            if initialdir == '':
                # explicitly missing key or empty str signals to use cwd
                rcParams['savefig.directory'] = initialdir
            else:
                # save dir for next time
                rcParams['savefig.directory'] = os.path.dirname(six.text_type(fname))
            try:
                # This method will handle the delegation to the correct type
                self.canvas.print_figure(fname)
            except Exception as e:
                tkinter_messagebox.showerror("Error saving file", str(e))
        """
    def set_active(self, ind):
        pass
        #self._ind = ind
        #self._active = [ self._axes[i] for i in self._ind ]

    def update(self):
        pass
        #_focus = windowing.FocusManager()
        #self._axes = self.canvas.figure.axes
        #naxes = len(self._axes)
        #if not hasattr(self, "omenu"):
        #    self.set_active(range(naxes))
        #    self.omenu = AxisMenu(master=self, naxes=naxes)
        #else:
        #    self.omenu.adjust(naxes)
        #NavigationToolbar2.update(self)

    def dynamic_update(self):
        'update drawing area only if idle'
        pass
        # legacy method; new method is canvas.draw_idle
        #self.canvas.draw_idle()

root = Tk.Tk()
root.wm_title("Embedding in TK")

thisPane = Tk.PanedWindow(root)
thisPane.pack()

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)

a.plot(t,s)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavBar( canvas, thisPane )
toolbar.update()

toolbar.pack(side=Tk.LEFT)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def on_key_event(event):
    print('you pressed %s'%event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.