=====================
Program Overview
=====================

The CALIPSO: Global Health & Air Quality project aims at creating a tool with the ability to classify aerosols within CALIPSO Data to help improve future research and decision making. The summer 2015 team consisting of Grant Mercer and Nathan Qian will build on the existing graphical user interface built by the previous team.

----------------------------------------
Abstract
----------------------------------------

This section will contain the abstract written by the Summer LaRC 2015 team

----------------------------------------
Information
----------------------------------------

* **Applied Sciences Natinoal Applications Addressed:**
     National App1, National App2, etc

* **Study Area:**
     Global

* **Study Period:**
     May 2000 - Nov 2010

* **Earth Observations & Parameters:**
     CALIPSO, CALIOP - Vertial Profile of Aerosols

* **Ancillary Datasets Utilized:**
     Provider & Dataset - Parameter (*examples below* )

     * USGS National Land Cover Dataset (NLCD)
     * NOAA Coastal Change Analysis Program (C-CAP) - regional land cover
     * EPA AIRNow PM:sub:`2.5` dataset - PM:sub:`2.5` measurements

* **Models Utilized:**
     Agency & Model Name ( *examples below* )

     * USGS National Invasive Species Forecasting System (ISFS)
     * NASA Regional Ocean Model System (ROMS)
     * NOAA Sea, Lake and Overland Surges from Hurricanes (SLOSH) model

Features
----------------------------------------

.. class:: left: blank program, right: shapes form around selected areas of the plot

   .. image:: _static/program.png
      :scale: 40%

   .. image:: _static/programShapesActive.png
      :scale: 40%


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

Additional features are still to come!


