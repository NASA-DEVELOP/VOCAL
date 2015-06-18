'''
Created on Jun 15, 2015

@author: Grant Mercer

'''

from Tkinter import Toplevel

class attributesDialog(Toplevel):
    '''
    Dialog window for creating and assigning attributes to objects
    '''
    def __init__(self, root, master):
        '''
        Initialize root tkinter window and master GUI window
        '''
        self.__root = root
        self.__master= master