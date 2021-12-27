import webview
from bs4 import BeautifulSoup

import inspect
import logging 

import sys
import os

if not sys.platform.startswith('linux'):
    import keyboard

from Neutron import elements
from Neutron import utils



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

global api_functions
api_functions = {}


# PYTHON - JAVASCRIPT BRIDGE #

class Api:
    def __init__(self):
        pass

    def bridge(self, func):
        if api_functions[func]:
            api_functions[func]()

def event(function):
    if callable(function):
        if not str(function) in api_functions:
            api_functions.update({str(function): function})
        return f"bridge('{str(function)}')"
    else:
        raise EventException("Event attribute is not a function!")

# EXCEPTIONS #

class EventException(Exception):
    pass

class WindowException(Exception):
    pass
  

class Window:
    def __init__(self, title, css="def.css", min_size=(300, 300), size=(900, 600), fullscreen=False):
        api = Api()
        self.webview = webview.create_window(title, html=html, js_api=api, min_size=min_size, width=size[0],
                                             height=size[1], fullscreen=fullscreen)
        self.css = css
        self.running = False

        # Cover attributes
        self.covertime = 3000
        self.covercolor = '#fff'
        self.covercontent = "<h1>Loading...</h1>"
        self.after_load = None

        self.resize = self.webview.resize
        self.toggle_fullscreen = self.webview.toggle_fullscreen

    def load_handler(self, win):
        if self.showafter:
            self.showafter()

    def loader(self, content="<h1 style='None'>Loading...</h1>", color='#fff', duration=3000, after=None):
        self.webview.background_color = color
        self.covercolor = color
        self.covertime = duration

        self.covercontent = content

        if after:
            self.after_load = event(after)

    def display(self, html=None, file=None):
        frame = inspect.currentframe()
        locals = frame.f_back.f_locals

        if file:
            # Convert file content to f-string
            
            # Check if program is being run as an exe
            if getattr(sys, 'frozen', False):
                content = str(open(os.path.join(sys._MEIPASS, file), "r").read())
            else:
                content = str(open(file, "r").read())

            oneLine = content.replace("\n", "")
            try:
                soupSrc = eval(f"f'{oneLine}'", locals)
            except Exception as e:
                raise WindowException("Error while parsing python code inside -> { }. Error: " + str(e))

        elif html:
            soupSrc = html
        
        self.webview.html = soupSrc

    def setHtml(self, html):
        self.webview.html = str(html)

    def hide(self):
        self.webview.hide()

    def show(self, after=None):
        self.showafter = after

        if self.running != True:
            if not sys.platform.startswith('linux'):
                keyboard.block_key("f5")
            
            soup = BeautifulSoup(self.webview.html, features="lxml")
            bridge = soup.new_tag('script')
            if self.after_load:
                bridge.string = "function bridge(func) {pywebview.api.bridge(func)} setTimeout(function() {document.getElementById('cover').style.display = 'none';" +self.after_load+"}," + str(self.covertime) +")"
            else:
                bridge.string = "function bridge(func) {pywebview.api.bridge(func)} setTimeout(function() {document.getElementById('cover').style.display = 'none'}," + str(self.covertime) +")"
            
            soup.body.append(bridge)

            cover = soup.new_tag('div', id="cover", attrs={'style':'position: fixed; height: 100%; width: 100%; top:0; left: 0; background: ' +self.covercolor+ '; z-index:9999;'})

            coverContent = BeautifulSoup(str(self.covercontent), features="lxml")
            cover.append(coverContent)
            soup.body.append(cover)
            style = soup.new_tag('style')

            # Check if program is being run as an exe
            if getattr(sys, 'frozen', False):
                style.string = open(os.path.join(sys._MEIPASS, self.css), "r").read()
            else:
                style.string = open(self.css, "r").read()

            
            soup.body.append(style)

            self.webview.html = str(soup)

            self.running = True
            webview.start(self.load_handler, self.webview)
        else:
            self.webview.show()

    def appendChild(self, html):
        if self.running:
            self.webview.evaluate_js(f"""document.body.innerHTML += '{html}';""")
            return html
        else:
            raise WindowException(""""Window.append" can only be called while the window is running!""")
            
    def append(self, html):
        if self.running:
            self.webview.evaluate_js(f"""document.body.innerHTML += '{html}';""")
        else:
            raise WindowException(""""Window.append" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elem = str(self.webview.evaluate_js(f""" '' + document.getElementById("{id}");"""))

            if elem != "null":
                return elements.HTMlelement(self, id)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None

        else:
            soup = BeautifulSoup(self.webview.html, features="lxml")
            # check if element exists
            if soup.select(f'#{id}') != []:
                return elements.HTMlelement(self, id)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None
 
