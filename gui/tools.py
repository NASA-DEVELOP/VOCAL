#
#   tools.py
#   Grant Mercer
#   6/3/2015
#
#   a set of tools that can be used to simplify the means of creating out GUI program
#
import matplotlib
matplotlib.use('TkAgg')
from Tkinter import TclError, Label, LEFT, SOLID, Toplevel, Button, RAISED, \
    SUNKEN
import tkFileDialog
from matplotlib.backends.backend_tkagg import NavigationToolbar2

# Allows for tool tips to be displayed just below buttons
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    # Parameter: text to display as tooltip
    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    
# Button wrapper which simulates the toggled button as you see in the draw, magnify, etc. 
#    buttons. Interally keeps a bind map which on toggle binds the keys in the map, and 
#    unbinds them on untoggle or forced untoggle.
class ToggleableButton(Button):

    
    def __init__(self, root, master=None, cnf={}, **kw):
        self.__bindMap = []         # bind map to be bound once toggled
        self.__isToggled = False    # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ""          # cursor private var
        self.__destructor = None    # destructor var called when untoggled
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.__Toggle)       # button command is always bound internally to toggle

    # Parameters: 
    #    key         -> a string which accepts a valid Tkinter key
    #    command     -> the command to be bound to string
    #    cursor      -> the cursor to be set when toggled
    #    destructor  -> a function called when untoggled
    def latch(self, key="", command=None, cursor="", destructor=None):
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor
        if key != "" and command != None : self.__bindMap.append((self.__root, key, command))
        if destructor != None : self.__destructor = destructor

    # Wrapper function to call the private toggle function. As the design of 
    #    toggleable button was to internalize this method, we keep it private
    def unToggle(self):
        self.__Toggle(toggle=True)

    # The bread and potatos of the class, __Toggle uses a boolean variable to keep track
    #    of the current state of the class and will toggle the button accordingly. Addtionally,
    #    the unToggle function will forcefully untoggle by setting the toggle var to True, this
    #    is useful if you wish to set binds where the button untoggles outside of the button
    #    just being clicked a second time
    def __Toggle(self, toggle=False):
        if toggle:
            self.__root.config(cursor="")
            for pair in self.__bindMap: 
                pair[0].unbind(pair[1])
            self.config(relief=RAISED)
            if self.__destructor : self.__destructor()
        else:
            self.__isToggled = not self.__isToggled
            if self.__isToggled:
                self.__root.config(cursor=self.__cursor)
                self.config(relief=SUNKEN)
                for pair in self.__bindMap:
                    pair[0].bind(pair[1], pair[2])
                self.__root.grab_set()
            else:
                for pair in self.__bindMap:
                    pair[0].unbind(pair[1])
                self.__root.config(cursor="")
                self.config(relief=RAISED)
                if self.__destructor : self.__destructor()

class NavigationToolbar2CALIPSO(NavigationToolbar2):
    def __init__(self, canvas):
        NavigationToolbar2.__init__(self, canvas)
        
    def _init_toolbar(self):
        pass

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y0 =  height-y0
        y1 =  height-y1
        try: self.lastrect
        except AttributeError: pass
        else: self.canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.canvas._tkcanvas.create_rectangle(x0, y0, x1, y1)
        
    def release(self, event):
        try: self.lastrect
        except AttributeError: pass
        else:
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
        
    def set_cursor(self, event):
        pass
    
    def save_figure(self, *args):
        pass
    
    def configure_subplots(self):
        pass
    
    def set_active(self, ind):
        pass
    
    def update(self):
        NavigationToolbar2.update(self)

    def dynamic_update(self):
        pass
