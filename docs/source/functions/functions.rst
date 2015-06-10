============================
Functions
============================

Documentation on non-class-bound Functions

.. py:module:: tools

.. py:method:: createToolTip(widget, text)

   The function used to create a tool tip, internally creates a :py:class:'ToolTip' object and binds the corresponding keys.

   :param Widget widget: the Widget the tooltip should be shown for
   :param str text: The message to show in the tooltip

.. py:module:: Polygon

.. py:function:: perpendicular(a)

   Returns a numpy array that's orthongonal to the param

   :param a: Numpy array 

.. py:function:: getIntersection(a1, a2, b1, b2)

   Retrieves the point of interesection of two lines given two points on each line.

   :param a1, a2: First point
   :param b1, b2: Second point

.. py:function:: isInteresecting(a1, a2, b1, b2)

   Determines if two line segments are intersecting by checking if the point of intersection exists on the line segments

   :param a1, a2: The endpoints of the first line segment
   :param b1, b2: The endpoints of the second line segment

.. py:function:: tupleToNpArray(pair)

   Returns an array of the tuple passed

   :param pair: A tuple

.. py:function:: npArrayToTuple(array)

   Returns a tuple of the array passed

   :param array: The array passed

