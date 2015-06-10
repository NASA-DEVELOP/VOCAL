======
Tools
======

.. py:module:: tools

.. py:class:: ToolTip(object)

   Allows for the easy creation of tool tips that are displayed below buttons. Requires a widget and overlays a simple tool tip once hovered over by the mouse. Created with py:meth:`createToolTip`

   .. py:method:: __init__(self, widget)
      :noindex:

      Initialize class variables, set widget

      :param Widget widget: Widget the tooltip will appear below

   .. py:method:: showtip(self, text):
      :noindex:

      Displays text as tooltip

      :param str text: Text to display

   .. py:method:: hidetip(self):
      :noindex:

      Hide tool tip once mouse leaves

.. py:class:: ToggleableButton(Button, object)

   A Class which wraps the Tkinter Button object and simulates the toggled button you commonly see in draw, magnify, etc. buttons. Keeps a static container of toggleable buttons to only allow one button at any time to be toggled.

   .. py:method:: __init__(self, root, master=None, cnf={}, **kw)
      :noindex: 

      Creates button and binds command to internal function :py:meth:`Toggle`  

      :param Widget root: The root of the program, or global cursor handle
      :param Widget master: Location the button will be packed to
      :param cnf: Button forwarded args
      :param kw: Button forwarded args

   .. py:method:: latch(self, key="", command=None, cursor="", destructor=None)
      :noindex:

      Binds a *key* to a *command* upon the button being toggled, stored inside a bindmap. **Note** latch is additive, it can be called multiple times to bind multiple keys

      :param str key: A valid Tkinter command key
      :param func command: The function to be binded to the key
      :param str cursor: a valid Tkinter cursor to be set upon toggle
      :param func destructor: A function called upon un-toggling the button
      
   .. py:method:: unToggle(self)
      :noindex:

      Manually untoggle the button

   .. py:method:: Toggle(self)
      :noindex:

      The method bound to the button, *Toggle* will internally bind the inputed keys when toggled, and unbind them accordingly. Also keeps track of all toggled button via a static container and ensures only one button can be toggled at any time

.. py:class:: ToolbarToggleableButton(ToggleableButton)
   
   A wrapper of a wrapper of a button, this class is a specialized wrapper of the button for the matplotlib backend toolbar. This class inherits all functionality of the previous ToggleableButton class, but now invokes a function **before** and **after** the toggling, and does no binding of keys. This is useful for custom implementing all of the buttons provided by the Navigationtoolbar2TkAgg, since we re-implementing these with our own GUI

   .. py:method:: __init__(self, root, master=None, func=None, cnf={}, **kw)
      :noindex:

      Initializes base class by forwarding all required arguments, additionaly sets the internal function call to *func* which is called on toggle and untoggle

      :param Widget root: The root of the program, or global cursor handle
      :param Widget master: Location of where to draw the button
      :param Function func: Function to be invoked on toggle and untoggle of button
      :param cnf: Button forwarded args
      :param kw: Button forwarded args

   .. py:method:: Toggle(self)
      :noindex:

      Calls the super class :py:meth:`Toggle`, but not before invoking *func* if exists

.. py:class:: NavigationToolbar2CALIPSO(NavigationToolbar2)

   Custom toolbar implementation deriving from the matplotlib.backend *NavigationToolbar2*, The TkAgg port is not used because we specifically implement our own GUI and therefore to not want to draw the TkAgg's navigation bar. So we declare this class and leave it mostly bare, thus nothing will be rendered to the screen but we still have access to the button functions and can bind them to our own GUI

   .. py:method:: __init__(self, canvas)
      :noindex:

      Calls the base class *__init__* constructor

   .. py:method:: _init_toolbar(self)
      :noindex:

      Passed

   .. py:method:: draw_rubberband(self, event, x0, y0, x1, y1)
      :noindex:

      the function that dynamically draws the rectangle when the zoom feature is active , follows the mouse location when the button 1 is held and deletes upon release

      :param event: event passed containing the mouse coordinates
      :param x0: Location of rectangle X0
      :param y0: Location of rectangle Y0
      :param x1: Location of rectangle X1
      :param y1: Location of rectangle Y1

   .. py:method:: release(self, event)
      :noindex:

      Destructor call for the navigation button, releases resources

   .. py:method:: set_cursor(self, event)
      :noindex:

      Passed

   .. py:method:: save_figure(self, *args)
      :noindex:

      Passed

   .. py:method:: configure_subplots(self)
      :noindex:

      Passed

   .. py:method:: set_active(self)
      :noindex:

      Passed

   .. py:method: update(self)
      :noindex:

      Passed

   .. py:method: dynamic_update(self)
      :noindex:

      Passed 
