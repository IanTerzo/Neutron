from logging import error, exception
from re import A
import webview
from bs4 import BeautifulSoup
from webview import window
from . import utils
import inspect
import sys
import logging

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

# Does not contain with global event handlers
HTMLelementAttributes = ['value', 'accept', 'action', 'align', 'allow', 'alt', 'autocapitalize', 'autocomplete', 'autofocus', 'autoplay', 'background', 'bgcolor', 'border', 'buffered', 'capture', 'challenge', 'charset', 'checked', 'cite', 'className', 'code', 'codebase', 'color', 'cols', 'colspan', 'content', 'contenteditable', 'contextmenu', 'controls', 'coords', 'crossorigin', 'csp ', 'data', 'datetime', 'decoding', 'default', 'defer', 'dir', 'dirname', 'disabled', 'download', 'draggable', 'enctype', 'enterkeyhint', 'for_', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'headers', 'height', 'hidden', 'high', 'href', 'hreflang', 'http_equiv', 'icon', 'importance', 'integrity', 'intrinsicsize ', 'inputmode', 'ismap', 'itemprop', 'keytype', 'kind', 'label', 'lang', 'language ', 'loading ', 'list', 'loop', 'low', 'manifest', 'max', 'maxlength', 'minlength', 'media', 'method', 'min', 'multiple', 'muted', 'name', 'novalidate', 'open', 'optimum', 'pattern', 'ping', 'placeholder', 'poster', 'preload', 'radiogroup', 'readonly', 'referrerpolicy', 'rel', 'required', 'reversed', 'rows', 'rowspan', 'sandbox', 'scope', 'scoped', 'selected', 'shape', 'size', 'sizes', 'slot', 'span', 'spellcheck', 'src', 'srcdoc', 'srclang', 'srcset', 'start', 'step', 'style', 'summary', 'tabindex', 'target', 'title', 'translate', 'type', 'usemap', 'width', 'wrap']

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

# ELEMENTS #

def Button(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('button', id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Input(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('input', id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Header(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('h' + str(type), id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Paragraph(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('p' + str(type), id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Div(window, id=None, children=[], **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")

    # Remove children from body
    for child in children:
        soup = str(soup).replace(str(child), "")

    soup = BeautifulSoup(soup, features="lxml")
    elem = soup.new_tag('div', id=id, attrs=args)
    elem.id = id
    for child in children:
        elem.append(child)

    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


class HTMlelement:
    def __init__(self, window, id, elementHTML=None):
        self.window = window
        self.elementHTML = elementHTML
        self.id = id

    def __str__(self):
        # elementHTML will be set to None if class is called on runtime
        if self.elementHTML is not None:
            return str(self.elementHTML)
        else:
            return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").outerHTML;"""))
    
    def AddEventListener(self, eventHandler, NeutronEvent):
        if not self.window.running:
                eventHandler = "on" + eventHandler
                soup = BeautifulSoup(self.window.webview.html, features="lxml")
                # Create a new attribute for the event (i.e onclick)
                soup.find(id=self.id)[eventHandler] = NeutronEvent
                
                self.window.webview.html = str(soup)
        else:
            self.window.webview.evaluate_js(
            f""" '' + document.getElementById("{self.id}").addEventListener("{eventHandler}", {NeutronEvent});""");


    # Does not work with global event handlers!!
    def getAttributes(self):
        if self.window.running:
            return self.window.webview.get_elements(f'#{self.id}')[0]
        else:
            return self.elementHTML.attrs
    
    # Does not work with global event handlers!!
    def setAttribute(self, attribute, value):
        self.window.webview.evaluate_js(
            f""" '' + document.getElementById("{self.id}").setAttribute("{attribute}", "{value}");""")

    def innerHTML_get(self):
        return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").innerHTML;"""))

    def innerHTML_set(self, val):
        self.window.webview.evaluate_js(f"""document.getElementById("{self.id}").innerHTML = "{val}";""")
    
    innerHTML = property(innerHTML_get, innerHTML_set)

    for attribute in HTMLelementAttributes:
        exec(f"{attribute} = property(lambda self: self.getAttributes()['{attribute}'], lambda self, val: self.setAttribute('{attribute}', val))")
    

    

class Window:
    def __init__(self, title, css="def.css", min_size=(300, 300), size=(900, 600), fullscreen=False):
        api = Api()
        self.webview = webview.create_window(title, html=html, js_api=api, min_size=min_size, width=size[0],
                                             height=size[1], fullscreen=fullscreen)
        self.css = css
        self.running = False

        # Cover attributes
        self.covertime = 2000
        self.covercolor = '#fff'
        self.covercontent = ""
        self.after_load = None

        self.resize = self.webview.resize
        self.toggle_fullscreen = self.webview.toggle_fullscreen

    def load_handler(self, win):
        if self.showafter:
            self.showafter()

    def loader(self, source=None, color='#fff', duration=2000, after=None):
        self.webview.background_color = color
        self.covercolor = color
        self.covertime = duration

        if source:
            self.covercontent = source

        if after:
            self.after_load = event(after)

    def display(self, html=None, file=None):
        frame = inspect.currentframe()
        locals = frame.f_back.f_locals

        if file:
            # Convert file content to f-string
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

    def show(self, after=None):
        self.showafter = after

        soup = BeautifulSoup(self.webview.html, features="lxml")

        bridge = soup.new_tag('script')
        if self.after_load:
            bridge.string = "function bridge(func) {pywebview.api.bridge(func)} setTimeout(function() {document.getElementById('cover').style.display = 'none';" +self.after_load+"}," + str(self.covertime) +")"
        else:
            bridge.string = "function bridge(func) {pywebview.api.bridge(func)} setTimeout(function() {document.getElementById('cover').style.display = 'none'}," + str(self.covertime) +")"
        soup.body.append(bridge)

        cover = soup.new_tag('div', id="cover", attrs={'style':'position: fixed; height: 100%; width: 100%; top:0; left: 0; background: ' +self.covercolor+ '; z-index:9999;'})
        coverContent = BeautifulSoup(self.covercontent, features="lxml")
        cover.append(coverContent)
        soup.body.append(cover)
        
        style = soup.new_tag('style')
        style.string = open(self.css, "r").read()
        soup.body.append(style)

        self.webview.html = str(soup)


        self.running = True
        webview.start(self.load_handler, self.webview)

    def appendChild(self, html):
        if self.running:
            self.webview.evaluate_js(f"""document.body.innerHTML += '{html}';""")
        else:
            raise WindowException(""""Window.append" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elem = str(self.webview.evaluate_js(f""" '' + document.getElementById("{id}");"""))

            if elem != "null":
                return HTMlelement(self, id)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None

        else:
            soup = BeautifulSoup(self.webview.html, features="lxml")
            # check if element exists
            if soup.select(f'#{id}') != []:
                return HTMlelement(self, id)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None
