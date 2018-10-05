from flask import Blueprint, jsonify, request
from server import ma

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
    return jsonify(params)
