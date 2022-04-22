![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Neutron allows developers to build native Python apps along with CSS and HTML for frontend design. Based on [pywebview](https://github.com/r0x0r/pywebview) for it's native GUI window and JavaScript-Python communication.

You can get started contributing via [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md) or **you can message me** on discord (**IanTheThird#9732**) if you want more insigths on the code and tips on what to contribute. 
## Installation

```
pip install neutron-web
```

## Building to EXE/APP/AN EXECUTABLE

> **Note:** This has only been tested on windows.

To build a Neutron project you first need pyinstaller, install pyinstaller throught pip: `pip install pyinstaller`. Then run the script below in your command prompt/terminal.

```
pyinstaller YOUR_PYTHON_FILE.py --noconsole --onefile --add-data="YOUR_HTML_FILE.html;." --add-data="YOUR_CSS_FILE.css;."
```

## Examples

For a fully set up example project see [TEMPLATE](https://github.com/IanTerzo/Neutron/tree/main/TEMPLATE). The project is build how it's intended, meaning it has a CSS and HTML file for the design and a Python file for the logic. (It is comparable to how websites using JavaScript are built).

### Other examples

Althought not recommended for big projects, it's possible to create an app using only a Python file.
```py
import Neutron

win = Neutron.Window("Example", css="def.css")

HeaderObject = Neutron.elements.Header(win, id="title", content="Hello")


def setName():
    HeaderObject.setAttribute("style", "color: red;")
    HeaderObject.innerHTML = "Hello world!"
    win.getElementById("submit").innerHTML = "clicked!"


Neutron.elements.Button(win, id="submit", content="Hi", onclick=Neutron.event(setName))

win.show()
```

Another example featuring in-python HTML:
```py
import Neutron

win = Neutron.Window("Example")

def setName():
    name = win.getElementById("inputName").value
    win.getElementById("title").innerHTML = "Hello: " + name


win.display(f"""

<!DOCTYPE html>
<html>
   <head lang="en">
      <meta charset="UTF-8">
   </head>
   <body>
      <h1 id="title">Hello: </h1>
      <input id="inputName">
      <button id="submitName" onclick="{Neutron.event(setName)}">Submit</button>
      <!-- OR-->
      {Neutron.elements.Button(win, content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```

To resolve the loading time issue, Neutron features a loader system seen here:
```py
import Neutron

win = Neutron.Window("Example", size=(600,100))

# The loader covers while all the other elements and css loads
win.loader(content="<h1>Loading App...</h1>", color="#fff", after=lambda: win.toggle_fullscreen())


def setName():
    name = win.getElementById("inputName").value
    win.getElementById("title").innerHTML = "Hello: " + name


win.display(f"""

<!DOCTYPE html>
<html>
   <head lang="en">
      <meta charset="UTF-8">
   </head>
   <body>
      <h1 id="title">Hello: </h1>
      <input id="inputName">
      <button id="submitName" onclick="{Neutron.event(setName)}">Submit</button>
      <!-- OR-->
      {Neutron.elements.Button(win, content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```
