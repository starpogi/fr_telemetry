from server import db
from datetime import datetime


class LocationEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    robot = db.Column(db.String(150), index=True, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Integer, index=True, default=datetime.utcnow,
                          nullable=False)

    def __repr__(self):
        return '<Location Event %r (%r, %r)>' % (self.robot, self.x, self.y)
