from tkinter import *
from tkinter import ttk

class TKApp:
    def __init__(self, title=None):
        self.el = Tk()
        if title is not None:
            self.el.title(title)

    def show(self, window):
        self.name_registry = {}
        main_el = window.show(self)
        main_el.grid(row=0, column=0)

    def replace(self, widget_name, new_widget):
        old_widget = self.name_registry[widget_name]
        grid_info = old_widget.el.grid_info()
        old_widget.el.grid_forget()
        new_el = new_widget.show(old_widget.parent)
        new_el.grid(row=grid_info['row'], column=grid_info['column'])
        

    def set_attr(self, widget_name, prop_name, value):
        self.name_registry[widget_name].el[prop_name] = value

    def set_text(self, widget_name, new_text):
        self.set_attr(widget_name, 'text', new_text)

    def get_value(self, widget_name):
        return self.name_registry[widget_name].get_value()
    
    def set_value(self, widget_name, new_value):
        self.name_registry[widget_name].set_value(new_value)

    def run(self):
        self.el.mainloop()
