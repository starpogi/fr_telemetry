from flask import Blueprint, jsonify, request
from server import ma

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route("/robots/<string:robot>/odometer", methods=('GET',))
def get_odometer(robot=None):
    params = request.args
    return jsonify(params)
