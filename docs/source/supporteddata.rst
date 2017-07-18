Supported Data Types
====================

VOCAL uses a backend library called `ccplot`_ to pull data from inside the ``.hdf`` files, and thus are limited
in what ccplot supports.

+------------+------------+-----------------------------------------------+-------------------+-----------+
| Spacecraft | Instrument | Product                                       | Includes          | Supported |
+============+============+===============================================+===================+===========+
| CALIPSO    | CALIOP     | Lidar L1B Profiles                            | * Backscatter     | Yes       |
|            |            |                                               | * Depolarization  |
+------------+------------+-----------------------------------------------+-------------------+-----------+
|            |            | Lidar L2 Vertical Feature Mask                | * VFM             | Yes       |
|            |            |                                               | * Ice/Water Phase |           |
|            |            |                                               | * Aerosol Subtype |           |
+------------+------------+-----------------------------------------------+-------------------+-----------+

.. note::

   Several other features are included in the L2 Vertical Feature Mask files such as:
      * Cloud Subtype
      * Polar Stratospheric Cloud Subtype
      * Quality Assurance on all data products

   Which may be implemented later.

.. _ccplot: http://ccplot.org/
