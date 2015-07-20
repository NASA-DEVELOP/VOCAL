from Tkconstants import RAISED
from Tkinter import MenuButton, TclError


class _SetIt:
    """
    Internal class for wrapping command into widget OptionMenu
    """
    def __init__(self, var, value, callback=None):
        self.__value = value
        self.__var = var
        self.__callback = callback

    def __call__(self, *args):
        self.__var.set(self.__value)
        if self.__callback:
            self.__callback(self.__value, *args)

class ShapeOptionMenu(MenuButton):
    """
    Custom OptionMenu which allows the user to select a value from
    a menu and update upon button click.
    """

    def __init__(self, master, variable, value, **kwargs):
        kw = {'borderwidth': 2, 'textvariable': variable,
              'indicatoron': 1, 'relief': RAISED, 'anchor': 'c',
              'highlightthickness': 2}
        Widget.__init__(self, master, 'menubutton', kw)
        self.widget_name = 'tk_optionmenu'
        menu = self.__menu = Menu(self, name='menu', tearoff=0)
        self.menuname = menu._w
        callback = kwargs.get('command')
        if 'command' in kwargs:
            del kwargs['command']
        if kwargs:
            raise TclError('unknown option -' + kwargs.keys()[0])
        menu.add_command(label=value,
                         command=_SetIt(variable, value, callback))
