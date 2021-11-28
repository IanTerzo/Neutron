![](https://i.ibb.co/0hCHmNX/Asset-3.png)
# Neutron
Make desktop applications using HTML and CSS with python

## What is Neutron
Neutron will allow developers to design modern application in python using CSS and HTML in python. Neutron will provide a seamless integration with python and html, for example:

    
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
      <h1 id="title">Hello: </h1>a
      <input id="inputName">
      <button id="submitName" onclick="{Neutron.event(setName)}">Submit</button>
      <!-- OR-->
      {Neutron.Button(win, id="submitName2",content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```
 
## Contributing
Contributions are welcome and in need! You can easily get started coding by reading [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md)
