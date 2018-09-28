from flask import Flask
from flask_sockets import Sockets
from flask_alembic import Alembic


app = Flask(__name__)
websocket = Sockets(app)
alembic = Alembic(app)


@websocket.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def index():
    return "Hi"


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000),
                               app,
                               handler_class=WebSocketHandler)
    server.serve_forever()
