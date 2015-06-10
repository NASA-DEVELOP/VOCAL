=============
PolygonDrawer
=============

..
   POPULATING METHODS

   The general structure of populating a method is as follows:

   py:method:: <name>           # let sphinx know the following is a method
   :noindex:                    # do not populate in index tab because
                                # this is a class method

   <description>                # description of what method does

   :param <type> <name>:        # parameter passed, do not do this for self
   :param <name>:               # parameter with no type

   EXAMPLE

   py:class:: foo
   
      py:method:: func(self, arg1, arg2)
      :noindex:

      does stuff and more stuff

      :param int arg1: argument 1
      :param arg2: argument 2

   Markup docs: http://sphinx-doc.org/rest.html#rst-primer

.. py:module:: PolygonDrawer

.. py:class:: PolygonDrawer(Widget)

   .. py:method:: __init__(self, canvas)
      :noindex:
      
      Creates a drawer that handles all polygon manipulations on the canvas

   .. py:method:: OnTokenButtonPress(self, event)
      :noindex:

   .. py:method:: OnTokenButtonRelease(self, event)
      :noindex:

   .. py:method:: OnTokenMotion(self, event)
      :noindex:

   .. py:method:: anchorRectangle(self, event)
      :noindex:

   .. py:method:: plotPoint(self, event)
      :noindex:

   .. py:method:: rubberBand(self, event)
      :noindex:

   .. py:method:: fillRectangle(self, event)
      :noindex:

   .. py:method:: setHDF(self, HDFFilename)
      :noindex:

   .. py:method:: getVertices(self)
      :noindex:

   .. py:method:: getHDF(self)
      :noindex:

   .. py:method:: __canDrawPolygon(self)
      :noindex:

   .. py:method:: drawPolygon(self)
      :noindex:

   .. py:method:: toggleDrag(self, event)
      :noindex:

   .. py:method:: generateTag(self)
      :noindex:

   .. py:method:: reset(self)
      :noindex:

   .. py:method:: delete(self, event)
      :noindex:

   .. py:method:: __clear(self, event)
      :noindex:

   .. py:method:: outline(self)
      :noindex:

   .. py:method:: paint(self, event)
      :noindex:

   .. py:method:: hide(self)
      :noindex:
