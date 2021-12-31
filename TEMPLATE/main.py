import Neutron

win = Neutron.Window("Example", size=(600, 100), css="def.css")
win.display(file="render.html")


def onClick():
    win.getElementById("title").innerHTML = "Hello:" + win.getElementById("inputName").value


win.getElementById("submitName").AddEventListener("click", Neutron.event(onClick))

win.show()
