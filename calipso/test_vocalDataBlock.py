import tools.vocalDataBlock as vocalDataBlock
import sys


def test_vocal_data_class():
    test_arguments = vocalDataBlock.MetaData(in_type=1, in_x_min=0, in_x_max=15000, in_y_min=0, in_y_max=30.0, in_wavelength=532)
    '''filenameL1 = "C:\Users\Joseph\Documents\VOCALTestData\CAL_LID_L1-Test0011-Mod001-V4-XX.2007-10-17T18-24-58ZD.hdf"
    filenameL2 = "C:\Users\Joseph\Documents\VOCALTestData\CAL_LID_L2_01kmCLay-Test0011-Mod001-V4-XX.2007-10-17T18-24-58ZD.hdf"

    my_data_block1 = vocalDataBlock.VocalDataBlock(filenameL1)
    my_data_block1.set_working_meta(test_arguments)
    my_data_block1.print_working_metadata()


    temp = my_data_block1.get_figure(test_arguments)
    print temp'''
