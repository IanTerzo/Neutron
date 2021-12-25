![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Create modern cross-platform apps in HTML and CSS with Python

## What is Neutron
Neutron allows developers to build native Python apps while using CSS and HTML for the design. Neutron will give full access to the DOM just as it would be in Javascript and  offer an easy scripting method to bind HTML with Python.

## Installation
At the moment there is no straightforward installation method using pip. So for now, it is only possible like this.

1 **Clone this repository.**

2 **Move the Neutron folder into the TEMPLATE folder.**

3 **Run main.py**

## Examples

For a fully set up example project see [TEMPLATE](https://github.com/IanTerzo/Neutron/tree/main/TEMPLATE). The project is build how it's intended, meaning it has a CSS and HTML file for the design and a Python file for the logic. (It is comparable to how websites using JavaScript are built).

### Other examples

Althought not recommended for big project, it is possible to create an app using only python.
```
import Neutron

win = Neutron.Window("Example", css="def.css")

HeaderObject = Neutron.Header(win, id="title", content="Hello")


def setName():
    HeaderObject.setAttribute("style", "color: red;")
    HeaderObject.innerHTML = "Hello world!"
    win.getElementById("submit").innerHTML = "clicked!"


Neutron.Button(win, id="submit", content="Hi", onclick=Neutron.event(setName))

win.show()
```

Another example featuring in-python HTML:
```
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
      {Neutron.Button(win, content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```

To resolve the loading time issue Neutron features a loader system.:
```
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
      {Neutron.Button(win, content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```

## Contributing
Contributions are welcome and in need! You can easily get started contributing by reading [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md)


