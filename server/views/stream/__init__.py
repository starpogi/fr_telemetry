from flask import Blueprint, current_app

from server import ws
from server.tasks import process

blueprint = Blueprint('stream', __name__)


@blueprint.route('/upstream')
def upstream_data(socket):
    while not socket.closed:
        message = socket.receive()
        process.push_event(message, socket)


ws.register_blueprint(blueprint, url_prefix=r'/')
