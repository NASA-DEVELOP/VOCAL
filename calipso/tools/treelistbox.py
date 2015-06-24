from Tkinter import Scrollbar, VERTICAL, HORIZONTAL, RIGHT, BOTTOM, \
    X, Y, NO, YES, BOTH
import ttk, tkFont, re

class TreeListBox(object):
    '''
    Class that internally handles a TreeView widget which creates 
    a columned view of the information from the database
    '''
    def __init__(self, root, headers):
        '''
        Initialize any variables used in treelistbox, the list is the actual
        information being displayed, the headers are what appears in the columns
        and the tree is the TreeView object
        '''
        self.info = list()
        self.headers = headers
        self.__root = root
        self.tree = ttk.Treeview(self.__root, columns=self.headers, show="headings")
        # create scrollbars and pack window
        yScrollBar = Scrollbar(self.__root, orient=VERTICAL, command=self.tree.yview)
        xScrollBar = Scrollbar(self.__root, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=yScrollBar.set, xscrollcommand=xScrollBar.set)
        yScrollBar.pack(side=RIGHT, fill=Y, expand=NO)
        xScrollBar.pack(side=BOTTOM, fill=X, expand=NO)
        self.tree.pack(expand=YES, fill=BOTH)
        
        for col in self.headers:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
    
    def update(self):
        '''
        Redisplay any information updated in self.list to the screen
        '''
        # create a treeview with dual scrollbar
        self.tree.delete(*self.tree.get_children(''))
        
        for item in self.info:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.headers[ix],width=None)<col_w:
                    self.tree.column(self.headers[ix], width=col_w)
        self.tree.pack(fill=BOTH, expand=YES)

def sortby(tree, col, descending):
    '''
    Sorts the treeview by the column clicked by the user
    
    :param Treeview tree: The tree object to sort
    :param str col: The column to sort
    :param bool descending: Boolean value to switch between sorting from ascending or descending
    '''
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data = change_numeric(data)
    # now sort the data in place
    convert = lambda text : int(text) if text.isdigit() else text
    alphanum_key = lambda key : [convert(c) for c in re.split('([0-9]+)', key[0])]
    data.sort(key=alphanum_key, reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
    int(not descending)))