from server import ma
from server.models import events, robots


class RobotSerializer(ma.ModelSchema):
    class Meta:
        model = robots.Robot


class EventSerializer(ma.ModelSchema):
    class Meta:
        model = events.LocationEvent
        fields = ('robot', 'x', 'y', 'timestamp')
