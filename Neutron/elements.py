from bs4 import BeautifulSoup
import uuid

"""

Neutron passes HTML elements beetween JavaScript and Python using a custom ID system "NeutronID".
The NeutronID is located in an elements classlist, and is generated when display() is first called.
Using this system Neutron can share HTML elements that do not have a regular HTML id,
for example HTML elements returned by getElementsByTagName().
Every NeutronID is an UUID.

"""

def createNeutronId(tag):
    NeutronID = f"NeutronID_{uuid.uuid1()}"

    element_classes = tag.get('class')
    if element_classes is not None:
        tag['class'] = NeutronID + " " + " ".join(element_classes)
    else:
         tag['class'] = NeutronID

    return NeutronID


# Web componets #

# TODO: Add event Attributes
HTMLelementAttributes = ['value', 'accept', 'action', 'align', 'allow', 'alt', 'autocapitalize', 'autocomplete',
                         'autofocus', 'autoplay', 'background', 'bgcolor', 'border', 'buffered', 'capture', 'challenge',
                         'charset', 'checked', 'cite', 'id', 'className', 'code', 'codebase', 'color', 'cols', 'colspan',
                         'content', 'contenteditable', 'contextmenu', 'controls', 'coords', 'crossorigin', 'csp ',
                         'data', 'datetime', 'decoding', 'default', 'defer', 'dir', 'dirname', 'disabled', 'download',
                         'draggable', 'enctype', 'enterkeyhint', 'for_', 'form', 'formaction', 'formenctype',
                         'formmethod', 'formnovalidate', 'formtarget', 'headers', 'height', 'hidden', 'high', 'href',
                         'hreflang', 'http_equiv', 'icon', 'importance', 'integrity', 'intrinsicsize ', 'inputmode',
                         'ismap', 'itemprop', 'keytype', 'kind', 'label', 'lang', 'language ', 'loading ', 'list',
                         'loop', 'low', 'manifest', 'max', 'maxlength', 'minlength', 'media', 'method', 'min',
                         'multiple', 'muted', 'name', 'novalidate', 'open', 'optimum', 'pattern', 'ping', 'placeholder',
                         'poster', 'preload', 'radiogroup', 'readonly', 'referrerpolicy', 'rel', 'required', 'reversed',
                         'rows', 'rowspan', 'sandbox', 'scope', 'scoped', 'selected', 'shape', 'size', 'sizes', 'slot',
                         'span', 'spellcheck', 'src', 'srcdoc', 'srclang', 'srcset', 'start', 'step', 'style',
                         'summary', 'tabindex', 'target', 'title', 'translate', 'type', 'usemap', 'width', 'wrap',
                         'onblur', 'onchange', 'oncontextmenu', 'onfocus', 'oninput', 'oninvalid', 'onreset', 'onsearch',
                         'onselect', 'onsubmit', 'onkeydown', 'onkeypress', 'onkeyup', 'onclick', 'ondblclick', 'onmousedown',
                         'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onwheel', 'ondrag', 'ondragend',
                         'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'onscroll', 'oncopy', 'oncut',
                         'onpaste', 'onabort', 'oncanplay', 'oncanplaythrough', 'oncuechange', 'ondurationchange', 'onemptied', 'onended',
                         'onerror', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onpause', 'onplay', 'onplaying', 'onprogress',
                         'onratechange', 'onseeked', 'onseeking', 'onstalled', 'onsuspend', 'ontimeupdate', 'onvolumechange',
                         'onwaiting', 'ontoggle',]


class HTMLelement:
    def __init__(self, window, NeutronID, elementHTML, domAttatched):
        self.window = window
        self.elementHTML = elementHTML # elementHTML is None if element is aquired while window is running
        self.NeutronID = NeutronID
        self.domAttatched = domAttatched;

        if "NeutronID_" not in self.NeutronID:
            raise ValueError("NeutronID is invalid")

    def __str__(self):
        # elementHTML will be set to None if class is called on runtime
        if self.window.running and self.domAttatched:
            return str(self.window.run_javascript(f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].outerHTML;"""))
        else:
            return str(self.elementHTML)


    def addEventListener(self, eventHandler, NeutronEvent):
        if self.window.running and self.domAttatched:
            self.window.run_javascript(
                f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].addEventListener("{eventHandler}", {NeutronEvent});""");
        else:
            eventHandler = "on" + eventHandler
            soup = BeautifulSoup(self.window.html, features="html.parser")
            # Create a new attribute for the event (i.e onclick)
            soup.find_all(class_=self.NeutronID)[0][eventHandler] = NeutronEvent

            self.window.html = str(soup)

    def appendChild(self, html_element):
        if self.window.running and self.domAttatched:
            soup = BeautifulSoup(str(html_element), features="html.parser")
            bodyContent = soup.find_all()

            for element in bodyContent:
                createNeutronId(element)

            self.window.run_javascript(f"""document.getElementsByClassName("{self.NeutronID}")[0].innerHTML += '{str(soup)}';""")
            return html_element
        else:
            self.elementHTML.append(BeautifulSoup(str(html_element), 'html.parser'))

    def append(self, html):
        if self.window.running and self.domAttatched:
            soup = BeautifulSoup(html, features="html.parser")
            bodyContent = soup.find_all()

            for element in bodyContent:
                createNeutronId(element)

            self.window.run_javascript(f"""document.getElementsByClassName("{self.NeutronID}")[0].innerHTML += '{str(soup)}';""")
        else:
            self.elementHTML.append(BeautifulSoup(html, 'html.parser'))

    # TODO
    def remove(self):
        if not self.window.running or not self.domAttatched:
             raise RuntimeError(""""remove" can only be called while the window is running and element is present on DOM!""")

        self.window.run_javascript(f"""document.getElementsByClassName("{self.NeutronID}")[0].remove();""")

     # Does not work with global event handlers!
    def getAttribute(self, attribute):
        if self.window.running and self.domAttatched:
            return str(self.window.run_javascript(f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].{attribute};"""))
        else:
            return self.elementHTML.attrs

    # Does not work with global event handlers!
    def setAttribute(self, attribute, value):
        if self.window.running and self.domAttatched:
            self.window.run_javascript(
                f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].setAttribute("{attribute}", "{value}");""")
        else:
            self.elementHTML[attribute] = value

    def removeAttribute(self, attribute):
        if self.window.running and self.domAttatched:
            self.window.run_javascript(
                f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].removeAttribute("{attribute}");"""
            )
        else:
            del self.elementHTML[attribute]


    def innerHTML_get(self):
        if self.window.running and self.domAttatched:
            return str(self.window.run_javascript(f""" '' + document.getElementsByClassName("{self.NeutronID}")[0].innerHTML;"""))
        else:
            return self.elementHTML.decode_contents()

    def innerHTML_set(self, value):
        if self.window.running and self.domAttatched:
            self.window.run_javascript(f"""document.getElementsByClassName("{self.NeutronID}")[0].innerHTML = "{value}";""")
        else:
            self.elementHTML.clear()
            self.elementHTML.append(BeautifulSoup(value, 'html.parser'))

    innerHTML = property(innerHTML_get, innerHTML_set)

    for attribute in HTMLelementAttributes:
        exec(
            f"{attribute} = property(lambda self: self.getAttribute('{attribute}'), lambda self, val: self.setAttribute('{attribute}', val))")
