from Tkinter import TclError, Label, LEFT, SOLID, Toplevel, Button, RAISED, \
    SUNKEN
    

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    
class ToggleableButton(Button):
    
    __isToggled = False
    __button = None
    __root = None
    __bindMap = []
    
    def __init__(self, master=None, cnf={}, **kw):
        Button.__init__(self, master, cnf, kw)
        
    def bind(self, root, bindKey):
        self.__bindMap.append((root, bindKey))
    
    def Toggle(self, toggle=False):
        if toggle:
            self.__root.config(cursor="")
            self.__button.config(relief=RAISED)
        else:
            self.__isToggled = not self.__isToggled
            if self.__isToggled:
                self.__root.config(cursor=self.cursor)
                self.__button.config(relief=SUNKEN)
                self.__keyBinds()
            else:
                self.__root.unbind(self.__bind)
                self.__drawplotCanvas.unbind(self.__bind)
                self.__root.config(cursor="")
                self.__button.config(relief=RAISED)