import webview
from bs4 import BeautifulSoup


html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

</head>
<body>


</body>
</html>
"""

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

</head>
<body>

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



class Window:
    def __init__(self, title, css="def.css"):
        api = Api()
        self.webview = webview.create_window(title, html=html, js_api=api)
        self.css = css

    def load_handler(self, win):
        css_src = open(self.css, "r").read()
        win.load_css(css_src)

    def show(self):
        webview.start(self.load_handler, self.webview)


