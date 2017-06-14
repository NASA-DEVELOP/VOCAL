#
# uniform_alt_2.py
# Translated by Brian Magill
# 12/31/2013
#
import numpy as np

#
# Description (8/2013):  Builds a uniformly spaced altitude grid above region 2
# of the CALIOP lidar data.  The spacing is 30 km.  From what I have been told
# the idea here is to have a 30 km spacing instead of 60 km.  Note that the altitude
# is stored in descending order.
# 
# Parameters:
#   max_altitude        - [in] maximum altitude for grid (should be above region 2)
#   old_altitude_array  - [in] region 2 altitudes
#
#   new_alt             - [out] output array with region 2 and above
#
def uniform_alt_2(max_altitude, old_altitude_array):

    D_ALT = 0.03 # spacing is 30 km
    MID_RES_TOP = 288
    MID_RES_BOT = 576

    # Altitude indices for high res altitude region (region 2):
    # 288:576
    
    alt2 = old_altitude_array[MID_RES_TOP:MID_RES_BOT]

    new_num_bins = np.ceil((max_altitude-alt2[0])/D_ALT)

    new_length = new_num_bins + len(alt2)

    new_alt = np.zeros(int(new_length))
    new_alt[int(new_num_bins):int(new_length)] = alt2

    upper_altitudes =  (np.arange(new_num_bins) + 1.)*D_ALT
    new_alt[:int(new_num_bins)] = new_alt[int(new_num_bins)] + upper_altitudes[::-1]

    return new_alt
