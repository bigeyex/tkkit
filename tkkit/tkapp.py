from tkinter import *
from tkinter import ttk

class TKApp:
    def __init__(self, title=None):
        self.el = Tk()
        if title is not None:
            self.el.title(title)

    def show(self, window):
        self.name_registry = {}
        self.var_registry = {}
        main_el = window.show(self)
        main_el.pack(side='left', fill='both')

    def set(self, widget_name, prop_name, value):
        self.name_registry[widget_name].el[prop_name] = value

    def set_text(self, widget_name, new_text):
        self.set(widget_name, 'text', new_text)

    def run(self):
        self.el.mainloop()
