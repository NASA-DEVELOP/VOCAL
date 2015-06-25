######################################
#    toggleablebutton.py
#    @author: Grant Mercer
#    6/24/2015
######################################
from Tkinter import Button

#global button container for managing state
toggleContainer = []  

class ToggleableButton(Button):
    '''
    Button wrapper which simulates the toggled button as you see in the draw, magnify, etc. 
    buttons. Interally keeps a bind map which on toggle binds the keys in the map, and 
    unbinds them on untoggle or forced untoggle.
    
    :param root: Root of the program, which handles the cursor
    :param master: The location to draw the button to
    :param cnf: Button forwarded args
    :param \*\*kw: Button forwarded args
    '''

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
        

    def latch(self, key="", command=None, cursor="", destructor=None):
        '''
        Allows the binding of keys to certain functions. These bindings will become
        active once the button is in a toggled state. latch can be called **multiple**
        times and keeps an internal bindmap. 
        
        :param str key: A valid Tkinter key string
        :param command: Function to be bound to key
        :param str cursor: A valid Tkinter cursor string
        :param destructor: A function called when untoggled
        '''
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor
        if key != "" and command != None : self.__bindMap.append((self.__root, key, command))
        if destructor != None : self.__destructor = destructor

    def unToggle(self):
        '''
        Forcefully untoggles the button. Used when ensuring
        only one button in the global container is active at any time
        '''
        self.isToggled = False
        self.config(relief='raised')
        for pair in self.__bindMap:
            pair[0].unbind(pair[1])
        if self.__destructor : self.__destructor()


    def toggle(self):
        '''
        The method bound to the button, *Toggle* will internally bind the inputed keys when toggled,
         and unbind them accordingly. Also keeps track of all toggled button via a static container and 
         ensures only one button can be toggled at any time
        '''
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
    GUI button used to implement the backend matplotlib plot functions. Instead
    of placing more overhead in the ToggleableButton another class is created 
    since the number of matplotlib functions will remain constant, while we
    may continue creating new tools that use ToggleableButton
    
    :param root: Root of the program, or the location of the cursor to be changed
    :param master: Location of the button to be drawn to
    :param func: Function to be called each time the button is 'toggled'
    :param cnf: Button forwarded args
    :param \*\*kw: Button forwarded args
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
        '''
        Set the internal cursor variable to the cursor to be used when the button 
        is in a toggled state
        
        :param str cursor: A valid Tkinter cursor string
        '''
        # only set these variables if the user entered one
        if cursor != "" : self.__cursor = cursor

    def unToggle(self):
        '''
        Forcefully untoggles the button and invokes ``func``. Used when ensuring
        only one button in the global container is active at any time
        '''
        self.isToggled = False
        self.config(relief='raised')
        if self.__func : self.__func()
        
    # Call the super classes Toggle, and execute our function as well
    def toggle(self):
        '''
        Calls the passed function ``func`` and manages a toggle state below. Ensures only
        one toggled button is active at any time and the button is correctly raised/sunk
        '''
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
            
