#
#   interprete_vfm_type.py
#   Brian Magill
#   7/25/2014
#
import numpy as np

mask_3bits = np.uint16(7)
mask_2bits = np.uint16(3)
mask_1bit = np.uint16(1)

def extract_type(vfm_array):
    """
    Extracts feature type for each element in a vertical feature mask array:

        0 = invalid (bad or missing data)
        1 = 'clear air'
        2 = cloud
        3 = aerosol
        4 = stratospheric feature
        5 = surface
        6 = subsurface
        7 = no signal (totally attenuated)

    """

    return np.bitwise_and(mask_3bits, vfm_array)

def extract_qa(vfm_array):
    """
    Extracts quality assurance information for each element of the array:
    
        0 = none
        1 = low
        2 = medium
        3 = high
    """ 
    shifted = np.right_shift(vfm_array, 3)
    return np.bitwise_and(mask_2bits, shifted)

def extract_water_phase(vfm_array):
    """
    Where applicable,extracts water phase for each element of the array:
    
        0 = unknown / not determined
        1 = randomly oriented ice
        2 = water
        3 = horizontally oriented ice        
    """ 
    shifted = np.right_shift(vfm_array, 5)
    return np.bitwise_and(mask_2bits, shifted)

def extract_water_phase_qa(vfm_array):
    """
    Extracts water phase quality assurance information for each element 
    of the array:

        0 = none
        1 = low
        2 = medium
        3 = high    
    
    """ 
    shifted = np.right_shift(vfm_array, 7)
    return np.bitwise_and(mask_2bits, shifted)

def extract_sub_type(vfm_array):
    """
    Extracts the subtype for each element of the array.  Its 
    interpretation depends on whether the feature is an aerosol,
    cloud, or Polar Stratospheric Cloud.
    
    Aerosol:

        0 = not determined
        1 = clean marine
        2 = dust
        3 = polluted continental
        4 = clean continental
        5 = polluted dust
        6 = smoke
        7 = other  
          
    Cloud:
    
        0 = low overcast, transparent
        1 = low overcast, opaque
        2 = transition stratocumulus
        3 = low, broken cumulus
        4 = altocumulus (transparent)
        5 = altostratus (opaque)
        6 = cirrus (transparent)
        7 = deep convective (opaque)   
        
    Polar Stratospheric Cloud:

        0 = not determined
        1 = non-depolarizing PSC
        2 = depolarizing PSC
        3 = non-depolarizing aerosol
        4 = depolarizing aerosol
        5 = spare
        6 = spare
        7 = other    
     
    """ 
    shifted = np.right_shift(vfm_array, 9)
    return np.bitwise_and(mask_3bits, shifted)

def extract_type_confidence(vfm_array):
    """
    Extracts the degree of confidence that the feature type has been
    determined correctly:
    
        0 = not confident
        1 = confident   
    
    """ 
    shifted = np.right_shift(vfm_array, 12)
    return np.bitwise_and(mask_1bit, shifted)

def extract_aerosol_subtype(vfm_array):
    """
    Extracts the aerosol sub type using extract_type and extract_sub_type

        0 = not determined
        1 = clean marine
        2 = dust
        3 = polluted continental
        4 = clean continental
        5 = polluted dust
        6 = smoke
        7 = other
    """
    feature_type = extract_type(vfm_array)
    aerosol_sub_type = extract_sub_type(vfm_array)

    # Iterate through both arrays and mask sub type values where the feature type is not 3
    for i,j in np.nditer([feature_type, aerosol_sub_type], op_flags=['readwrite']):
        if i != 3:
            j[...] = 0
    return aerosol_sub_type

def extract_horiz_avg(vfm_array):
    """
    Extracts the identifier for the ammount of horizontal averaging:
    
        0 = not applicable
        1 = 1/3 km
        2 = 1 km
        3 = 5 km
        4 = 20 km
        5 = 80 km
    .
    """ 
    shifted = np.right_shift(vfm_array, 13)
    return np.bitwise_and(mask_3bits, shifted)

#low/no confidence needs to be accounted for, not sure how to do this, bitwise numbers need to be reclassified
Feature_Type = dict(fieldDescription = 'Feature Type',
              byteText =['Invalid','Clear Air','Cloud','Aerosol','Stratospheric Layer',
                        'Surface','Subsurface','Totally Attenuated'])

Feature_Type_QA = dict(fieldDescription ='Feature Type QA',
                      byteText = ['Clear Air','No','Low','Medium','High'])

Water_Phase = dict(fieldDescription = 'Ice/Water Phase', 
                byteText = ['Unknown/Not Determined','Ice','Water','HO'])

Phase_QA    = dict(fieldDescription = 'Ice/Water Phase QA', 
                byteText = ['None','Low','Medium','High'])

Aerosol     = dict(fieldDescription = 'Aerosol Sub-Type', 
                byteText = ['Not Determined','Clean Marine','Dust','Polluted Cont.','Clean Cont.',
                             'Polluted Dust','Smoke','Other'])

Cloud       = dict(fieldDescription = 'Cloud Sub-Type', 
                byteText = ['NA','Low, overcast, thin','Low, overcast, thick','Trans. StratoCu','Low Broken',
                             'Altocumulus','Altostratus','Cirrus (transparent)','Deep Convection'])

PSC         = dict(fieldDescription = 'PSC Sub-Type', 
                byteText = ['Not Determined','Non-Depol. Large P.','Depol. Large P.','Non-Depol Small P.','Depol. Small P.',
                             'empty','empty','Other'])

Type_Confidence = dict(fieldDescription = 'Sub-Type QA', 
                   byteText = ['None','Low','Medium','High'])                            

Horizontal_Avg  = dict(fieldDescription = 'Averaging Required for Detection', 
                byteText = ['NA','1/3 km','1 km','5 km','20 km','80 km'])
