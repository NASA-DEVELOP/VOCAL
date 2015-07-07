'''
Created on Jul 7, 2015

@author: nqian
'''
from Tkconstants import TOP, BOTH, X, END
from Tkinter import Toplevel, Frame, StringVar, Label, Entry, Button


class ColorDialog(Toplevel):
    '''
    classdocs
    '''


    def __init__(self, root, shape, canvas):
        '''
        Constructor
        '''
        Toplevel.__init__(self, root, width=150, height=150)
        
        self.shape = shape
        if shape is False:
            self.destroy()
            return
        self.color = shape.get_color()
        self.red = self.color[1:3]
        self.green = self.color[3:5]
        self.blue = self.color[5:]
        self.title('Color Palette')
        self.canvas = canvas
        
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.top_frame = None
        self.bottom_frame = None
        
        self.create_top_frame()
        
    def create_top_frame(self):
        self.top_frame = Frame(self.container)
        self.top_frame.pack(side=TOP, fill=X, expand=False)
        
        red_string = StringVar()
        red_string.set('Red')
        red_label = Label(self.top_frame, textvariable=red_string)
        red_label.grid(row=0, column=0)
        
        green_string = StringVar()
        green_string.set('Green')
        green_label = Label(self.top_frame, textvariable=green_string)
        green_label.grid(row=0, column=1)
        
        blue_string = StringVar()
        blue_string.set('Blue')
        blue_label = Label(self.top_frame, textvariable=blue_string)
        blue_label.grid(row=0, column=2)
        
        self.red_entry = Entry(self.top_frame)
        self.red_entry.insert(END, self.red)
        self.red_entry.grid(row=1, column=0)
        
        self.green_entry = Entry(self.top_frame)
        self.green_entry.insert(END, self.green)
        self.green_entry.grid(row=1, column=1)
        
        self.blue_entry = Entry(self.top_frame)
        self.blue_entry.insert(END, self.blue)
        self.blue_entry.grid(row=1, column=2)
        
        paint_button = Button(self.top_frame, text='Paint', command=self.paint)
        paint_button.grid(row=2, column=1)
        
    def paint(self):
        self.red = self.red_entry.get()
        self.green = self.green_entry.get()
        self.blue = self.blue_entry.get()
        self.color = '#' + self.red + self.green + self.blue
        self.shape.get_itemhandler().set_facecolor(self.color)
        self.canvas.show()
        self.destroy()