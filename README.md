# tkkit
Make python GUI easy.

```python
from tkkit import TKApp, Button, Window, Row, Column


app = TKApp('My App')

window = Window([
    Row([Button('One'), Button('Two'), Button('Three')]),
    Row([
        Column([Button('One'), Button('Two')]),
        Column([Button('One')]),
        Column([Button('One'), Button('Two'), Button('Three')]),
    ])
])

app.show(window)
app.run()
```


# TODO
- [] common widgets: Slider, Spinbox, Progressbar, LabelFrame, Tabs
- [] support align of widgets
- [] picker widgets
- [] Release lib
- [] TreeView