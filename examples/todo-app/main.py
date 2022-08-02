from asyncio import tasks
from tkinter import W
import Neutron
from bs4 import BeautifulSoup

# All the CSS and HTML in this example is based on https://bbbootstrap.com/snippets/todo-list-jquery-and-font-awesome-icons-77769811

win = Neutron.Window("Example", size=(800, 500), css="def.css")

tasks = [0, 1, 2]

def CreateTask(key):
    if key == "Enter":
        taskName = win.getElementById("addTask").value
        taskId = len(tasks)

        tasks.append(taskId)
        
        taskHtml = f'<li id="task{taskId}"><span onclick="RemoveTask(this.parentNode.id)"><i class="fa fa-trash">X</i></span> {taskName}</li>'
        win.getElementById("tasks").append(taskHtml)

def RemoveTask(taskid):
    win.getElementById(taskid).remove()
    

win.display(file="render.html", pyfunctions=[CreateTask, RemoveTask])

win.show()
