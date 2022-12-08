import http.server
import socketserver

"""

HTTP server used for hosting a projects files.
Files used in HTML are only accessible when in an HTTPS server.

On window.show() Neutron adds '<base href="http://localhost:5600/">' to the projects HTML.
This way all local files in HTML will be redirected to their localhost equivalent.

This is because pywebview does not support local files when using self.html
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    pass


httpd = socketserver.TCPServer(("", 5600), Handler)
httpd.serve_forever()
