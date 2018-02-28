import logging

from flask import Flask, request as req

# from app.controllers import pages
from api.v1_0.models import db
from v1_0 import views


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.register_blueprint(views.blueprint)

    app.logger.setLevel(logging.NOTSET)
    db.init_app(app)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app, db
