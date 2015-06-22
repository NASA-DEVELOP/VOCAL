"""
Demo of image that's been clipped by a circular patch.
"""
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook


image_file = cbook.get_sample_data('grace_hopper.png')
image = plt.imread(image_file)

fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((260, 200), radius=200, transform=ax.transData)
im.set_clip_path(patch)

plt.axis('off')
plt.show()
"""

import Tkinter as tk
import tkFont
import ttk
class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        
    def _setup_widgets(self):
        s = """\
        click on header to sort by that column
        to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
        padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
        command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
        command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
        xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
    
    def _build_tree(self):
        for col in car_header:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))
        for item in car_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)
                    

    
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
    for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data = change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
    int(not descending)))
    
# the test data ...
car_header = ['car', 'repair']
car_list = [
('Hyundai', 'brakes') ,
('Honda', 'light') ,
('Lexus', 'battery') ,
('Benz', 'wiper') ,
('Ford', 'tire') ,
('Chevy', 'air') ,
('Chrysler', 'piston') ,
('Toyota', 'brake pedal') ,
('BMW', 'seat')
]
root = tk.Tk()
root.wm_title("multicolumn ListBox")
mc_listbox = McListBox()
root.mainloop()