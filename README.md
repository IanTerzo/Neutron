![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Neutron is ment to be an intuative way of creating GUI applications using HTML, CSS and Python. It is built on top of PyQt6 and uses the QtWebEngine.

You can get started contributing via [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md).

## Installation

```
pip install neutron-web
```

## Example
For a template project see [TEMPLATE](https://github.com/IanTerzo/Neutron/tree/main/TEMPLATE) or see the [to-do app](https://github.com/IanTerzo/Neutron/tree/main/examples/todo-app).

## Usage
The Neutron api is designed to be very similar to the JavaScript DOM api. You can imagine the `Window` class as the `document` object in JavaScript (altough it is still missing a lot of features). Ideally you should be able to use Neutron as you would use the JavaScript DOM api, altough there are some differences.

### Neutron features

```python
Neutron.event(function : Callable)) -> str
```
Use this function when passing a python function to an event listener or javascript method that requires a callable as parameter. Return the new javascript "bridge" function as str.

```python
Window(title: str, css: str, position: Tuple[int, int], size: Tuple[int, int]) -> Window
```
Create a window.

```python
Window.run_javascript(javascript: str) -> str
```
Evaluate JavaScript code.

```python
Window.display(file: str, html: str, pyfunctions: List[Callable], encoding: str) -> None
```
Used to parse your html code. You run it before showing the window. It takes a path to your htlm file or html code (if file is not provided), a list of python functions and an encoding. The encoding is the encoding of your html file. The python functions are the functions you want to able to directly call from your html file. See the to-do app example.

```python
Window.show() -> None / Window.close() -> None
```
Show and close the window.


## Building your project

To build a Neutron project you first need pyinstaller, install pyinstaller through pip: `pip install pyinstaller`. Then run the script below in your command prompt/terminal. You can also use other programs to build your project such as py2exe if you prefer.

> **Note:** If you are on linux use ":" instead of ";"
```
pyinstaller YOUR_PYTHON_FILE.py --noconsole --onefile --add-data="YOUR_HTML_FILE.html;." --add-data="YOUR_CSS_FILE.css;."
```

You don't need to use `--add-data` if your project doesn't have a CSS or HTML file
