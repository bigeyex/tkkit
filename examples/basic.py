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
