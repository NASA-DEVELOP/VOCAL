=====================
Program Overview
=====================

The CALIPSO: Global Health & Air Quality project aims at creating a tool with the ability to classify aerosols within CALIPSO Data to help improve future research and decision making. The summer 2015 team consisting of Grant Mercer and Nathan Qian will build on the existing graphical user interface built by the previous team.

----------------------------------------
Abstract
----------------------------------------

The CALISPO satellite (Cloud-Aerosol Lidar and Infrafred Pathfinder Satellite Observation) is a NASA
earth observation that analyzes aerosol particles suspended in the Earth's atmosphere. Researchers use 
CALIPSO data to track the aerosol's global distribution, dispersion and source. However, researchers 
have a hard time tracking specific airborne objects as the current visualization tool that reads CALIPSO 
data lacks the feature to highlight unique aerosols and has not method of sharing aerosol data. This tool 
is written in a propriety language, which prevents users from making the necessary adjustments. To 
rectify these issues, a NASA DEVELOP team created a new visualization tool written in Python that is 
open source and displays CALIPSO data. For this summer term, another DEVELOP team implemented 
new features that will help scientists track aerosols and share this data with each other. These additional 
features will allow scientists to more easily identify the source of the aerosol and its impact on the Earth.

.. rubric:: Community Concerns

* The current CALISPO visualization tool is not easily configurable or adaptable
* The CALIPSO science team lacks a method for storing and sharing specific features of CALISPO imagery

.. rubric:: Current Management Practices & Policies 

* The tool currently used to visualize CALIPSO data is written in IDL, a proprietary language which lacks many features and hinders open source updates.

----------------------------------------
Structure
----------------------------------------

The program has the following file layout::

   +---.settings
   +---dat
   +---db
   |   \---manage_db
   +---docs
   |   +---build
   |   |   +---.doctrees
   |   |   |   +---classes
   |   |   |   \---functions
   |   |   +---classes
   |   |   +---functions
   |   |   +---_images
   |   |   +---_modules
   |   |   +---_sources
   |   |   |   +---classes
   |   |   |   \---functions
   |   |   \---_static
   |   \---source
   |       +---classes
   |       +---functions
   |       \---_static
   +---gui
   |   +---dat
   |   +---ico
   |   +---objs
   |   \---plot
   \---plot_vfm

----------------------------------------
Features
----------------------------------------

.. class:: left: blank program, right: shapes form around selected areas of the plot

   .. image:: _static/program.png
      :scale: 30%

   .. image:: _static/programShapesActive.png
      :scale: 30%


CALIPSO is still in a very early development phase

The CALIPSO Visualization software currently contains a number of great features:

* Load standard L1 Calipso data and display a backscattered plot     
* Manipulate the image with ``zoom``, ``move``, ``reload`` and many more
* Draw object which are overlayed upon the plot , free draw or rect mode

Data from the ``HDF`` file is loaded and parsed in order to display the plot inside of the application. Object can be drawn on top and manipulated to select key parts of the map, these object will later be able to be saved

*(above: a recent snapshot of the CALIPSO Visualization tool)*

Once a plot is displayed, the user can select from a range of features in the *toolbar*:

* ``Reset`` : reload the original state of the plot
* ``Plot Type`` : select type of plot
* ``Drag`` : drag plot
* ``Zoom`` : zoom to rectangle
* ``Undo`` : undo button
* ``Redo`` : redo button
* ``Draw Rect`` : draw a rectangle on the plot
* ``Drag Rect`` : drag shapes around the plot
* ``Free Draw`` : connect vertices on the map to form a shape
* ``Erase`` : erase a shape
* ``Focus`` : fill or no fill setting for shapes
* ``Paint`` : specify the color of a shape
* ``Hide``  : hide shapes
* ``Save``  : save visible objects to a JSON file
* ``Load``  : load a JSON file containing objects
* ``View``  : view notes and attributes of polygon
* ``Edit``  : add notes and attributes for polygons

Additional features are still to come!

----------------------------------------
Additional Information
----------------------------------------

* **Applied Sciences Natinoal Applications Addressed:**
     National App1, National App2, etc

* **Study Area:**
     Global

* **Study Period:**
     May 2000 - Nov 2010

* **Earth Observations & Parameters:**
     CALIPSO, CALIOP - Vertial Profile of Aerosolsl

