import Neutron

win = Neutron.Window("Example", size=(600, 400), css="def.css")
win.display(file="render.html")


def onClick():
    win.getElementById("title").innerHTML = "Hello:" + win.getElementById("inputName").value


win.getElementById("submitName").addEventListener("click", Neutron.event(onClick))

win.show()
