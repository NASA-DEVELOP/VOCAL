######################################
#    toggleablebutton.py
#    @author: Grant Mercer
#    6/24/2015
######################################
from Tkinter import Button
import Tkinter as tk
import ttk
from sys import platform as _platform

# global button container for managing state
toggleContainer = []

class ToggleableButton(object):
    """
    Button wrapper which simluates the toggle button as you see in the draw, magnify, etc.
    buttons. Internally keeps a bind map whic on toggle binds the keys in the map, and
    unbinds them on untoggle or forced untoggle.

    :param root: Root of the program, which handles the cursor
    :param canvas: The matplotlib Tkinter canvas to connect binds to
    :param master: The locaiton to draw the button on
    """
    def __init__(self, root, master, text='', width=30, height=30, image=''):
        self.__bindMap = []         # bind map to be bound once toggled
        self.unToggled = True       # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__destructor = None    # destructor var called when untoggled
        self.__cid_stack = []
        self.__master = master
        self.__button = ttk.Button(root, text=text, command=lambda: self.toggle(), style='SunkableButton.TButton')
        self.__style = ttk.Style()

        self.__button.configure(width=width, image=image)
        toggleContainer.append(self)    # push button to static container

    def latch(self, target=None, key='', command=None, destructor=None, cursor=''):
        """
        Allows the binding of keys to certain functions. These bindings will become
        active once the button is in a toggle state. latch can be called **multiple**
        times and keeps an internal bindmap.

        :param str key: A valid Tkinter key string
        :param command: Function to be bound to key
        :param destructor: A function called when untoggled
        """
        if key != '' and command is not None and target is not None:
            self.__bindMap.append((target, key, command))
        if destructor is not None:
            self.__destructor = destructor

    def untoggle(self):
        """
        Forcefully untoggles the button. Used when ensuring
        only one button in the global container is active at any time
        """
        self.unToggled = True
        for pair in self.__bindMap:
            if self.__cid_stack:
                pair[0].mpl_disconnect(self.__cid_stack.pop())
        if self.__destructor:
            self.__destructor()

    def toggle(self):
        """
        The method bound to the button. *Toggle* wil internally bind the inputed keys when toggled,
        and unbind them accordingly. Also keeps track of all toggled button via a static container
        and ensures only one button can be toggled at any time
        """
        # first flit the toggle switch
        self.unToggled = not self.unToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.unToggled is False and x is not self]:
            s.untoggle()

        # else if the next stat is false
        if self.unToggled:
            self.__button.state(['!pressed'])
            self.__style.configure('SunkableButton.TButton', relief=tk.RAISED)
            for pair in self.__bindMap:             # unbind using the bindmap
                if self.__cid_stack:
                    pair[0].mpl_disconnect(self.__cid_stack.pop())
            if self.__destructor:
                self.__destructor()                 # call the pseudo 'destructor'
        # if the next state is false
        else:
            self.__button.state(['pressed'])
            self.__style.configure('SunkableButton.TButton', relief=tk.SUNKEN)
            for pair in self.__bindMap:             # bind using the bindmap
                self.__cid_stack.append(pair[0].mpl_connect(pair[1, pair[2]]))

    def grid(self, row, column, padx=2, pady=5):
        self.__button.grid(row=row, column=column)

class ToolbarToggleableButton(Button):
    """
    GUI button used to implement the backend matplotlib plot functions. Instead
    of placing more overhead in the ToggleableButton another class is created
    since the number of matplotlib functions will remain constant, while we
    may continue creating new tools that use ToggleableButton

    :param root: Root of the program, or the location of the cursor to be changed
    :param master: Location of the button to be drawn to
    :param func: Function to be called each time the button is 'toggled'
    :param cnf: Button forwarded args
    :param \*\*kw: Button forwarded args
    """

    # noinspection PyDefaultArgument
    def __init__(self, root, master=None, func=None, cnf={}, **kw):
        if not cnf:
            cnf = {}
        self.isToggled = False      # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__cursor = ''          # cursor private var
        self.__master = master
        self.__func = func
        
        Button.__init__(self, master, cnf, **kw)    # call button constructor
        self.configure(command=self.toggle)         # button command is always toggle
        toggleContainer.append(self)         # push button to static container
        
    def latch(self, cursor=''):
        """
        Set the internal cursor variable to the cursor to be used when the button
        is in a toggled state

        :param str cursor: A valid Tkinter cursor string
        """
        # only set these variables if the user entered one
        if cursor != '':
            self.__cursor = cursor

    def untoggle(self):
        """
        Forcefully untoggles the button and invokes ``func``. Used when ensuring
        only one button in the global container is active at any time
        """
        self.isToggled = False
        self.config(relief='raised')
        if self.__func:
            self.__func()
        
    # Call the super classes Toggle, and execute our function as well
    def toggle(self):
        """
        Calls the passed function ``func`` and manages a toggle state below. Ensures only
        one toggled button is active at any time and the button is correctly raised/sunk
        """
        self.isToggled = not self.isToggled
        # if any buttons are currently active, untoggle them
        for s in [x for x in toggleContainer if x.isToggled is True and x is not self]:
            s.untoggle()
        
        # first flip the toggle switch
        if self.__func:
            self.__func()
        # else if next state it false
        if self.isToggled is False:
            self.config(relief='raised')                # raise the button, e.g. deactivated
        # else if next state is true
        else:
            self.__root.config(cursor=self.__cursor)
            self.config(relief='sunken')                # sink the button, e.g. activate
