import webview
from bs4 import BeautifulSoup
from . import utils

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
</head>
<body>
<!-- <div id="cover" style="position: fixed; height: 100%; width: 100%; top:0; left: 0; background: #000; z-index:9999;"></div> -->

<script>
    function bridge(func) {
        pywebview.api.bridge(func)
        
    }


</script>
</body>
</html>
"""

global api_functions
api_functions = {}


class Api:
    def __init__(self):
        pass

    def bridge(self, func):
        if api_functions[func]:
            api_functions[func]()


def event(function):
    if not str(function) in api_functions:
        api_functions.update({str(function): function})
    return f"bridge('{str(function)}')"


# ELEMENTS #

def Button(window, id, content="", **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('button', id=id, attrs=args)
    elem.string = content
    elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return elem


def Input(window, id, content="", **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('input', id=id, attrs=args)
    elem.string = content
    elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return elem


def Header(window, id, content="", type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('h' + str(type), id=id, attrs=args)
    elem.string = content
    elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return elem


def Div(window, id, children=[], **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('div', id=id, attrs=args)
    elem.id = id
    for child in children:
        elem.append(child)

    soup.body.append(elem)
    window.setHtml(soup)
    return elem


class HTMlelement:
    def __init__(self, window, id):
        self.window = window
        self.id = id

    def getAttributes(self):
        return self.window.webview.get_elements(f'#{self.id}')[0]

    def value_get(self):
        return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").value;"""))

    def value_set(self, val):
        self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").value = "{val}";""")

    value = property(value_get, value_set)

    def innerHTML_get(self):
        return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").innerHTML;"""))

    def innerHTML_set(self, val):
        self.window.webview.evaluate_js(f"""document.getElementById("{self.id}").innerHTML = "{val}";""")

    innerHTML = property(innerHTML_get, innerHTML_set)


class Window:
    def __init__(self, title, css="def.css", min_size=(300, 300), size=(900, 600), fullscreen=False):
        api = Api()
        self.webview = webview.create_window(title, html=html, js_api=api, min_size=min_size, width=size[0],
                                             height=size[1], fullscreen=fullscreen)
        self.css = css
        self.running = False

    def load_handler(self, win):
        css_src = open(self.css, "r").read()
        win.load_css(css_src)

    def display(self, html):
        soup = BeautifulSoup(html, features="lxml")
        elem = soup.new_tag('script')
        elem.string = "function bridge(func) {pywebview.api.bridge(func)}"
        soup.body.append(elem)

        self.webview.html = str(soup)

    def setHtml(self, html):

        self.webview.html = str(html)

    def show(self):
        self.running = True
        webview.start(self.load_handler, self.webview)

    def appendChild(self, html):
        if self.running:
            self.webview.evaluate_js(f"""document.body.innerHTML += '{html}';""")
        else:
            raise Exception(""""Window.append" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elem = str(self.webview.evaluate_js(f""" '' + document.getElementById("{id}");"""))

            if elem != "null":
                return HTMlelement(self, id)
            else:
                return None

        else:
            raise Exception(""""Window.getElementById" can only be called while the window is running!""")
