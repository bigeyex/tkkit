from tkinter import *
from tkinter import ttk
import threading

class Widget:
    def __init__(self, name=None, **kwargs):
        self.styles = kwargs
        self.name = name

    def show(self, parent):
        self.name_registry = parent.name_registry
        self.var_registry = parent.var_registry
        if self.name is not None:
            self.name_registry[self.name] = self
        self.el = self.get_widget(parent)
        return self.el

    def get_widget(self, parent):
        raise NotImplementedError('get_widget is not implemented')


class Column(Widget):
    def __init__(self, children=[], name=None, **kwargs):
        self.children = children
        super().__init__(name=name, **kwargs)
    
    def get_widget(self, parent):
        self.el = Frame(parent.el, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=index, column=0)
        return self.el
            
class Row(Column):
    def get_widget(self, parent):
        self.el = Frame(parent.el, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=0, column=index)
        return self.el

class Window(Column):
    pass

class Button(Widget):
    def __init__(self, text="Button", name=None, on_click=None, **kwargs):
        self.text = text
        self.on_click = on_click
        super().__init__(name=name, **kwargs)

    def handle_click(self):
        handler_thread = threading.Thread(target=self.on_click, daemon=True)
        handler_thread.start()

    def get_widget(self, parent):
        command = self.handle_click if self.on_click is not None else None
        return ttk.Button(parent.el, text=self.text, command=command, **self.styles)
    
class Label(Widget):
    def __init__(self, text="Label", name=None, on_click=None, **kwargs):
        self.text = text
        super().__init__(name=name, **kwargs)

    def get_widget(self, parent):
        return ttk.Label(parent.el, text=self.text, **self.styles)
    
class TextBox(Widget):
    def get_widget(self, parent):
        return ttk.Entry(parent.el, **self.styles)