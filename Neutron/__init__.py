from logging import error, exception
from re import A
import webview
from bs4 import BeautifulSoup
from webview import window
from . import utils
import inspect
import sys
import logging
import keyboard

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

def __CreateElement(window, tag, content, id, args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag(tag, attrs=args)
    if id:
        elem.id = id

    if type(content) == HTMlelement:
        soup = BeautifulSoup(str(soup).replace(str(content), "", 1), features="lxml")
        contentParsed = BeautifulSoup(str(content), 'html.parser')
        elem.append(contentParsed)
    else:
        elem.string = str(content)
    
    soup.body.append(elem)

    # Remove old element

    window.setHtml(soup)
    return HTMlelement(window, id, elem)

# For HTML elements ment for containing other elements i.e div
def __CreateContainer(window, tag, children, id, args):
    soup = BeautifulSoup(window.webview.html, features="lxml")

    # Remove children from body
    for child in children:
        soup = str(soup)[::-1].replace(str(child)[::-1], "", 1)[::-1]

    soup = BeautifulSoup(soup, features="lxml")
    elem = soup.new_tag(tag, id=id, attrs=args)
    elem.id = id
    for child in children:
        # Make children into tags
        childParsed = BeautifulSoup(str(child), 'html.parser')
        elem.append(childParsed)
    
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)

# Content sectioning #

def Adress(window, children=[], id=None, **args):
   return __CreateContainer(window, "adress", children, id, args)

def Article(window, children=[], id=None, **args):
    return __CreateContainer(window, "article", children, id, args)


def Aside(window, children=[], id=None, **args):
    return __CreateContainer(window, "aside", children, id, args)

def Footer(window, children=[], id=None, **args):
    return __CreateContainer(window, "footer", children, id, args)

def Header(window, content="", id=None, **args):
    return __CreateElement(window, "header", content, id, args)

def H(window, content="", id=None, type=1, **args):
    return __CreateElement(window, "h" + str(type), content, id, args)

def H1(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=1, **args)

def H2(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=2, **args)   

def H3(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=3, **args)  

def H4(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=4, **args)  

def H5(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=5, **args)  

def H6(window, content="", id=None, **args):
    return H(window=window, content=content, id=id, type=6, **args)    
    
def Main(window, children=[], id=None, **args):
    return __CreateContainer(window, "main", children, id, args)

def Nav(window, children=[], id=None, **args):
    return __CreateContainer(window, "nav", children, id, args)
    
def Section(window, children=[], id=None, **args):
    return __CreateContainer(window, "section", children, id, args)

# Text content #

def Blockquote(window, content="", id=None, **args):
    return __CreateElement(window, "blockquote", content, id, args)

def Dd(window, content="", id=None, **args):
    return __CreateElement(window, "dd", content, id, args)

def Div(window, id=None, children=[], **args):
    return __CreateContainer(window, "div", children, id, args)

def Dl(window, content="", id=None, **args):
    return __CreateElement(window, "dl", content, id, args)

def Dt(window, content="", id=None, **args):
    return __CreateElement(window, "dt", content, id, args)

def Figcaption(window, content="", id=None, **args):
    return __CreateElement(window, "figcaption", content, id, args)

def Figure(window, id=None, children=[], **args):
    return __CreateContainer(window, "Figure", children, id, args)

def Hr(window, content="", id=None, **args):
    return __CreateElement(window, "Hr", content, id, args)

def Li(window, content="", id=None, **args):
    return __CreateElement(window, "li", content, id, args)

def Ol(window, id=None, children=[], **args):
    return __CreateContainer(window, "ol", children, id, args)

def P(window, content="", id=None, **args):
    return __CreateElement(window, "p", content, id, args)

def P(window, content="", id=None, **args):
    return __CreateElement(window, "p", content, id, args)

def Pre(window, content="", id=None, **args):
    return __CreateElement(window, "pre", content, id, args)

def Ul(window, id=None, children=[], **args):
    return __CreateContainer(window, "Ul", children, id, args)

# Image and multimedia #

def Area(window, content="", id=None, **args):
    return __CreateElement(window, "area", content, id, args)

def Audio(window, content="", id=None, **args):
    return __CreateElement(window, "audio", content, id, args)

def Img(window, content="", id=None, **args):
    return __CreateElement(window, "img", content, id, args)

def Map(window, id=None, children=[], **args):
    return __CreateContainer(window, "Map", children, id, args)

def Track(window, content="", id=None, **args):
    return __CreateElement(window, "track", content, id, args)

def Video(window, content="", id=None, **args):
    return __CreateElement(window, "video", content, id, args)

# Embedded content #

def Embed(window, content="", id=None, **args):
    return __CreateElement(window, "embed", content, id, args)

def Iframe(window, content="", id=None, **args):
    return __CreateElement(window, "iframe", content, id, args)

def Object(window, content="", id=None, **args):
    return __CreateElement(window, "object", content, id, args)

def Param(window, content="", id=None, **args):
    return __CreateElement(window, "param", content, id, args)

def Picture(window, id=None, children=[], **args):
    return __CreateContainer(window, "picture", children, id, args)

def Portal(window, content="", id=None, **args):
    return __CreateElement(window, "portal", content, id, args)

def Source(window, content="", id=None, **args):
    return __CreateElement(window, "source", content, id, args)

# SVG and MathML #

def Svg(window, content="", id=None, **args):
    return __CreateElement(window, "svg", content, id, args)

def Math(window, content="", id=None, **args):
    return __CreateElement(window, "math", content, id, args)

# Table content #

def Caption(window, content="", id=None, **args):
    return __CreateElement(window, "caption", content, id, args)

def Col(window, content="", id=None, **args):
    return __CreateElement(window, "col", content, id, args)

def Colgroup(window, content="", id=None, **args):
    return __CreateElement(window, "colgroup", content, id, args)

def Table(window, id=None, children=[], **args):
    return __CreateContainer(window, "table", children, id, args)

def Tbody(window, id=None, children=[], **args):
    return __CreateContainer(window, "tbody", children, id, args)

def Td(window, content="", id=None, **args):
    return __CreateElement(window, "td", content, id, args)

def Tfoot(window, id=None, children=[], **args):
    return __CreateContainer(window, "tfoot", children, id, args)

def Th(window, content="", id=None, **args):
    return __CreateElement(window, "th", content, id, args)

def Thead(window, id=None, children=[], **args):
    return __CreateContainer(window, "thead", children, id, args)

def Tr(window, id=None, children=[], **args):
    return __CreateContainer(window, "tr", children, id, args)

# Forms #

def Button(window, content="", id=None, **args):
    return __CreateElement(window, "button", content, id, args)

def Datalist(window, id=None, children=[], **args):
    return __CreateContainer(window, "datalist", children, id, args)

def Fieldset(window, id=None, children=[], **args):
    return __CreateContainer(window, "fieldset", children, id, args)

def Form(window, id=None, children=[], **args):
    return __CreateContainer(window, "form", children, id, args)

def Input(window, content="", id=None, **args):
    return __CreateElement(window, "input", content, id, args)

def Label(window, content="", id=None, **args):
    return __CreateElement(window, "label", content, id, args)

def Legend(window, content="", id=None, **args):
    return __CreateElement(window, "legend", content, id, args)

def Meter(window, content="", id=None, **args):
    return __CreateElement(window, "meter", content, id, args)

def Optgroup(window, id=None, children=[], **args):
    return __CreateContainer(window, "optgroup", children, id, args)

def Option(window, content="", id=None, **args):
    return __CreateElement(window, "option", content, id, args)

def Output(window, id=None, children=[], **args):
    return __CreateContainer(window, "output", children, id, args)

def Progress(window, content="", id=None, **args):
    return __CreateElement(window, "progress", content, id, args)

def Select(window, id=None, children=[], **args):
    return __CreateContainer(window, "select", children, id, args)

def Textarea(window, content="", id=None, **args):
    return __CreateElement(window, "textarea", content, id, args)

# Interactive elements #

def Details(window, id=None, children=[], **args):
    return __CreateContainer(window, "details", children, id, args)

def Dialog(window, content="", id=None, **args):
    return __CreateElement(window, "dialog", content, id, args)

def Menu(window, id=None, children=[], **args):
    return __CreateContainer(window, "menu", children, id, args)

def Summary(window, content="", id=None, **args):
    return __CreateElement(window, "summary", content, id, args)

# Web componets #
     #soon


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

    def appendChild(self, html):
        self.window.webview.evaluate_js(f"""document.getElementById("{self.id}").innerHTML += '{html}';""")
        return html
    
    def append(self, html):
        self.window.webview.evaluate_js(f"""document.getElementById("{self.id}").innerHTML += '{html}';""")
        
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
        self.covertime = 3000
        self.covercolor = '#fff'
        self.covercontent = "<h1 style='None'>Loading...</h1>"
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
