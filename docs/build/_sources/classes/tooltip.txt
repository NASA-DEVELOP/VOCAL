==============
ToolTip
==============

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

