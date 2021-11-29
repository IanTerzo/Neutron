![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Create modern cross-platform apps in HTML and CSS with python

## What is Neutron
Neutron will allow developers to build complex python apps while using CSS and HTML for the design. Neutron will give full access to the DOM just as it would be in Javascript and will offer an easy scripting method to bind HTMl with Python.

For example:

```
import Neutron

win = Neutron.Window("Example", css="def.css")



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
      {Neutron.Button(win, id="submitName2",content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```
Neutron is still in it's alpha and phase and many feature are not out yet, but it is important to know that **the examples shown in this repo are always working**.

### CSS
As stated before Neutron allows developers to integrate CSS. Simply enter the CSS file's path in the Neutron.Window() object and then use CSS as you normally would.

 
## Contributing
Contributions are welcome and in need! You can easily get started contributing by reading [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md)

## Installation
At the moment there is no straight forward installation method. It is always possible to just clone the repo.
