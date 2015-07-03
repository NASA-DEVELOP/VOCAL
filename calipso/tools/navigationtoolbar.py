######################################
#    navigationtoolbar.py
#    @author: Grant Mercer
#    @author: Nathan Qian
#    6/24/2015
######################################

from Tkinter import StringVar, Label
from matplotlib.backends.backend_tkagg import NavigationToolbar2

import numpy as np


# noinspection PyProtectedMember
class NavigationToolbar2CALIPSO(NavigationToolbar2):
    """
    Custom toolbar derived from matplotlib.backend, since we won't be specifically displaying
    any of their provided TkGUI, we will be creating our own GUI outside of the toolbar and
    simply using the functions provided by NavigationToolbar2. Thus we strip the toolbar of
    anything GUI related

    :param canvas: The main canvas of the application that will be drawn to
    :param master: The master program (Calipso)
    """
    
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.master = master
        self.lastrect = None
        NavigationToolbar2.__init__(self, canvas)
        
    def _init_toolbar(self):
        """
        Sets a string var which self updates with the coordinates of the cursor
        relative to the plot
        """
        self.message = StringVar(master=self.master)
        self._message_label = Label(master=self.master, textvariable=self.message)
        self._message_label.grid(row=3, column=1)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        """
        Draws a rectangle rubber band to indicate area that will be zoomed in on

        :param event: Tkinter passed event object
        :param x0: top left x coordinate
        :param y0: top left y coordinate
        :param x1: bottom right x coordinate
        :param y1: bottom right y coordinate
        """
        height = self.canvas.figure.bbox.height
        y0 = height-y0
        y1 = height-y1
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)

        self.lastrect = self.canvas._tkcanvas.create_rectangle(x0, y0, x1, y1)
        
    def release(self, event):
        """
        Upon mouse release while zooming, the rectangle is deleted and the
        application is zoomed to that view

        :param event: Tkinter passed event object
        """
        try:
            self.lastrect
        except AttributeError:
            pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
        
    def set_message(self, s):
        """
        Set the message of the stringvar

        :param str s: String to set
        """
        self.message.set(s)
        
    def set_cursor(self, event):
        pass
    
    def save_figure(self, *args):
        pass
    
    def configure_subplots(self):
        pass
    
    def set_active(self, ind):
        pass
    
    def update(self):
        """
        Call the base class update function
        """
        NavigationToolbar2.update(self)

    def dynamic_update(self):
        pass

    # noinspection PyTypeChecker,PyUnusedLocal
    def release_zoom(self, event):
        """
        the release mouse button callback in zoom to rect mode, upon
        release the plot will zoom to the location of the rectangle

        :param event: Tkinter passed event object
        """
        for zoom_id in self._ids_zoom:
            self.canvas.mpl_disconnect(zoom_id)
        self._ids_zoom = []

        if not self._xypress:
            return

        last_a = []

        for cur_xypress in self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, ind, lim, trans = cur_xypress  # @UnusedVariable
            # ignore singular clicks - 5 pixels is a threshold
            if abs(x - lastx) < 5 or abs(y - lasty) < 5:
                self._xypress = None
                self.release(event)
                self.draw()
                return

            x0, y0, x1, y1 = lim.extents

            # zoom to rect
            inverse = a.transData.inverted()
            lastx, lasty = inverse.transform_point((lastx, lasty))
            x, y = inverse.transform_point((x, y))
            x_min, x_max = a.get_xlim()
            y_min, y_max = a.get_ylim()

            # detect twinx,y axes and avoid double zooming
            twinx, twiny = False, False
            if last_a:
                for la in last_a:
                    if a.get_shared_x_axes().joined(a, la):
                        twinx = True
                    if a.get_shared_y_axes().joined(a, la):
                        twiny = True
            last_a.append(a)

            if twinx:
                x0, x1 = x_min, x_max
            else:
                if x_min < x_max:
                    if x < lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 < x_min:
                        x0 = x_min
                    if x1 > x_max:
                        x1 = x_max
                else:
                    if x > lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 > x_min:
                        x0 = x_min
                    if x1 < x_max:
                        x1 = x_max

            if twiny:
                y0, y1 = y_min, y_max
            else:
                if y_min < y_max:
                    if y < lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 < y_min:
                        y0 = y_min
                    if y1 > y_max:
                        y1 = y_max
                else:
                    if y > lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 > y_min:
                        y0 = y_min
                    if y1 < y_max:
                        y1 = y_max

            if self._button_pressed == 1:
                if self._zoom_mode == 'x':
                    a.set_xlim((x0, x1))
                elif self._zoom_mode == 'y':
                    a.set_ylim((y0, y1))
                else:
                    a.set_xlim((x0, x1))
                    a.set_ylim((y0, y1))
            elif self._button_pressed == 3:
                if a.get_xscale() == 'log':
                    alpha = np.log(x_max / x_min) / np.log(x1 / x0)
                    rx1 = pow(x_min / x0, alpha) * x_min
                    rx2 = pow(x_max / x0, alpha) * x_min
                else:
                    alpha = (x_max - x_min) / (x1 - x0)
                    rx1 = alpha * (x_min - x0) + x_min
                    rx2 = alpha * (x_max - x0) + x_min
                if a.get_yscale() == 'log':
                    alpha = np.log(y_max / y_min) / np.log(y1 / y0)
                    ry1 = pow(y_min / y0, alpha) * y_min
                    ry2 = pow(y_max / y0, alpha) * y_min
                else:
                    alpha = (y_max - y_min) / (y1 - y0)
                    ry1 = alpha * (y_min - y0) + y_min
                    ry2 = alpha * (y_max - y0) + y_min

                if self._zoom_mode == 'x':
                    a.set_xlim((rx1, rx2))
                elif self._zoom_mode == 'y':
                    a.set_ylim((ry1, ry2))
                else:
                    a.set_xlim((rx1, rx2))
                    a.set_ylim((ry1, ry2))

        self.draw()
        self._xypress = None
        self._button_pressed = None

        self._zoom_mode = None

        self.push_current()
        self.release(event)
    
    def zoom(self, *args):
        """
        Caller function for activating and deactivating zoom mode
        """
        if self._active == 'ZOOM':
            self._active = None
        else:
            self._active = 'ZOOM'

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''

        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if self._active:
            self._idPress = self.canvas.mpl_connect('button_press_event',
                                                    self.press_zoom)
            self._idRelease = self.canvas.mpl_connect('button_release_event',
                                                      self.release_zoom)
            self.mode = 'zoom rect'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)