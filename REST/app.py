import os
# flask packages
from flask import Flask, app
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from api.routes import create_routes
import configparser

def get_flask_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for wsgi (gunicorn) server.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    app = Flask(__name__)

    parser = configparser.ConfigParser()
    parser.read("db_config.txt")

    DB_URI = parser.get("config", "uri")

    app.config["MONGODB_HOST"] = DB_URI
    app.config["JWT_SECRET_KEY"] = parser.get("config", "key")

    # init api and routes
    api = Api(app=app)
    create_routes(api=api)

    # init mongoengine
    db = MongoEngine(app=app)

    # init jwt manager
    jwt = JWTManager(app=app)

    return app


if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    app = get_flask_app()
    app.run(debug=True)
