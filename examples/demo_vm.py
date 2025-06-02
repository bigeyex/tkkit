from tkkit import *

app = TKApp('My App')
vm = ViewModel()
vm.text = "Hello"
vm.radio_value="Option 2"

def button_click():
    vm.text = "world"
    vm.list_value = "world"
    vm.checked = 1

view = HStack([
    VStack([
        Button(vm.text_, on_click=button_click),
        Label(vm.text_),
        Label(vm.checked_),
        TextBox(vm.text_),
        ComboBox(("hello", "world", "all"), vm.text_),
        ListBox(("hello", "world", "all"), value=vm.list_value_),
        CheckBox("Check Me", checked=vm.checked_),
        ShowIf(vm.checked_, [
            Label("Checkbox is checked!!"),
            Label("Checkbox is checked!!!"),
        ]),
        HStack([
           Label("Selected Radio"), Label(vm.radio_value_)
        ]),
        RadioGroup(value=vm.radio_value_, children=[
            RadioButton("Option 1", value="Option 1"),
            RadioButton("Option 2", value="Option 2"),
            RadioButton("Option 3", value="Option 3"),
        ]),
    
    ]),
    VStack([
        Slider(vm.slider_value_),
        ProgressBar(vm.slider_value_)
    ]),
    VStack([
        FilePicker(value=vm.file_value_),
        Label(vm.file_value_)
    ]),
])

app.show(view)
app.run()
