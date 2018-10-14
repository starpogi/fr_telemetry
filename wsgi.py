from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from server import create_app


app = create_app()

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8000),
                               app,
                               handler_class=WebSocketHandler)
    server.serve_forever()
