from flask import Blueprint, jsonify, request

from server import ma
from server.controllers import location


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route("/robots", methods=('GET',))
def get_robots():
    params = request.args
    return jsonify(params)


@blueprint.route("/robots/<string:robot>", methods=('GET',))
def get_robot(robot=None):
    params = request.args
    return jsonify(params)


@blueprint.route("/robots/<string:robot>/odometer", methods=('GET',))
def get_odometer(robot=None):
    params = request.args

    odometer = location.get_odometer(
        robots=robot,
        start_time=params.get('start_time'),
        end_time=params.get('end_time')
    )

    return jsonify(odometer)
