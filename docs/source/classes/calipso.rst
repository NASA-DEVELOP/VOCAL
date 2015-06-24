=============
Calipso
=============

The main class of the application. Calipso manages all Tkinter and widget related entities, and ensures all parts of the GUI are initialized and created before the start of the program. The order of functions calls in the beginning of the program is as follows::

    __init__
    setupWindow
    setupMenu
    setupMainScreen
        * calls createTopScreenGUI
        * calls createChildWindowGUI
        * calls selPlot(BASE_PLOT)

#.. inheritance-diagram:: gui.Calipso

.. py:class:: Calipso(r)

   .. py:data:: self.__root

      the root widget of the program, passed into __init__ and will always be ``Tk()``

   .. py:data:: self.__file

      current loaded file being displayed in the program, file extension *hdf*

   .. py:data:: self.__menuBar

      menu bar appearing at the top of the screen

   .. py:data:: self.__menuFile

      sub menu

   .. py:data:: self.__menuHelp

      sub menu

   .. py:method:: __init__(self, r)
      :noindex:
    
      Creates and initializes all windows in the program to a blank state. Creates panes and frames to section off each window and connects a draw canvas to the center screen of the main window. 

      :param Widget r: the root of the program, often just ``root = Tk()``

   .. py:method:: centerWindow(self)
      :noindex:

      Grabs the size of the screen as given by the root and determines the center location of the screen, then places the main window and child window accordingly

   .. py:method:: setupWindow(self)
      :noindex:

      Sets the title of root and invokes py:meth:`centerWindow`

   .. py:method:: setupMenu(self)
      :noindex:

      Creates the drop down menu bar

   .. py:method:: selPlot(self, plotType)
      :noindex:

      .. py:attribute:: BASE_PLOT

      .. py:attribute:: BACKSCATTERED 

      .. py:attribute:: DEPOLARIZED

      .. py:attribute:: VFM 

      Draws to the canvas according to the *plotType* specified in the arguments. Accepts one of the attributes above
    
      :param int plotType: accepts ``BASE_PLOT, BACKSCATTERED, DEPOLARIZED, VFM``

   .. py:method:: reset(self)
      :noindex:

      Reloads the initial image displayed on the canvas in accordance to *plotType*. Deletes all objects currently drawn to the screen as well.

   .. py:method:: toolbarCleanup(self, str_)
      :noindex:

      Force toggles the toolbar functions provided by matplot lib and sets their active state to **off**

      :param str str\_: The state to set _active to, e.g. ``pan()`` is 'PAN', ``zoom()`` is 'ZOOM'

   .. py:method:: createTopScreenGUI(self)
      :noindex:

      Initializes and creates the file dialog and browse button that appear at the top of the screen

   .. py:method:: createChildWindowGUI(self)
      :noindex:

      Initializes and creates all buttons and tools on the child window

   .. py:method:: importFile(self)
      :noindex:

      Opens load dialong and prompts user for input of file, sets internal file state to passed file

   .. py:method:: exportImage(self)
      :noindex:

      ``Pass``

   .. py:method:: saveImage(self)
      :noindex:

      ``Pass``

   .. py:method:: saveAs(self)
      :noindex:

      Saves the HDF similar to how it was initially loaded, opens dialog and prompts save location

   .. py:method:: about(self)
      :noindex:

      Opens message box displaying author information

   .. py:method:: tutorial(self)
      :noindex:

      Tutorial function *note:* likely to be deprecated in the future

   .. py:method:: setupMainScreen(self)
      :noindex:

      Wrapper function which calls py:meth:`createTopScreenGUI` , py:meth:`setupMenu` , py:meth:`setupMainScreen`

