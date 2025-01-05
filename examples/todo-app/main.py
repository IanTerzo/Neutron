import Neutron

# All the CSS and HTML in this example is based on https://bbbootstrap.com/snippets/todo-list-jquery-and-font-awesome-icons-77769811

win = Neutron.Window("Example", size=(800, 500), css="def.css")

tasks = [0, 1, 2]

def CreateTask(key):
    if key == "Enter":
        taskId = len(tasks)
        tasks.append(taskId)

        taskName = win.getElementById("addTask").value

        # Create task element

        taskHtml = f'<li id="task{taskId}"><span onclick="RemoveTask(this.parentNode.id)"><i class="fa fa-trash">X</i></span> {taskName}</li>'
        win.getElementById("tasks").append(taskHtml)

        # Or you can do it like this...

        """
        task = win.createElement("li")
        task.id = f"task{taskId}"

        span = win.createElement("span")
        span.onclick = "RemoveTask(this.parentNode.id)"
        span.innerHTML = '<i class="fa fa-trash">X</i>'

        task.appendChild(span)
        task.append(taskName)

        win.getElementById("tasks").appendChild(task)
        """

def RemoveTask(taskid):
    win.getElementById(taskid).remove()

win.display(file="render.html", pyfunctions=[CreateTask, RemoveTask])

win.show()
