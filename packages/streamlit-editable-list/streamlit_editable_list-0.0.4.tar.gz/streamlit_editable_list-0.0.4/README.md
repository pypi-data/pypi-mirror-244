# streamlit-editable-list

A Streamlit component to edit a list of entries, made of several inputs.


## Installation instructions

```sh
pip install streamlit-editable-list
```

## Usage instructions

```python
import streamlit as st

from streamlit_editable_list import editable_list

input_params = [
    {
        "type": "text",
        "placeholder": "Enter text",
        "value": "",
    },
    {
        "type": "number",
        "placeholder": "Enter number",
        "value": 0,
    },
    {
        "list": "countries",
        "placeholder": "Select country",
        "value": "",
        "options": ["Switzerland", "France", "Germany"],
    }
]

initial_data = [
    ["Hello", 1, "Switzerland"],
    ["World", 2, "France"],
]

new_data = editable_list(initial_data, input_params)
```

For use inside a Streamlit form, the `auto_save` option can be set to `True`:

```python
new_data = editable_list(initial_data, input_params, auto_save=True)
```

The Python data will be updated each time the user leaves an input field.
