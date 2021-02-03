import os
import jwt
# flask packages
import pymongo
from flask import Flask, app
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mongoengine import MongoEngine
from pymongo import MongoClient

from api.routes import create_routes

# default mongodb configuration
default_config = {'MONGODB_SETTINGS': {
    'db': 'Connect',
    'host': 'connect5.thcpu.mongodb.net',
    'username': 'admin',
    'password': 'WHUwh7G8STmvO7IZ',
    'authentication_source': 'admin'},
     'JWT_SECRET_KEY': 'B540E36ECF5803C5AFC1D239E9FC40256C2C85D35562D8341A72D96C25A08104'
}


def get_flask_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for wsgi (gunicorn) server.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    app = Flask(__name__)

    DB_URI = "mongodb+srv://admin:WHUwh7G8STmvO7IZ@connect5.thcpu.mongodb.net/Connect5?retryWrites=true&w=majority"

    app.config["MONGODB_HOST"] = DB_URI
    app.config["JWT_SECRET_KEY"] = "B540E36ECF5803C5AFC1D239E9FC40256C2C85D35562D8341A72D96C25A08104"

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
