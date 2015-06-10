=================================
ToolbarToggleableButton
=================================

.. py:module:: tools

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
