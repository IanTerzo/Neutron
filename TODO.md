
# Neutron to-dos list

### HTML
- [ ] Finish all HTML elements

In Neutron are HTML elements made like this:
```
def Button(window, id, content="", **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('button', id=id, attrs=args)
    elem.string = content
    elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return elem
```
To create a new Element simply edit the functions name and the tag in `soup.new_tag()`.


- [ ] Finish all DOM methods

Right now there's only getElementById() (It is located inside the window class) and it would be ideal to add all the other DOM methods. All DOM methods should be inside the window class.
- [ ] Iframe to window communication

Ideally it would be possible communicate between the Iframe and the main window.
### OTHER
- [ ] In-python css 

Creating a system to write CSS in the python code
- [ ] Finish the HTMLelement class

The `HTMLelement` class is supposed to contain all of the original HTMLelement attributes, right now it only contains value and innerHTML. Example:

    def value_get(self):
        return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").value;"""))

    def value_set(self, val):
        self.setAttribute("value", val)

    value = property(value_get, value_set)
- [ ] Wait for all elements to load before display

This is still a blank spot, an idea is to put a `cover`  div on top of the screen and then hide it when all the elements and CSS are fully loaded.

    <div id="cover" style="position: fixed; height: 100%; width: 100%; top:0; left: 0; background: #000; z-index:9999;"></div>

- [ ] System to make loading animation

A system to let the user create his own loading animation with CSS.

### COMPLETED TO-DOS
- [x] JavaScript-Python bridge


