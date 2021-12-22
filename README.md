![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Create modern cross-platform apps in HTML and CSS with Python

## What is Neutron
Neutron allows developers to build complex Python apps while using CSS and HTML for the design. Neutron will give full access to the DOM just as it would be in Javascript and will offer an easy scripting method to bind HTML with Python.

## Installation
At the moment there is no straightforward installation method using pip. So for now, it is only possible like this.

1 **Clone this repository.**

2 **Move the Neutron folder into the TEMPLATE folder.**

3 **Run main.py**

You now have a template project to work with. For more examples read below.

## Examples
For example:
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
Neutron is still in it's alpha and phase and many feature are not out yet, but it is important to know that **the examples shown in this repo are always working and updating**.

Another example:
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

First example but with a loader:
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

### CSS
As stated before Neutron allows developers to integrate CSS. Simply enter the CSS file's path in the Neutron.Window() object and then use CSS as you normally would.

## Contributing
Contributions are welcome and in need! You can easily get started contributing by reading [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md)


