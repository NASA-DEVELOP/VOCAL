######################################
#    tooltip.py
#    @author: Grant Mercer
#    6/24/2015
######################################
from Tkinter import Toplevel, TclError, Label, LEFT, SOLID


class ToolTip(object):
    """
    Displays text in a label below a passed widget

    :param widget: The widget tooltip will be binding text to
    """
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.x = self.y = 0
        self.text = ''

    # noinspection PyProtectedMember
    def show_tip(self, text):
        """
        Create and pack the tooltip, bound to the ``'<Enter>'`` event when
        :py:func:`createToolTip` is called

        :param str text: string to place inside label
        """
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox('insert')  # @UnusedVariable
        # Larger button should have the tip placed lower
        if self.widget.winfo_height() > 70:
            x = x + self.widget.winfo_rootx() + 50
            y = y + cy + self.widget.winfo_rooty() + 50
        else:
            x = x + self.widget.winfo_rootx() + 27
            y = y + cy + self.widget.winfo_rooty() + 27
        self.tipWindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry('+%d+%d' % (x, y))
        try:
            # For Mac OS
            tw.tk.call('::Tk::unsupported::MacWindowStyle',
                       'style', tw._w,
                       'help', 'noActivates')
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background='#ffffe0', relief=SOLID, borderwidth=1,
                      font=('tahoma', '8', 'normal'))
        label.pack(ipadx=1)

    def hide_tip(self):
        """
        Hide or destroy the tool tip label when the mouse leaves widget.
        Bound to the ``'<Leave>'`` event when :py:func:`createToolTip` is called
        """
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()


def create_tool_tip(widget, text):
    """
    Create an instance of :py:class:`ToolTip` and bind the ``'<Enter>'`` and
    ``'<Leave>'`` events for displaying to the widget passed

    :param widget: the widget for the tooltip to be displayed below
    :param str text: text contained in the tooltip
    """
    tool_tip = ToolTip(widget)

    # noinspection PyUnusedLocal
    def enter(event):
        tool_tip.show_tip(text)

    # noinspection PyUnusedLocal
    def leave(event):
        tool_tip.hide_tip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)