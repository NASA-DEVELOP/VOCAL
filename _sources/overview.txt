=====================
Program Overview
=====================

The CALIPSO: Global Health & Air Quality project aims at creating a tool with the ability to classify aerosols within CALIPSO Data to help improve future research and decision making. The summer 2015 team consisting of Grant Mercer and Nathan Qian will build on the existing graphical user interface built by the previous team.

----------------------------------------
Background
----------------------------------------

The CALISPO satellite (Cloud-Aerosol Lidar and Infrared Pathfinder Satellite Observation) is a NASA
earth observation that analyzes aerosol particles suspended in the Earth's atmosphere. Researchers use 
CALIPSO data to track the aerosol's global distribution, dispersion and source. However, researchers 
have a hard time tracking specific airborne objects as the current visualization tool that reads CALIPSO 
data lacks the feature to highlight unique aerosols and has not method of sharing aerosol data. This tool 
is written in an obscure, and propriety, language which prevents users from making the necessary adjustments. To
rectify these issues, we've developed VOCAL. VOCAL is an open source tool written in python 2.7 that supports
all previous features of past tool and more! We've developed with a heavy influence on open source collaboration,
we hope VOCAL will continue to improve long past the initial contracted work.

VOCAL allows users to visualize Hierarchical Data Format (HDF) files from CALIPSO and draw shapes upon the plot.
These shapes can be assigned attributes and notes than can help characterize aerosols in the atmosphere as well as
track specific objects moving. Data can be extracted from these shapes and shown on either a subplot or as a raw
exported data file, allowing users additional tools for tracking the trajectory of aerosols. The biggest benefit
VOCAL brings is a standardized information sharing medium. Users can export their shapes into a JSON file and personally
pass data between each other, or share a centralized database which can store and be queried for specific shapes and
specific files.

.. rubric:: Current Concerns

* The current CALISPO visualization tool is not easily configurable or adaptable as it is developed in IDL.
* The CALIPSO science team lacks a method for storing and sharing specific features of CALISPO imagery

.. rubric:: Current Management Practices & Policies 

* The tool currently used to visualize CALIPSO data is written in IDL, a proprietary language which lacks many
  features and hinders open source updates. It also has very little documentation as to the development process of the
  tool, making it very difficult to build upon.

----------------------------------------
Structure
----------------------------------------

The program has the following file layout::

   +---calipso
   |   +---.idea
   |   |   \---dictionaries
   |   +---dat
   |   +---ico
   |   +---log
   |   +---objs
   |   +---plot
   |   +---plot_vfm
   |   +---polygon
   |   \---tools
   +---dat
   +---db
   |   \---manage_db
   \---docs
       +---source
           +---.idea
           +---analytics
           +---dev
           +---doc
           |   +---general
           |   +---polygon
           |   \---tools
           +---trouble
           \---_static


----------------------------------------
Features
----------------------------------------

.. class:: left: blank program, right: shapes form around selected areas of the plot

   .. image:: _static/program.png
      :scale: 20%

   .. image:: _static/programShapesActive.png
      :scale: 20%


VOCAL is still in a very early development phase

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
* ``Extract``: extract the shape data to a file
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

