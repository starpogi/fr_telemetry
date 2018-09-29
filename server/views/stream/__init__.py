from flask import Blueprint, current_app
from flask_sockets import Sockets

blueprint = Blueprint('stream', __name__)

websocket = Sockets(current_app)


@blueprint.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

websocket.register_blueprint(blueprint, url_prefix=r'/stream')
