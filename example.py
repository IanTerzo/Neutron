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
      {Neutron.Input(win, "inputName", onkeydown=Neutron.event(setName))}
      <!-- OR-->
      <button id="submitName" class="center" onclick="{Neutron.event(setName)}">Submit</button>
   </body>
</html>
""")
win.show()
