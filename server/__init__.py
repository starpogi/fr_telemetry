import os

from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from server.tools import data_generator

alembic = Alembic()
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config=None):
    config = config or os.environ['CONFIG']

    app = Flask(__name__)

    app.config.from_object(config)
    alembic.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from server import views
    from server import models

    app.register_blueprint(views.api.blueprint)

    app.cli.add_command(data_generator.cli, "tools")

    return app
