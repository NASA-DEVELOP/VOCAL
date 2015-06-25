==========================
NavigationToolbar2Calipso
==========================

Custom toolbar implementation deriving from the matplotlib.backend *NavigationToolbar2*, The TkAgg port is not used because we specifically implement our own GUI and therefore to not want to draw the TkAgg's navigation bar. So we declare this class and leave it mostly bare, thus nothing will be rendered to the screen but we still have access to the button functions and can bind them to our own GUI

.. inheritance-diagram:: calipso.tools.navigationtoolbar.NavigationToolbar2CALIPSO

.. py:module:: navigationtoolbar

.. autoclass:: calipso.tools.navigationtoolbar.NavigationToolbar2CALIPSO
   :members:
