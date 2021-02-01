from flask import Response, request, jsonify
from flask_restful import Resource
from models.game import game
from api.errors import forbidden
import pymongo


class CreateGameApi(Resource):
    """
        Flask-resftul resource for creating game
        :Example:
        >>> from flask import Flask
        >>> from flask_restful import Api
        >>> from app import default_config
        # Create flask app, config, and resftul api, then add MakeMoveApi route
        >>> app = Flask(__name__)
        >>> app.config.update(default_config)
        >>> api = Api(app=app)
        >>> api.add_resource(MakeMoveApi, '/host/<game_code>/')
        """

    @staticmethod
    def post(game_code) -> Response:
        """
        POST response method for creating game.
        :return: JSON object
        """

        data = request.get_json()
        print(data)
        post_game = game(**data)
        post_game.save()

        output = {'id': str(post_game.id)}
        return jsonify({'result': game_code})

    @staticmethod
    def patch(game_code: str) -> Response:
        """
        PATCH response method for adding a second player to an established game
        :return: JSON object
        """

        data = request.get_json()
        ##patch_game = game.objects(id=game_code).
        patch_game = game.objects(id=game_code).update(**data)
        output = {'id': str(patch_game).id}
        return jsonify({'result': output})


class JoinGameApi(Resource):
    """
        Flask-resftul resource for connecting to open game
        :Example:
        >>> from flask import Flask
        >>> from flask_restful import Api
        >>> from app import default_config
        # Create flask app, config, and resftul api, then add MakeMoveApi route
        >>> app = Flask(__name__)
        >>> app.config.update(default_config)
        >>> api = Api(app=app)
        >>> api.add_resource(MakeMoveApi, '/join/<game_code>/')
        """

    @staticmethod
    def post(game_code: str) -> Response:
        """
        GET response method for retrieving game code. Used to check game status and to add the second player
        :return: JSON object
        """
        player_2 = request.get_json().get('player_2')

        print(game_code)
        gc = game.objects.get(game_code=game_code)

        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = my_client["test_db"]
        game_col = my_db["game"]

        my_query = {"game_code": game_code}
        new_values = {"$set": {"player_2": player_2, "game_status": "ongoing"}}
        game_col.update_one(my_query, new_values)

        return jsonify({'result': gc})


class MakeMoveApi(Resource):
    """
    Flask-resftul resource for retrieving user web token.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add MakeMoveApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(MakeMoveApi, '/play/')
    """

    @staticmethod
    def post() -> Response:
        data = request.get_json()
        us = data.get('userName')

        # if curr_game.player1 is None:
        #    curr_game.player1 = us
        # elif curr_game.player2 is None:
    #     curr_game.player2 = us
