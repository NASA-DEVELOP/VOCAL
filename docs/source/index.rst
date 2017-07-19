.. CALIPSO documentation master file, created by
   sphinx-quickstart on Tue Jun 09 15:49:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Visualization of Calipso
============================================================


The CALISPO satellite (Cloud-Aerosol Lidar and Infrared Pathfinder Satellite Observation) is a NASA
earth observation that analyzes aerosol particles suspended in the Earth's atmosphere. Researchers use
CALIPSO data to track the aerosol's global distribution, dispersion and source using a visualization tool. However,
researchers have a hard time tracking specific airborne objects as the current visualization tool that reads CALIPSO
data lacks features such as highlighting and sharing regions of data for tracking purposes. This tool is written in
IDL, an obscure, and propriety language which prevents users from making the necessary adjustments. To
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

Everything you'll need to know from installation to developing the application can be found here!
VOCAL aim's to have a very in depth doc page in order to promote open source development and allow for
VOCAL to evolve as the users see fit. Refer to the side bar on the left to navigate about the doc page,
and use the search button at the top corner if you're looking for specific areas.

Contents
============

.. toctree::
   :caption: User Documentation
   :maxdepth: 2

   overview
   installation
   gettingdata
   supporteddata
   tutorial
 
.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   dev/startdev
   dev/conventions
   dev/enviroment
   dev/docs
   dev/site
   doc/modules

* :ref:`genindex`
* :ref:`modindex`

.. toctree::
   :maxdepth: 2
   :caption: Support

   trouble/faq
   trouble/issuetracker
   trouble/contact


