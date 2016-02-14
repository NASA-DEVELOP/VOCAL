=====================
Program Overview
=====================

The CALIPSO: Global Health & Air Quality project at NASA DEVELOP aims at creating a tool with the ability to classify
aerosols within CALIPSO Data to help improve future research and decision making. The tool is open source and built
around community involvement.

.. rubric:: Key reason for VOCAL:

* The tool currently used to visualize CALIPSO data is written in IDL, a proprietary language which lacks many
  features and hinders open source updates. It also has very little documentation as to the development process of the
  tool, making it very difficult to build upon.

----------------------------------------
Features
----------------------------------------

.. class:: left: blank program, right: shapes form around selected areas of the plot

   .. image:: _static/program.png
      :scale: 22%

   .. image:: _static/programShapesActive.png
      :scale: 20%


.. note::
   VOCAL is currently in it's early *beta* phase, and requires additional work
   till it can be released to the community.

The Visualization tool currently contains a number of great features:

* Load standard Calipso data and display a backscattered and depolarized plot
* Manipulate the image with ``zoom``, ``move``, ``reload`` and many more
* Draw object which are overlayed upon the plot , free draw or rect mode

Data from the ``HDF`` file is loaded and parsed in order to display the plot inside of the application. Objects can be
drawn on top and manipulated to select key parts of the map, these object will later be able to be saved

Once a plot is displayed, the user can select from a range of features in the *toolbar*:

* ``Reset`` : reload the original state of the plot
* ``Backscattered`` : render backscattered
* ``Depolarized``: render depolarized
* ``Render``: visualize the data
* ``Step``: jump to a custom time range in the HDF
* ``Drag`` : drag plot
* ``Zoom`` : zoom to rectangle
* ``Undo`` : undo button
* ``Redo`` : redo button
* ``Home`` : return to the home view originally rendered
* ``Properties``: view the properties of the shape
* ``Attributes``: assign attributes and notes to the shape
* ``Extract``: extract the shape to a separate subplot
* ``Draw Rect`` : draw a rectangle on the plot
* ``Free Draw`` : connect vertices on the map to form a shape
* ``Erase`` : erase a shape
* ``Paint`` : specify the color of a shape
* ``Focus`` : fill or no fill setting for shapes
* ``Hide``  : hide shapes
* ``Save``  : save visible objects to a JSON file
* ``Load``  : load a JSON file containing objects

Additional features are still to come!

----------------------------------------
Additional Information
----------------------------------------

* **Study Area:**
     Global

* **Earth Observations & Parameters:**
     CALIPSO, CALIOP - Vertial Profile of Aerosolsl

