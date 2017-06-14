#
# avg_lidar_dataB.py
# Brian Magill
# 10/9/2013
#
# Translated from a MatLab script written by an unknown person
# Removed Frame Number option since it does not lead to useful
# results if number of profiles in average is anything other
# than 3 or 5.  (Perhaps incorporate it into a separate function?)
# 
#

import numpy as np
from numpy import ma

def avg_horz_data(data, N):
    """
    This function will average lidar data for N profiles.
    Inputs: 
        data - the lidar data to average. Profiles are assumed to be stored in columns and to be a masked array.
        N    - the number of profile to average

    Outputs:
        out - the averaged data array.

    """
    nAlts     = data.shape[0]
    nProfiles = data.shape[1]                                                  


    nOutProfiles = np.floor(nProfiles/N)
    out = np.zeros((int(nAlts), int(nOutProfiles)))
  
    for i in range(0, int(nOutProfiles) - 1): 
        out[:, i] = ma.mean(data[:, i*N:(i+1)*N - 1], axis=1)  
  
    return out
