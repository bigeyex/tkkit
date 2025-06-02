from tkinter import *
from tkinter import ttk
from .widgets import *
from .exceptions import *

class TKApp:
    def __init__(self, title=None):
        self.el = Tk()
        self.align = None
        self.vertical_align = None
        if title is not None:
            self.el.title(title)

    def show(self, window):
        if not isinstance(window, Container):
            raise LayoutException("root element has to be VStack or HStack") 
        self.name_registry = {}
        main_el = window.build(self)
        self.el.columnconfigure(0, weight=1)
        self.el.rowconfigure(0, weight=1)
        main_el.grid(row=0, column=0, sticky="wens")

    def replace(self, widget_name, new_widget):
        old_widget = self.name_registry[widget_name]
        grid_info = old_widget.el.grid_info()
        old_widget.el.grid_forget()
        new_el = new_widget.build(old_widget.parent)
        new_el.grid(row=grid_info['row'], column=grid_info['column'])
        

    def set_attr(self, widget_name, prop_name, value):
        self.name_registry[widget_name].el[prop_name] = value

    def set_text(self, widget_name, new_text):
        self.set_attr(widget_name, 'text', new_text)

    def get_value(self, widget_name):
        return self.name_registry[widget_name].get_value()
    
    def get_tk(self, widget_name):
        return self.name_registry[widget_name].el
    
    def set_value(self, widget_name, new_value):
        self.name_registry[widget_name].set_value(new_value)

    def run(self):
        self.el.mainloop()
