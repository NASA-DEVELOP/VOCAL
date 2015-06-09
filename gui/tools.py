"""
    tools.py
    @author: Grant Mercer
    6/3/2015

    a set of tools that can be used to simplify the means of creating out GUI program
    CONTENTS:
        L18 -> ToolTip                     A class that creates tiny tool tip windows when a mouse hovered
                                           over a button, useful for button with no text and rather images
        L69 -> ToggleableButton            A wrapper class for Button that allows for quick and easy
                                           creation of buttons that remain sunken until reclicked, and
                                           allows for a bind map to bind any keys to functions once 
                                           toggled
        L134 -> ToolbarToggleableButton    A wrapper FOR a wrapper , a bit confusing but simply put it 
                                           allows simple declarations of toggleable buttons that do not
                                           require binds. This is for the Matplotlib backend buttons, as
                                           they bind the mouse buttons internally thus we only need to call
                                           a function when toggled
        L144 -> NavigationToolbar2CALIPSO  A custom implementation of NavigationToolbar2TkAgg, inherits from
                                           the matplotlib backend and purposely does not implement the GUI
                                           for the toolbar, instead we custom create our own buttons in the
                                           main program implementation
"""

import matplotlib
matplotlib.use('TkAgg')
from Tkinter import TclError, Label, LEFT, SOLID, Toplevel, Button, RAISED, \
    SUNKEN, Message
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
class ToggleableButton(Button, object):

    # static class container to keep track of all active and unactive buttons
    # currently living
    __toggleContainer = []
    
    # Parameters:
    #    root        -> the root of the program, which handles the cursor
    #    master      -> the parent of the actual button 
    #    cnf         -> button forward args
    #    kw          -> button forward args
    def __init__(self, root, master=None, cnf={}, **kw):
        self.__bindMap = []         # bind map to be bound once toggled
        self.isToggled = False      # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ""          # cursor private var
        self.__destructor = None    # destructor var called when untoggled
        self.__master = master
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.Toggle)         # button command is always bound internally to toggle
        self.__toggleContainer.append(self)         # push button to static container
        
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

    # Clone to toggle, except the only functionality of unToggle is to forceably
    #    untoggle the button and set the state accordingly
    def unToggle(self):
        self.isToggled = False
        self.config(relief='raised')
        for pair in self.__bindMap:
            pair[0].unbind(pair[1])
        if self.__destructor : self.__destructor()

    # The bread and potatos of the class, __Toggle uses a boolean variable to keep track
    #    of the current state of the class and will toggle the button accordingly. Addtionally,
    def Toggle(self):
        # first flip the toggle switch
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them and set their state
        for s in [x for x in self.__toggleContainer if x.isToggled == True and x is not self]:
            s.unToggle()

        # else if next state it false
        if self.isToggled == False:
            self.config(relief='raised')
            for pair in self.__bindMap: 
                pair[0].unbind(pair[1])
            if self.__destructor : self.__destructor
        # else if next state is true
        else:
            self.config(relief='sunken')
            for pair in self.__bindMap:
                pair[0].bind(pair[1], pair[2])
            


class ToolbarToggleableButton(ToggleableButton):
    def __init__(self, root, master=None, func=None, cnf={}, **kw):
        ToggleableButton.__init__(self, root, master, kw)
        self.configure(command=self.__toggle)
        self.__func = func
        
    def __toggle(self, toggle=False):
        if self.__func : self.__func()
        super(ToolbarToggleableButton, self).Toggle()

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
    
def createToolBarToggle(master, cnf={}, **kw):
        button = Button(master, kw)
        
        return button

class ref:
    def __init__(self, val):
        self._value = val
        
    def get(self):
        return self._value
    
    def set(self, val):
        self._value = val