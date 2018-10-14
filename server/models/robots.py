from datetime import datetime

from server import db


class Robot(db.Model):
    name = db.Column(db.String(150), primary_key=True)
    odometer = db.Column(db.Float, default=0, nullable=False)
    last_x = db.Column(db.Float, default=0.0, nullable=False)
    last_y = db.Column(db.Float, default=0.0, nullable=False)
    last_event_id = db.Column(db.Integer, db.ForeignKey('location_event.id'),
                              nullable=False)

    created_time = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, onupdate=datetime.utcnow)
    removed_time = db.Column(db.Integer, default=0, index=True)

    def __repr__(self):
        return '<Robot %r>' % self.name
