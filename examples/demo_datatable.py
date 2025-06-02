from tkkit import *
from tkkit.view_model import ViewModel

# Create a ViewModel instance
vm = ViewModel()

# Initialize non - bindable header and data
header = ["Name", "Age", "City"]
static_people_data = [
    ["Alice", 25, "New York"],
    ["Bob", 30, "London"],
    ["Charlie", 22, "Paris"]
]

# Initialize bindable data
vm.people_data = [
    ["David", 28, "Tokyo"],
    ["Eve", 32, "Sydney"]
]

# Create the main application
app = TKApp('DataTable Example')


def add_row():
    new_row = ["Frank", 27, "Berlin"]
    vm.people_data.append(new_row)


def delete_row():
        vm.people_data.pop()

def update_cell():
        vm.people_data[0] = ["Frank", 29, "Berlin"]



# Arrange the UI elements
main_view = VStack([
    Label("Non-Bindable DataTable:"),
    DataTable(header, static_people_data),
    Label("Bindable DataTable:"),
    HStack([
        Button("Add Row", on_click=add_row),
        Button("Delete Row", on_click=delete_row),
        Button("Update Cell", on_click=update_cell)
    ]),
    DataTable(header, vm.people_data_, selected_index=vm.selected_index_, selected_item=vm.selected_item_),
    HStack([
        Label("Selected Index:"),
        Label(vm.selected_index_)
    ]),
    HStack([
        Label("Selected Item:"),
        Label(vm.selected_item_)
    ])
])

# Show the main view and run the application
app.show(main_view)
app.run()


