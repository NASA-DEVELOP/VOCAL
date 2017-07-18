Getting the Data
================

Data collected by the CALIPSO satellite is free to the public, all it takes is going through a couple
of steps to order the data. **Eosweb** is the primary distributor for the satellite, you can find their
webpage `here`__ and order data from `here`__.

Once at the order page, you can use either **EarthData Search** or the **ASDC Ordering Tool**. Each
has advantages and disadvantages, so test each to see which works best for you. Once you've decided
on the time and place you would like data, download it. The tool works with both Level One and Level
Two data, which come as HDF files entitled "CAL_LID_L1-Standard" and "CAL_LID-VFM_Standard" followed
by the version number, date, and time. Version 4.10 data is recommended, however other less verified
versions may work.

In order to view L1 and L2 data simultaneously, you will have to download L1 and L2 files with the
exact same date and time. In the **ASDC HTML Order Tool**, this is easily done by *ctrl + clicking*
on both the "CAL_LID_L1-Standard-V4-10" and "CAL_LID_VFM-Standard-V4-10" options under *Data Sets*.
**EarthData Search** provides a visual tool for selecting data. See the tour on their `website`__
for more details on its use. You will still want to download both L1 and L2 data.

Another option is to grab example data from ccplot's sourceforge page, which a simple CALIPSO data
file you can easily download and load into VOCAL right off the bat:

* `CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf`_

.. __: https://eosweb.larc.nasa.gov/
.. __: https://eosweb.larc.nasa.gov/order-data
.. __: https://search.earthdata.nasa.gov/search/project
.. _CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf: https://sourceforge.net/projects/ccplot/files/products/CAL_LID_L1-ValStage1-V3-01.2007-06-12T03-42-18ZN.hdf
