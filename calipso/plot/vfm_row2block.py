import numpy as np


def vfm_row2block(vfm_row):
    """
    Description: Rearanges a vfm row to a 2d grid
    Inputs: vfm_row - an array 1 x 5515

    Outputs: block - 2d array of vfm data, see function vfm_altitude for
            altitude array information. Altitude array is in similar format as
            CALIPSO L1 profile data (i.e. it isn't uniform).

    Translated from Matlab:
    Brian Magill
    10/16/2013

    Written by Ralph Kuehn
    3/24/2005

    The layout of a row of VFM data is described at
    http://www-calipso.larc.nasa.gov/resources/calipso_users_guide/data_summaries/vfm/index.php#feature_classification_flags
    under the heading 'Layout of the Feature Classification Flag data block.'
    """

    #   For higher altitude data, info will be over-sampled in horizontal dimension
    #   for 8-20km block it will be 200x15 = 3000 rather than 200x5 = 1000
    #   for 20-30 km block it will be 55x15 = 825, rather than 55x3 = 165

    #   Resolutions defined here are defined in terms of lengths of index numbers
    #
    HIGH_ALT_RES = 55
    MID_ALT_RES = 200
    LOW_ALT_RES = 290
    ALT_DIM = HIGH_ALT_RES + MID_ALT_RES + LOW_ALT_RES

    block = np.ones((ALT_DIM, 15), dtype=np.uint8)
    offset = 0
    step = HIGH_ALT_RES
    indA = 0
    indB = HIGH_ALT_RES

    for i in range(3):

        iLow = offset + step * i
        iHi = iLow + step

        n = i * 5
        #        block[indA:indB, n:n+4] = vfm_row[iLow:iHi]

        for k in range(5):
            block[indA:indB, n + k] = vfm_row[iLow:iHi]

    offset = 3 * HIGH_ALT_RES
    step = MID_ALT_RES
    indA = HIGH_ALT_RES
    indB = HIGH_ALT_RES + MID_ALT_RES

    for i in range(5):

        iLow = offset + step * i
        iHi = iLow + step

        n = i * 3
        #        block[indA:indB, n:n+2] = vfm_row[iLow:iHi]

        for k in range(3):
            block[indA:indB, n + k] = vfm_row[iLow:iHi]

            # element 1,1 correspond to Alt -0.5km, position -2.5 km from center lat lon.

    offset = 3 * HIGH_ALT_RES + 5 * MID_ALT_RES
    step = LOW_ALT_RES
    indA = HIGH_ALT_RES + MID_ALT_RES
    indB = ALT_DIM

    for i in range(15):
        iLow = offset + step * i
        iHi = iLow + step
        block[indA:indB, i] = vfm_row[iLow:iHi]

    return block
