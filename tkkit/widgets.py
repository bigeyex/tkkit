import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import threading

class Widget:
    # override if there's additional arguments
    def __init__(self, name=None, **kwargs):
        self.styles = kwargs
        self.name = name

    def bind_var(self): # override if there's binding variable, none for skipping
        return None
    
    def get_value(self):
        return self.var_to_bind.get()
    
    def set_value(self, value):
        self.var_to_bind.set(value)

    def show(self, parent): # should never be overridden
        self.name_registry = parent.name_registry
        self.parent = parent
        self.var_to_bind = self.bind_var()
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
        self.el = tk.Frame(parent.el, **self.styles)
        for index in range(0, len(self.children)):
            child_el = self.children[index].show(self)
            child_el.grid(row=index, column=0)
        return self.el
            
class Row(Column):
    def get_widget(self, parent):
        self.el = tk.Frame(parent.el, **self.styles)
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
    def __init__(self, text="", password=False, lines=1, scrollable=True, name=None, on_click=None, **kwargs):
        self.text = text
        self.password = password
        self.lines = lines
        self.scrollable = scrollable
        super().__init__(name=name, **kwargs)

    def bind_var(self):
        return tk.StringVar()
    
    def get_value(self):
        if self.lines > 1:
            return self.el.get('1.0', 'end')
        else:
            return self.var_to_bind.get()

    def get_widget(self, parent):
        show = '*' if self.password else None
        if self.text is not None and self.var_to_bind is not None:
            self.var_to_bind.set(self.text)
        if self.lines > 1:
            if self.scrollable:
                return ScrolledText(parent.el, height=self.lines, **self.styles)
            else:
                return tk.Text(parent.el, height=self.lines, **self.styles)
        else:
            return ttk.Entry(parent.el, textvariable=self.var_to_bind, show=show, **self.styles)
