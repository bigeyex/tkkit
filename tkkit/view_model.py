from enum import Enum
from tkinter import Variable
from typing import Callable, Any

class BindedListUpdateType(Enum):
    INSERT = "insert"
    SETITEM = "setitem"
    REMOVE = "remove"
    POP = "pop"
    EXTEND = "extend"
    INSERT_AT = "insert_at"
    SORT = "sort"
    REVERSE = "reverse"
    DELETE_ROW = "delete_row"
    SET_CELL = "set_cell"

class BindedList(list):
    def __init__(self, notify_func: Callable[[BindedListUpdateType, Any], None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notify_func = notify_func

    def append(self, item):
        super().append(item)
        self.notify_func(BindedListUpdateType.INSERT, item)

    def __setitem__(self, index, value):
        if isinstance(value, list):
            # If setting a row, check if it's a cell update
            if isinstance(self[index], list) and len(self[index]) == len(value):
                for i in range(len(value)):
                    if self[index][i] != value[i]:
                        self.notify_func(BindedListUpdateType.SET_CELL, (index, i, value[i]))
        super().__setitem__(index, value)
        self.notify_func(BindedListUpdateType.SETITEM, (index, value))

    def remove(self, value):
        index = self.index(value)
        super().remove(value)
        self.notify_func(BindedListUpdateType.DELETE_ROW, index)

    def pop(self, index=-1):
        # Calculate the real index when using negative index
        if index < 0:
            index = len(self) + index
        value = super().pop(index)
        self.notify_func(BindedListUpdateType.DELETE_ROW, index)
        return value

    def extend(self, iterable):
        super().extend(iterable)
        self.notify_func(BindedListUpdateType.EXTEND, iterable)

    def insert(self, index, value):
        super().insert(index, value)
        self.notify_func(BindedListUpdateType.INSERT_AT, (index, value))

    def sort(self, *, key=None, reverse=False):
        super().sort(key=key, reverse=reverse)
        self.notify_func(BindedListUpdateType.SORT, None)

    def reverse(self):
        super().reverse()
        self.notify_func(BindedListUpdateType.REVERSE, None)

    def delete_row(self, index):
        """Custom method to delete a row and notify listeners."""
        del self[index]
        self.notify_func(BindedListUpdateType.DELETE_ROW, index)

    def set_cell(self, row_index, col_index, value):
        """Custom method to set a cell value and notify listeners."""
        self[row_index][col_index] = value
        self.notify_func(BindedListUpdateType.SET_CELL, (row_index, col_index, value))

class ViewModelBindable[T]:
    def __init__(self, vm, attr_name:str):
        self.vm = vm
        self.attr_name = attr_name
        self.listeners = []
        # Wrap list with BindedList if the value is a list
        value = getattr(self.vm, self.attr_name)
        if isinstance(value, list):
            setattr(self.vm, self.attr_name, BindedList(self._notify_list_change, value))

    def _notify_list_change(self, change_type: BindedListUpdateType, data: Any):
        value = getattr(self.vm, self.attr_name)
        for listener in self.listeners:
            try:
                listener(value, change_type, data)
            except TypeError:
                listener(value)

    def on_change(self, callback:Callable[[T], None]):
        self.listeners.append(callback)
        return self
    
    def get_value(self) -> T:
        return getattr(self.vm, self.attr_name)
    
    def set_value(self, new_value:T) -> None:
        if isinstance(new_value, list):
            new_value = BindedList(self._notify_list_change, new_value)
        return setattr(self.vm, self.attr_name, new_value)

    def notify(self) -> None:
        """
        Notify all listeners that the value has changed.
        """
        value = getattr(self.vm, self.attr_name)
        # Pass the new value to the listener
        for listener in self.listeners:
            try:
                listener(value)
            except TypeError:
                # Handle callbacks that expect list change details
                if isinstance(value, BindedList):
                    pass  # List changes are handled by _notify_list_change

    def connect_tk_var(self, tk_var:Variable, true_to_one=False) -> None:
        # Update Tkinter variable when ViewModelBindable changes
        def update_tk_var(value):
            # Only update tk_var if the value is different
            tk_value = value
            if true_to_one: # used to convert tk Variable's checkbox binding
                tk_value = 1 if value else 0
            if tk_value != tk_var.get():
                tk_var.set(tk_value)

        self.on_change(update_tk_var)

        # Update ViewModelBindable when Tkinter variable changes
        def update_view_model(*args):
            new_value = tk_var.get()
            if true_to_one:
                new_value = True if new_value else False
            setattr(self.vm, self.attr_name, new_value)

        tk_var.trace_add("write", update_view_model)


class ViewModel:
    """
        usage:
            vm = ViewModel()
            vm.text = "Hello"
            Label(vm.text_) # bind vm.text to Label's text property
            vm.text = "World" # Label's text property will be updated
    """
    def __init__(self):
        self._listeners = {} # attr_name -> ViewModelBindable

    def __getattribute__(self, name:str):
        if name.endswith('_'):
            attr_name = name[:-1]
            if attr_name not in self._listeners:
                self._listeners[attr_name] = ViewModelBindable(self, attr_name)
            return self._listeners[attr_name]
        return object.__getattribute__(self, name)
    
    def __getattr__(self, name):
        return 0

    def __setattr__(self, name, value):
        old_value = None
        if hasattr(self, name):
            old_value = getattr(self, name)
        object.__setattr__(self, name, value)
        # Use a more robust comparison
        if (value.__class__.__name__ == "DataFrame" or old_value != value and (old_value is not None or value is not None)) and name in self._listeners:
            self._listeners[name].notify()