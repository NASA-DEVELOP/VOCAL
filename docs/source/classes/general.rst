========
General
========

.. py:class:: Calipso(r)

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

      .. py:attribute:: BASE_PLOT - draws to an empty canvas

      .. py:attribute:: BACKSCATTERED - draws from *plot_uniform_alt_lidat_dev* 

      .. py:attribute:: DEPOLARIZED - draws from **noimpl** ..implement this

      .. py:attribute:: VFM - draws from **noimpl** ..implement this

      Draws to the canvas according to the *plotType* specified in the arguments. Accepts one of the attributes above
    
      :param int plotType: accepts ``BASE_PLOT, BACKSCATTERED, DEPOLARIZED, VFM``

   .. py:method:: reset(self)
      :noindex:

      Reloads the initial image displayed on the canvas in accordance to *plotType*. Deletes all objects currently drawn to the screen as well.

   .. py:method:: toolbarCleanup(self, str_)
      :noindex:


