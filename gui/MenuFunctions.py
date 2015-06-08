'''
Created on Jun 4, 2015

@author: Nathan Qian
'''
from Tkconstants import SUNKEN, LEFT, END
from Tkinter import Toplevel, Message, Button, Text
import tkFileDialog

from bokeh.colors import white

def exportImage():
    pass

def saveImage():
    pass

def saveAs():
    options = {}
    options['defaultextension'] = '.hdf'
    options['filetypes'] = [('CALIPSO Data files', '*.hdf'), ('All files', '*')]
    tkFileDialog.asksaveasfile(mode='w', **options)
    
def about(root): 
    filewin = Toplevel(root)
    filewin.title("About")
    T = Message(filewin, text="NASA DEVELOP \nLaRC Spring 2015 Term \n \nJordan Vaa (Team Lead) \nCourtney Duquette \nAshna Aggarwal")
    T.pack()
        
    btnClose = Button(filewin, text="Close", command=filewin.destroy)
    btnClose.pack()
    
def tutorial(root):
    filewin = Toplevel(root)
    T = Text(filewin, height=10, width=40, wrap='word')
    T.pack()
    T.insert(END, "This is a tutorial of how to use the CALIPSO Visualization Tool")   