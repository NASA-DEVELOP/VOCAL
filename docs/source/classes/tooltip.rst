==============
ToolTip
==============

Allows for the easy creation of tool tips that are displayed below buttons. Requires a widget and overlays a simple tool tip once hovered over by the mouse. Created with py:meth:`createToolTip`

.. py:module:: tools

.. py:class:: ToolTip(object)

   .. py:data:: self.widget
        
      the widget to draw to in :py:meth:`showTip`

   .. py:data:: self.tipWindow

      top level window created to show the tooltip

   .. py:data:: self.x
   .. py:data:: self.y
      
      x and y coordinates of tooltip window

   .. py:method:: __init__(self, widget)
      :noindex:
        
      Initialize class variables, set widget

      :param Widget widget: Widget the tooltip will appear below

   .. py:method:: showTip(self, text):
      :noindex:

      Displays text as tooltip

      :param str text: Text to display

   .. py:method:: hideTip(self):
      :noindex:

      Hide tool tip once mouse leaves

