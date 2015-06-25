=============
Calipso
=============

The main class of the application. Calipso manages all Tkinter and widget related entities, and ensures all parts of the GUI are initialized and created before the start of the program.

.. code-block:: python

   if __name__ == "__main__":
       rt = Tk()
       program = Calipso(rt)       # Create main GUI window

       program.setupWindow()       # create window in center screen
       program.setupMenu()         # create top menu
       program.setupMainScreen()   # create top buttons, initialize child and display base_plt
        
       rt.mainloop()               # program main loop
       os._exit(1)


The order of functions calls in the beginning of the program is as follows::
   
   __init__
   setupWindow
   setupMenu
   setupMainScreen
       |-> calls createTopScreenGUI
       |-> calls createChildWindowGUI
       |-> calls selPlot(BASE_PLOT)

.. inheritance-diagram:: calipso.Calipso.Calipso

.. automodule:: calipso.Calipso
   :members:
