
# Neutron to-dos list

### HTML

- [ ] Finish all DOM methods

(Inside the window class in `__init__.py`, DOM method: i.e getElementById)

- [ ] Iframe to window communication

(In `elements.py`)

### OTHER
- [ ] A way to get what HTMLelement is calling the Neutron.event()

example:
```
<button id="task1" onclick="{Neutron.event(onClick)}">Submit</button>
<button id="task2" onclick="{Neutron.event(onClick)}">Submit</button>

def onClick(caller):
    print(caller.id) #task1, task2, depending on wich is clicked
```

- [ ] Finish the HTMLelement class

(In `elements.py`, for example HTMLelement.style attribute)

- [ ] In-python css 

`window(css='SomeInPythonCss')`

- [ ] System to make custom web components


### COMPLETED TO-DOS
- [x] JavaScript-Python bridge
- [x] Finish all HTML elements

