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


