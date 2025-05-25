class ViewModelBindable:
    def __init__(self, vm, attr_name):
        self.vm = vm
        self.attr_name = attr_name
        self.listeners = []

    def on_change(self, callback):
        self.listeners.append(callback)
        return self
    
    def get_value(self):
        return getattr(self.vm, self.attr_name)

    def notify(self):
        value = getattr(self.vm, self.attr_name)
        # Pass the new value to the listener
        for listener in self.listeners:
            listener(value)

    def connect_tk_var(self, tk_var, true_to_one=False):
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
    def __init__(self):
        self._listeners = {}

    def __getattribute__(self, name):
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
        if old_value != value and (old_value is not None or value is not None) and name in self._listeners:
            self._listeners[name].notify()