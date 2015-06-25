==================
ToggleableButton
==================

A Class which wraps the Tkinter Button object and simulates the toggled button you commonly see in draw, magnify, etc. buttons. Keeps a static container of toggleable buttons to only allow one button at any time to be toggled.

.. inheritance-diagram:: calipso.tools.toggleablebutton

.. py:module:: toggleablebutton

.. autoclass:: calipso.tools.toggleablebutton.ToggleableButton
   :members:

A simplified version of ``ToggleableButton``, also inherits from ``Button``. This class manages an internal toggled state which is globally kept track of for all toggle buttons. The button is always bound to the :py:meth:`Toggle` function, which internally invokes the passed ``func`` argument

.. autoclass:: calipso.tools.toggleablebutton.ToolbarToggleableButton
   :members:
