=================================
ToolbarToggleableButton
=================================

A simplified version of ``ToggleableButton``, also inherits from ``Button``. This class manages an internal toggled state which is globally kept track of for all toggle buttons. The button is always bound to the :py:meth:`Toggle` function, which internally invokes the passed ``func`` argument

.. py:module:: tools

.. py:class:: ToolbarToggleableButton(Button)

   .. py:method:: __init__(self, root, master=None, func=None, cnf={}, **kw)
      :noindex:

      Sets private variables and initializes Button constructor, also appends *self* to the global toggle container ``toggleContainer``.

      :param Widget root: The root of the program, or global cursor handle
      :param Widget master: Location of where to draw the button
      :param Function func: Function to be invoked on toggle and untoggle of button
      :param cnf: Button forwarded args
      :param kw: Button forwarded args

   .. py:method:: latch(self, cursor="")
      :noindex:

      Stripped method that only sets the cursor. To maintain call conventions this method keeps the name latch, but since the class does not have a bind map it's only use is for the cursor.

      :param str cursor: Accepts a valid Tkinter cursor string

   .. py:method:: unToggle(self)
      :noindex:

      Forcefully untoggles the button and invokes ``func``. Used when ensuring only one button in the global container is active at any time.

   .. py:method:: Toggle(self)
      :noindex:

      Calls the passed function ``func``, and manages a toggle state below. Ensures only one toggled button is active at any time and the button is correctly raised/sunk
