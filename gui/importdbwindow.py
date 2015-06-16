from Tkinter import Toplevel, Entry, Button, Listbox, BOTH, LEFT, Frame, \
    RIGHT, TOP, Text, Label
from tools import center

class dbDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.title("Import from existing database")
        self.geometry('%dx%d+%d+%d' % (400, 600, 0, 0))
        center(self)
        
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.createTopFrame()
        self.createBottomFrame()

        #b = Button(self, text="OK", command=self.free)
        #b.pack(pady=5)
        #listbox = Listbox(self)
        #listbox.pack(fill=BOTH)
        
        
    def createTopFrame(self):
        self.top_frame = Frame(self.container)
        self.top_frame.pack(side="top", fill="x", expand=False)
        self.label = Label(self.top_frame, text="Search ")
        self.label.grid(row=0, column=0, padx=5, pady=10)
        self.e = Entry(self.top_frame)
        self.e.grid(row=0, column=1, padx=5, pady=10)
        
    def createBottomFrame(self):
        self.bottom_frame = Frame(self.container)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)
        self.separator = Frame(self.bottom_frame, relief="ridge", height=2, bg="gray")
        self.separator.pack(side="top", fill="x", expand=False)
        
    def free(self):
        self.destroy()