# regrid_lidar.py
# translated by Brian Magill
# 12/31/2013
#
import numpy as np
from scipy import interpolate

def regrid_lidar(alt, inMatrix, new_alt, method = 'linear'):
#
# This function will regrid the matrix inMatrix defined by the (Nx1) vector 'alt'
# onto the new grid (Jx1) 'new_alt'.
# The assumption is that the horizontal dimension changes column by
# column, and altitude is stored row by row (e.g. row x col == alt x (dist
# or time).
#
# Note that all values outside of bounds are returned as NaN's
# For interp1d to work, the ordinate array has to be monotonically increasing
# This is why the altitude and inMatrix arrays have been reversed in their
# common dimension.  
#

    interpFunc = interpolate.interp1d(alt[::-1], inMatrix[::-1,:], kind=method, 
                                      axis=0, bounds_error=False)
    return interpFunc(new_alt)

#
# Quick 'n dirty test to see if it works

if __name__ == '__main__':
    in_matrix = np.array([[   0.,    0.,    0.],
                          [  20.,   30.,   50.],
                          [  40.,   60.,  100.],
                          [  60.,   90.,  150.],
                          [  80.,  120.,  200.]])
       
    x_in = np.array([  0.,  10.,  20.,  30.,  40.])
    x_out = np.array([  5.,  10., 15.,  25.,  35.,  37., 45.])
    out_matrix = regrid_lidar(x_in, in_matrix, x_out)
    print "x_in = ", x_in
    print "in_matrix = ", in_matrix
    print "x_out = ", x_out
    print "out_matrix = ", out_matrix
