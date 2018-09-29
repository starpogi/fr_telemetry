import os

from flask import Flask
from flask_sockets import Sockets
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['CONFIG'])
websocket = Sockets(app)
alembic = Alembic(app)
db = SQLAlchemy(app)


from server.models.events import LocationEvent


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
