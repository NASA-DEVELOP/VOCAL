import Tkinter as tk
import ttk

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
    def __init__(self, root, master, text=''):
        self.__bindMap = []         # bind map to be bound once toggled
        self.unToggled = True       # internal var to keep track of toggling
        self.__root = root          # root variable for setting the cursor
        self.__destructor = None    # destructor var called when untoggled
        self.__cid_stack = []
        self.__master = master
        self.__button = ttk.Button(root, text=text, command=lambda: self.toggle(), style='SunkableButton.TButton')
        self.__style = ttk.Style()

        toggleContainer.append(self)    # push button to static container

    def latch(self, target=None, key='', command=None, destructor=None):
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

    def grid(self, row, column):
        self.__button.grid(row=row, column=column)