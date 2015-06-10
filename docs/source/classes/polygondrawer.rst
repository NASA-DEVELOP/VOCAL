=============
PolygonDrawer
=============

The class in charge of managing any drawing on the canvas. 

.. py:module:: PolygonDrawer

.. py:class:: PolygonDrawer(Widget)

   .. py:method:: __init__(self, canvas)
      :noindex:
      
      Creates a drawer that handles all polygon manipulations on the canvas
      
      :param tkcanvas canvas: A tkinter canvas that will hold all the polygons

   .. py:method:: OnTokenButtonPress(self, event)
      :noindex:
      
      An observer that determines which polygon has been selected for dragging
      
      :param event event: An event object generated at the selected polygon

   .. py:method:: OnTokenButtonRelease(self, event)
      :noindex:
      
      An observer that resets the internal attributes for polygon dragging
      
      :param event event: An event object generated at the selected polygon

   .. py:method:: OnTokenMotion(self, event)
      :noindex:
      
      An observer that redraws the polygon at the new coordinates
      
      :param event event: An event object generated at the polygon's new position

   .. py:method:: anchorRectangle(self, event)
      :noindex:
      
      Establishes a corner of a rectangle as an anchor for when the user drags the cursor to create the rectangle
      
      :param event event: An event object at the anchor point

   .. py:method:: plotPoint(self, event)
      :noindex:
      
      Plots the sides of the vertices as line segments. When a segment crosses over another, a polygon is generated from the resulting figure
      
      :param event event: An event object at the end point of each line segment

   .. py:method:: rubberBand(self, event)
      :noindex:
      
      Draws temporary rectangles to help the user visualize the rectangle he/she is drawing
      
      :param event event: An event object generated as the user sizes the rectangle

   .. py:method:: fillRectangle(self, event)
      :noindex:
      
      Draws the rectangle
      
      :param event event: An event object at the opposite corner of the anchor point that bounds the rectangle

   .. py:method:: setHDF(self, HDFFilename)
      :noindex:
      
      Saves the HDF file that the polygon is associated with
      
      param: str HDFFilename: the name of the HDF file

   .. py:method:: getVertices(self)
      :noindex:
      
      Returns the plotted points of the undrawn polygon

   .. py:method:: getHDF(self)
      :noindex:
      
      Returns the HDF file associated with the polygons

   .. py:method:: __canDrawPolygon(self)
      :noindex:

   .. py:method:: drawPolygon(self)
      :noindex:
      
      Determines if the last drawn line segment produces a polygon with any of the previously drawn lines

   .. py:method:: toggleDrag(self, event)
      :noindex:
      
      Enables or disables polygon dragging
      
      :param event event: An event object that toggles dragging

   .. py:method:: generateTag(self)
      :noindex:
      
      Produces a unique tag for each polygon drawn

   .. py:method:: reset(self)
      :noindex:
      
      Deletes all polygons and lines drawn and resets internal attributes

   .. py:method:: delete(self, event)
      :noindex:
      
      Deletes the specified polygon
      
      :param event event: An event object generated at a specified polygon

   .. py:method:: __clear(self)
      :noindex:
      
      Resets internal attributes to allow the user to draw a separate polygon

   .. py:method:: outline(self)
      :noindex:
      
      Redraws the polygons from shaded to outline and vice-versa

   .. py:method:: paint(self, event)
      :noindex:
      
      Redraws a polygon with the specified color. Creates a new prompt for the user to select the color
      
      :param event event: An event object that selects the polygon to be recolored

   .. py:method:: hide(self)
      :noindex:
      
      Switches between hiding and displaying all the polygons drawn on the canvas
