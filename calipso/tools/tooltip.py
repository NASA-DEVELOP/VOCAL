######################################
#    tooltip.py
#    @author: Grant Mercer
#    6/24/2015
######################################
from Tkinter import Toplevel, TclError, Label, LEFT, SOLID

class ToolTip(object):
    '''
    Displays text in a label below a passed widget
    
    :param widget: The widget tooltip will be binding text to
    '''
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.x = self.y = 0

    # Parameter: text to display as tooltip
    def showTip(self, text):
        '''
        Create and pack the tooltip, bound to the ``'<Enter>'`` event when
        :py:func:`createToolTip` is called
        
        :param str text: string to place inside label
        '''
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")  # @UnusedVariable
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipWindow = tw = Toplevel(self.widget)
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

    def hideTip(self):
        '''
        Hide or destory the tool tip label when the mouse leaves widget.
        Bound to the ``'<Leave>'`` event when :py:func:`createToolTip` is called
        '''
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    '''
    Create an instance of :py:class:`ToolTip` and bind the ``'<Enter>'`` and
    ``'<Leave>'`` events for displaying to the widget passed
    
    :param widget: the widget for the tooltip to be displayed below
    :param str text: text contained in the tooltip
    '''
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showTip(text)
    def leave(event):
        toolTip.hideTip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)