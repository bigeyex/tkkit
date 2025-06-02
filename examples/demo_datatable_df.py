from tkkit import *
from tkkit.view_model import ViewModel
import pandas as pd

# Create a ViewModel instance
vm = ViewModel()

# Initialize a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 22],
    "City": ["New York", "London", "Paris"]
}
df = pd.DataFrame(data)

# Create a bindable DataFrame
vm.bindable_df = df

# Create the main application
app = TKApp('DataTable with DataFrame Example')

# Create a DataTable with the bindable DataFrame
window = VStack([
    DataTable(data_frame=vm.bindable_df_),
])

# Show the main view and run the application
app.show(window)
app.run()