from flask import Blueprint, jsonify, request, abort

from server.views.api.serializers import RobotSerializer, EventSerializer
from server.controllers import events, robots


blueprint = Blueprint('api', __name__, url_prefix='/api')
robots_serializer = RobotSerializer(many=True)
robot_serializer = RobotSerializer()
event_serializer = EventSerializer(many=True)


@blueprint.route("/robots", methods=('GET',))
def get_robots():
    result = robots.get_robots()
    return jsonify(robots_serializer.dump(result).data)


@blueprint.route("/robots/<string:robot>", methods=('GET',))
def get_robot(robot):
    result = robots.get_robots(name=robot)

    if result is None:
        abort(404)

    return jsonify(robot_serializer.dump(result).data)


@blueprint.route("/robots/<string:robot>/events", methods=('GET',))
def get_robot_events(robot):
    params = request.args

    result = events.get_events(
        robots=robot,
        start_time=params.get('start_time'),
        end_time=params.get('end_time')
    )

    return jsonify(event_serializer.dump(result.all()).data)


@blueprint.route("/robots/<string:robot>/odometer", methods=('GET',))
def get_odometer(robot):
    params = request.args

    odometer = events.get_odometer(
        robot_name=robot,
        start_time=params.get('start_time'),
        end_time=params.get('end_time')
    )

    return jsonify({'robot': robot, 'odometer': odometer})
