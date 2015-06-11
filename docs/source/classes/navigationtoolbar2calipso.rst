==========================
NavigationToolbar2Calipso
==========================

Custom toolbar implementation deriving from the matplotlib.backend *NavigationToolbar2*, The TkAgg port is not used because we specifically implement our own GUI and therefore to not want to draw the TkAgg's navigation bar. So we declare this class and leave it mostly bare, thus nothing will be rendered to the screen but we still have access to the button functions and can bind them to our own GUI

.. py:module:: tools

.. py:class:: NavigationToolbar2CALIPSO(NavigationToolbar2)   

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
