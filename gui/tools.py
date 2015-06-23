"""
    tools.py
    @author: Grant Mercer
    6/3/2015

"""
from Tkinter import TclError, Label, LEFT, SOLID, Toplevel, Button, \
    StringVar, YES, BOTH, Scrollbar, Y,\
     X, VERTICAL, NO, RIGHT, BOTTOM, HORIZONTAL \
     
import re
import numpy as np
import ttk
import tkFont
    
from matplotlib.backends.backend_tkagg import NavigationToolbar2

toggleContainer = []

class ToolTip(object):
    '''
    Allows for tool tips to be displayed just below buttons
    '''
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.x = self.y = 0

    # Parameter: text to display as tooltip
    def showTip(self, text):
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")  # @UnusedVariable
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipWindow = tw = Toplevel(self.widget)
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

    def hideTip(self):
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showTip(text)
    def leave(event):
        toolTip.hideTip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    

class ToggleableButton(Button):
    '''
    Button wrapper which simulates the toggled button as you see in the draw, magnify, etc. 
    buttons. Interally keeps a bind map which on toggle binds the keys in the map, and 
    unbinds them on untoggle or forced untoggle.
    '''
    # static class container to keep track of all active and unactive buttons
    # currently living
    
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
        self.configure(command=self.toggle)         # button command is always bound internally to toggle
        toggleContainer.append(self)         # push button to static container
        
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

    # The toggle function ensures that the button is either correctly toggled, or not. The
    #    button command is bound here and additionally any functions 'latched' to a command
    #    will be binded here when toggled. Also internally ensures no two toggled buttons can
    #    exist at any one time
    def toggle(self):
        # first flip the toggle switch
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.isToggled == True and x is not self]:  
            s.unToggle()
            
        # else if next state it false
        if self.isToggled == False:
            self.config(relief='raised')                # raise the button, e.g. deactivated
            for pair in self.__bindMap:                 # unbind using the bindmap
                pair[0].unbind(pair[1])
            if self.__destructor : self.__destructor()  # call the pseudo 'destructor'
        # else if next state is true
        else:
            self.config(relief='sunken')                # sink the button, e.g. activate
            for pair in self.__bindMap:                 # bind using the bindmap
                pair[0].bind(pair[1], pair[2])



class ToolbarToggleableButton(Button):
    '''
    Wrapper of a wrapper of a button, it's a mouthful but it useful for having 
    additional functionality the matplotlib buttons would require. Instead
    of placing more overhead in the ToggleableButton another class is created 
    since the number of matplotlib functions will remain constant, while we
    may continue creating new tools that use ToggleableButton
    '''
    # Parameters: 
    #    root, master, cnf, kw    -> forwarded args to the ToggleableButton class
    #    func                     -> function to be called along with the invocation of Toggle
    def __init__(self, root, master=None, func=None, cnf={}, **kw):
        self.isToggled = False      # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ""          # cursor private var
        self.__master = master
        self.__func = func
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.toggle)         # button command is always bound internally to toggle
        toggleContainer.append(self)         # push button to static container
        
    def latch(self, cursor=""):
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor
        
    # Clone to toggle, except the only functionality of unToggle is to forceably
    #    untoggle the button and set the state accordingly
    def unToggle(self):
        self.isToggled = False
        self.config(relief='raised')
        if self.__func : self.__func()
        
    # Call the super classes Toggle, and execute our function as well
    def toggle(self):
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.isToggled == True and x is not self]:  
            s.unToggle()
        
        # first flip the toggle switch
        if self.__func : self.__func()
        # else if next state it false
        if self.isToggled == False:
            self.config(relief='raised')                # raise the button, e.g. deactivated
            self.__root.config(cursor="")
        # else if next state is true
        else:
            self.__root.config(cursor=self.__cursor)
            self.config(relief='sunken')                # sink the button, e.g. activate
            

class NavigationToolbar2CALIPSO(NavigationToolbar2):
    '''
    Custom toolbar derived from matplotlib.backend, since we won't be specifically displaying
    any of their provided TkGUI, we will be creating our own GUI outside of the toolbar and
    simply using the functions provided by NavigationToolbar2. Thus we strip the toolbar of
    anything GUI related 
    '''
    
    def __init__(self, canvas, master, observer):
        self.canvas = canvas
        self.master = master
        self.observer = observer
        NavigationToolbar2.__init__(self, canvas)
        
    def _init_toolbar(self):
        self.message = StringVar(master=self.master)
        self._message_label = Label(master=self.master, textvariable=self.message)
        self._message_label.grid(row=3, column=1)

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
        
    def set_message(self, s):
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
        NavigationToolbar2.update(self)

    def dynamic_update(self):
        pass
    
    def release_zoom(self, event):
        """the release mouse button callback in zoom to rect mode"""
        for zoom_id in self._ids_zoom:
            self.canvas.mpl_disconnect(zoom_id)
        self._ids_zoom = []

        if not self._xypress:
            return

        last_a = []

        for cur_xypress in self._xypress:
            x, y = event.x, event.y
            lastx, lasty, a, ind, lim, trans = cur_xypress
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
            Xmin, Xmax = a.get_xlim()
            Ymin, Ymax = a.get_ylim()

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
                x0, x1 = Xmin, Xmax
            else:
                if Xmin < Xmax:
                    if x < lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 < Xmin:
                        x0 = Xmin
                    if x1 > Xmax:
                        x1 = Xmax
                else:
                    if x > lastx:
                        x0, x1 = x, lastx
                    else:
                        x0, x1 = lastx, x
                    if x0 > Xmin:
                        x0 = Xmin
                    if x1 < Xmax:
                        x1 = Xmax

            if twiny:
                y0, y1 = Ymin, Ymax
            else:
                if Ymin < Ymax:
                    if y < lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 < Ymin:
                        y0 = Ymin
                    if y1 > Ymax:
                        y1 = Ymax
                else:
                    if y > lasty:
                        y0, y1 = y, lasty
                    else:
                        y0, y1 = lasty, y
                    if y0 > Ymin:
                        y0 = Ymin
                    if y1 < Ymax:
                        y1 = Ymax

            if self._button_pressed == 1:
                if self._zoom_mode == "x":
                    a.set_xlim((x0, x1))
                elif self._zoom_mode == "y":
                    a.set_ylim((y0, y1))
                else:
                    a.set_xlim((x0, x1))
                    a.set_ylim((y0, y1))
            elif self._button_pressed == 3:
                if a.get_xscale() == 'log':
                    alpha = np.log(Xmax / Xmin) / np.log(x1 / x0)
                    rx1 = pow(Xmin / x0, alpha) * Xmin
                    rx2 = pow(Xmax / x0, alpha) * Xmin
                else:
                    alpha = (Xmax - Xmin) / (x1 - x0)
                    rx1 = alpha * (Xmin - x0) + Xmin
                    rx2 = alpha * (Xmax - x0) + Xmin
                if a.get_yscale() == 'log':
                    alpha = np.log(Ymax / Ymin) / np.log(y1 / y0)
                    ry1 = pow(Ymin / y0, alpha) * Ymin
                    ry2 = pow(Ymax / y0, alpha) * Ymin
                else:
                    alpha = (Ymax - Ymin) / (y1 - y0)
                    ry1 = alpha * (Ymin - y0) + Ymin
                    ry2 = alpha * (Ymax - y0) + Ymin

                if self._zoom_mode == "x":
                    a.set_xlim((rx1, rx2))
                elif self._zoom_mode == "y":
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
        self.observer.update()
    
    def zoom(self, *args):
        """Activate zoom to rect mode"""
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
            self.observer.send()
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
    
class TreeListBox(object):
    '''
    Class that internally handles a TreeView widget which creates 
    a columned view of the information from the database
    '''
    def __init__(self, root, headers):
        '''
        Initialize any variables used in treelistbox, the list is the actual
        information being displayed, the headers are what appears in the columns
        and the tree is the TreeView object
        '''
        self.list = None
        self.headers = headers
        self.__root = root
        
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(self.__root, columns=headers, show="headings")
        # create scrollbars and pack window
        yScrollBar = Scrollbar(self.__root, orient=VERTICAL, command=self.tree.yview)
        xScrollBar = Scrollbar(self.__root, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=yScrollBar.set, xscrollcommand=xScrollBar.set)
        yScrollBar.pack(side=RIGHT, fill=Y, expand=NO)
        xScrollBar.pack(side=BOTTOM, fill=X, expand=NO)
        self.tree.pack(expand=YES, fill=BOTH)
    
    def update(self):
        '''
        Redisplay any information updated in self.list to the screen
        '''
        for i in self.tree.get_children():
            print "deleting", i
            self.tree.delete(i)
            
        for col in self.headers:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))
        for item in self.list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.headers[ix],width=None)<col_w:
                    self.tree.column(self.headers[ix], width=col_w)

def sortby(tree, col, descending):
    '''
    Sorts the treeview by the column clicked by the user
    '''
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data = change_numeric(data)
    # now sort the data in place
    convert = lambda text : int(text) if text.isdigit() else text
    alphanum_key = lambda key : [convert(c) for c in re.split('([0-9]+)', key[0])]
    data.sort(key=alphanum_key, reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
    int(not descending)))
    
def center(toplevel, size):
    '''
    Center the window
    '''
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def byteify(inp):
    if isinstance(inp, dict):
        return {byteify(key):byteify(value) for key,value in inp.iteritems()}
    elif isinstance(inp, list):
        return [byteify(element) for element in inp]
    elif isinstance(inp, unicode):
        return inp.encode('utf-8')
    else:
        return inp
    
class Observer(object):
    '''
    Class that implements the observer pattern
    '''
    
    def __init__(self, receiver):
        self.__receiver = receiver
        
    def update(self):
        self.__receiver.receive()
        
    def send(self):
        self.__receiver.send()