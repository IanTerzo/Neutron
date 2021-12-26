from bs4 import BeautifulSoup

"""

NOTE: HTMLelement class is located at the bottom of this file.

"""

def __CreateElement(window, tag, content, id, args):
    
    soup = BeautifulSoup(window.webview.html, features="lxml")

    if id:
        elem = soup.new_tag(tag, id=id, attrs=args)
    else:
        elem = soup.new_tag(tag, attrs=args)
    

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
    
    if id:
        elem = soup.new_tag(tag, id=id, attrs=args)
    else:
        elem = soup.new_tag(tag, attrs=args)

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



# Does not contain with global event handlers
HTMLelementAttributes = ['value', 'accept', 'action', 'align', 'allow', 'alt', 'autocapitalize', 'autocomplete', 'autofocus', 'autoplay', 'background', 'bgcolor', 'border', 'buffered', 'capture', 'challenge', 'charset', 'checked', 'cite', 'className', 'code', 'codebase', 'color', 'cols', 'colspan', 'content', 'contenteditable', 'contextmenu', 'controls', 'coords', 'crossorigin', 'csp ', 'data', 'datetime', 'decoding', 'default', 'defer', 'dir', 'dirname', 'disabled', 'download', 'draggable', 'enctype', 'enterkeyhint', 'for_', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'headers', 'height', 'hidden', 'high', 'href', 'hreflang', 'http_equiv', 'icon', 'importance', 'integrity', 'intrinsicsize ', 'inputmode', 'ismap', 'itemprop', 'keytype', 'kind', 'label', 'lang', 'language ', 'loading ', 'list', 'loop', 'low', 'manifest', 'max', 'maxlength', 'minlength', 'media', 'method', 'min', 'multiple', 'muted', 'name', 'novalidate', 'open', 'optimum', 'pattern', 'ping', 'placeholder', 'poster', 'preload', 'radiogroup', 'readonly', 'referrerpolicy', 'rel', 'required', 'reversed', 'rows', 'rowspan', 'sandbox', 'scope', 'scoped', 'selected', 'shape', 'size', 'sizes', 'slot', 'span', 'spellcheck', 'src', 'srcdoc', 'srclang', 'srcset', 'start', 'step', 'style', 'summary', 'tabindex', 'target', 'title', 'translate', 'type', 'usemap', 'width', 'wrap']

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
