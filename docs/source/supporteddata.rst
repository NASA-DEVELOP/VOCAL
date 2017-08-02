Supported Data Types
====================

VOCAL uses a backend library called `ccplot`_ to pull data from inside the ``.hdf`` files, and thus are limited
in what ccplot supports.

+------------+------------+------------------------------------------------+-----------+
| Spacecraft | Instrument | Product                                        | Supported |
+============+============+================================================+===========+
| CALIPSO    | CALIOP     | Lidar L1B Profiles                             | Yes       |
+------------+------------+------------------------------------------------+-----------+
|            |            | Lidar L2 Cloud Layer Products(333m, 1km, 5km)  | Unknown   |
+------------+------------+------------------------------------------------+-----------+

.. note::

   Testing and support is planned for Lidar L2 Cloud Layer Products in the future

.. _ccplot: http://ccplot.org/
