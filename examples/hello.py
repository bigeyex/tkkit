from tkkit import *

app = TKApp('My App')

window = Window([                                   # the title of the app will be "My App"
    Row([Button('First Button'),                    # the first row, has two buttons
         Button('Second Button')]),
    Row([
        Column([TextBox(""), Label('A label')]),    # the second row has two columns 
        Column([
            ProgressBar(value=50),
            CheckBox('Checkbox One'),
            RadioButton('Radio 1', name="radios"),
            RadioButton('Radio 2', name="radios"),
            RadioButton('Radio 3', name="radios"),
        ]),
    ])
])

app.show(window)                                    # use show to display the window to the screen
app.run()                                           # don't forget call app.run() at the end.

