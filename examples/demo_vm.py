from tkkit import *

app = TKApp('My App')
vm = ViewModel()
vm.text = "Hello"

def button_click():
    vm.text = "world"
    vm.checked = 1

view = VStack([
    Button(vm.text_, on_click=button_click),
    Label(vm.text_),
    Label(vm.checked_),
    TextBox(vm.text_),
    ComboBox(("hello", "world", "all"), vm.text_),
    ListBox(("hello", "world", "all")),
    CheckBox("Check Me", checked=vm.checked_)
])

app.show(view)
app.run()
