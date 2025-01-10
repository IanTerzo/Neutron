
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QThread
from bs4 import BeautifulSoup
import json
from . import elements
import sys
import os
import logging
import asyncio
import threading
import websockets
from websockets.exceptions import ConnectionClosedOK
from http.server import SimpleHTTPRequestHandler, HTTPServer

global api_functions
api_functions = {}

class ListenerHTTPServer(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable log messages
        pass

    def _set_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        data = json.loads(post_data)

        if data["type"] == "bridge":
            api_functions[data['function']](*data['parameters'])
            self.send_response(200)
            self._set_headers()
            self.end_headers()
        else:
            self.send_response(500)
            self._set_headers()
            self.end_headers()


def start_listener_server(port):
    httpd = HTTPServer(('', port), ListenerHTTPServer)
    httpd.serve_forever()

class WebSocketSendServer(QThread):
    client = None

    def __init__(self, port):
        super().__init__()
        self.pending_response = None
        self.port = port

    async def handler(self, websocket):
        self.client = websocket

        try:
            while True:
                try:
                    message = await websocket.recv()
                    if self.pending_response:
                        self.pending_response.set_result(message)

                except ConnectionClosedOK:
                    print(f"Client {websocket} disconnected gracefully.")
                    break
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connection closed unexpectedly: {e}")
                    break
        finally:
            self.client = None

    async def start_server(self):
        async with websockets.serve(self.handler, "localhost", self.port):  # Optional max size for messages
            await asyncio.Future()  # Run forever

    async def send_and_wait(self, message: str) -> str:
        if not self.client:
            raise RuntimeError("No client connected")

        # Create a future to await the response
        self.pending_response = asyncio.get_event_loop().create_future()

        await self.client.send(message)

        # Wait for the future to be done
        while True:
            if self.pending_response.done():
                result = self.pending_response.result()
                self.pending_response = None
                return result


    def run(self):
        asyncio.run(self.start_server())

def event(function):
    if callable(function):
        if not str(function) in api_functions:
            api_functions.update({str(function): function})
        return f"bridge('{str(function)}')"
    else:
        raise TypeError("Event attribute is not a function!")

class Window:
    def __init__(self, title, css=None, position=(300, 300), size=(900, 600), listener_port=22943, sender_port=22944):
        self.title = title
        self.css = css
        self.position = position
        self.size = size
        self.running = False

        self.listener_port = listener_port
        self.sender_port = sender_port

        self.view = None
        self.qt_window = None;
        self.html = ""
        self.loop = asyncio.new_event_loop()


    def run_javascript(self, javascript):
        if not self.running:
             raise RuntimeError(""""Window.run_javascript()" can only be called while the window is running!""")

        message = json.dumps({"type": "eval", "javascript": javascript})
        response = ""
        async def send_and_wait():
            nonlocal response
            try:
                response = await self.websocket_server.send_and_wait(message)
            except TimeoutError:
                raise TimeoutError("No response received within the timeout period.")

        asyncio.run(send_and_wait())
        return response

    def display(self, file=None, html=None, pyfunctions=None, encoding="utf-8"):

        if file:
            # Check if program is being run as an exe
            if getattr(sys, 'frozen', False):
                content = str(open(os.path.join(sys._MEIPASS, file), "r", encoding=encoding).read())
            else:
                content = str(open(file, "r", encoding=encoding).read())
        elif html:
            content = str(html) # Make sure it is a string (could be beutifulsoup element)

        soup = BeautifulSoup(content, "html.parser")

        bridge_html = """
        <script>
        const commandSocket = new WebSocket("ws://localhost:""" + str(self.sender_port) + """");

        commandSocket.onopen = function() {
            console.log("WebSocket connection opened");
            commandSocket.send("connect");
        };

        commandSocket.onmessage = function(event) {
            data = JSON.parse(event.data);
            if (data.type == "eval") {
                result = eval(data.javascript);
                commandSocket.send(result);
            }
        };

        commandSocket.onclose = function() {
            console.log("WebSocket connection closed");
        };

        commandSocket.onerror = function(error) {
            console.log("WebSocket error: " + error.message);
        };

        function bridge(func, ...params) {
            const url = 'http://localhost:""" + str(self.listener_port) + """';
            const data = {
                type: 'bridge',
                function: func,
                parameters: params
            };

            fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        };
        """


        # add registered python function
        if pyfunctions:
            for function in pyfunctions:
                api_functions.update({str(function): function})
                bridge_html += "function " + function.__name__ +  "(...params){bridge('" + str(function) + "',...params)}; "

        bridge_html += "</script>"

        # add stylesheet if needed
        if self.css:
            bridge_html += f'<link rel="stylesheet" href="http://localhost:{self.listener_port}/{self.css}">'


        # Append the new HTML to the <head> section

        if not soup.head:
            head = soup.new_tag('head')
            soup.insert(0, head)

        soup.head.append(BeautifulSoup(bridge_html, 'html.parser'))

        soupContent = soup.find_all()

        for element in soupContent:
            elements.createNeutronId(element)

        # Link all filereads to the http server
        base = soup.new_tag('base')
        base['href'] = f"http://localhost:{self.listener_port}/"

        self.html = str(soup)


    def show(self, after=None):
        title = self.title
        size = self.size

        # Start bridge server
        server_thread = threading.Thread(target=start_listener_server, args=(self.listener_port,))
        server_thread.daemon = True  # Ensures the thread will exit when the main program exits
        server_thread.start()

        # Start websocket server
        self.websocket_server = WebSocketSendServer(self.sender_port)
        self.websocket_server.start()

        # Create window
        app = QApplication(sys.argv)

        window = QMainWindow()
        window.setWindowTitle(title)
        window.setGeometry(100, 100, size[0], size[1])

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        window.setCentralWidget(central_widget)

        view = QWebEngineView()
        view.setHtml( self.html, QUrl("qrc:///"))

        layout.addWidget(view)

        self.view = view
        self.qt_window = window;

        self.running = True
        self.qt_window.show()
        sys.exit(app.exec())


    def close(self):
        self.qt_window.close()

    def appendChild(self, html_element):
        if self.running:
            self.run_javascript(f"""document.body.innerHTML += '{str(html_element)}';""")
            html_element.domAttatched = True;
            return html_element
        else:
            raise RuntimeError(""""Window.appendChild()" can only be called while the window is running!""")

    def append(self, html):
        if self.running:
            self.run_javascript(f"""document.body.innerHTML += '{str(html)}';""")
        else:
            raise RuntimeError(""""Window.append()" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elementNeutronID = str(self.run_javascript(f""" '' + document.getElementById("{id}").className;"""))

            NeutronID = None

            for classname in elementNeutronID.split(' '):
                if "NeutronID_" in classname:
                    NeutronID = classname
                    break

            if NeutronID:
                return elements.HTMLelement(self, NeutronID, None, True)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None
        else:
            soup = BeautifulSoup(self.html, "html.parser")
            # check if element exists
            element = soup.select(f'#{id}')
            if element != []:
                NeutronID = element[0].get('class')[0]
                return elements.HTMLelement(self, NeutronID, element, True)
            else:
                logging.warning(f'HTMLelement with id "{id}" was not found!')
                return None

    def getElementsByTagName(self, name):
        if self.running:
            ElementsNeutronID = self.run_javascript("var elementsNeutronID = []; Array.from(document.getElementsByTagName('" + name + "')).forEach(function(item) { elementsNeutronID.push(item.className) }); '' + elementsNeutronID;")
            return [elements.HTMLelement(self, NeutronID.split(' ')[0], None, True) for NeutronID in ElementsNeutronID.split(",")]
        else:
            soup = BeautifulSoup(self.html, "html.parser")
            return [elements.HTMLelement(self, element.get('class')[0], element, True) for element in soup.find_all(name)]

    def createElement(self, tag):
        soup = BeautifulSoup(self.html, features="html.parser")
        elem = soup.new_tag(tag)

        NeutronID = elements.createNeutronId(elem)

        soup.append(elem)

        return elements.HTMLelement(self, NeutronID, elem, False)
