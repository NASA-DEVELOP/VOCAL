#
#   findLatIndex.py
#   Brian Magill
#   8/22/2014
#
import numpy as np

def findLatIndex(lat, lat_array):
    """
    For finding the index that corresponds to a latitude in the latitude
    array.
    """
    if lat_array[0] < lat_array[-1]:
        isAscending = True  
    else:
        isAscending = False

    if lat >= 0:
        indices = np.where(lat_array > lat)[0]
        if len(indices) == 0:
            index = np.argmax(lat_array)  
        elif isAscending:
            index = indices[0]
        else: 
            index = indices[-1]
    else:
        indices = np.where(lat_array < lat)[0]
        if len(indices) == 0:
            index = np.argmin(lat_array)
        elif isAscending:
            index = indices[-1]
        else: 
            index = indices[0]
   
    return index
