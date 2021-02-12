from flask import Response, request, jsonify
from flask_restful import Resource
from models.game import game
from api.errors import forbidden
import pymongo

DB_URL = "mongodb+srv://admin:WHUwh7G8STmvO7IZ@connect5.thcpu.mongodb.net/Connect5?retryWrites=true&w=majority"


class CreateGameApi(Resource):
    """
        Flask-resftul resource for creating game
        :Example:
        >>> from flask import Flask
        >>> from flask_restful import Api
        >>> from app import default_config
        # Create flask app, config, and resftul api, then add CreateGameApi route
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
        post_game = game(**data)
        post_game.save()

        output = {'id': str(post_game.id)}
        return jsonify({'result': game_code})


class JoinGameApi(Resource):
    """
        Flask-resftul resource for connecting to open game
        :Example:
        >>> from flask import Flask
        >>> from flask_restful import Api
        >>> from app import default_config
        # Create flask app, config, and resftul api, then add JoinGameApi route
        >>> app = Flask(__name__)
        >>> app.config.update(default_config)
        >>> api = Api(app=app)
        >>> api.add_resource(MakeMoveApi, '/join/<game_code>/')
        """

    @staticmethod
    def get(game_code: str) -> Response:
        """
        GET response method for retrieving game info.
        :return: JSON object
        """

        game_info = game.objects.get(game_code=game_code)

        return jsonify({'result': game_info})

    @staticmethod
    def post(game_code: str) -> Response:
        """
        Post response method used to check game status and to add the second player
        :return: JSON object
        """
        player_2 = request.get_json().get('player_2')

        game_info = game.objects.get(game_code=game_code)

        my_client = pymongo.MongoClient(DB_URL)
        my_db = my_client["Connect5"]
        game_col = my_db["game"]

        my_query = {"game_code": game_code}
        new_values = {"$set": {"player_2": player_2, "game_status": "p1_turn"}}
        game_col.update_one(my_query, new_values)

        return jsonify({'result': game_info})


class GetGameInfo(Resource):
    """
            Flask-resftul resource for connecting to open game
            :Example:
            >>> from flask import Flask
            >>> from flask_restful import Api
            >>> from app import default_config
            # Create flask app, config, and resftul api, then add GetGameInfo route
            >>> app = Flask(__name__)
            >>> app.config.update(default_config)
            >>> api = Api(app=app)
            >>> api.add_resource(GetGameInfo, '/game/<game_code>/')
            """

    @staticmethod
    def get(game_code: str) -> Response:
        """
        GET response method for retrieving game info.
        :return: JSON object
        """

        game_info = game.objects.get(game_code=game_code)

        return jsonify({'result': game_info})

    @staticmethod
    def post(game_code: str) -> Response:
        """
        Post response method used to change game status
        :return: JSON object
        """

        game_info = game.objects.get(game_code=game_code)
        turn = game_info.game_status

        my_client = pymongo.MongoClient(DB_URL)
        my_db = my_client["Connect5"]
        game_col = my_db["game"]
        my_query = {"game_code": game_code}

        if turn == "p1_turn":
            new_values = {"$set": {"game_status": "p2_turn"}}
        elif turn == "p2_turn":
            new_values = {"$set": {"game_status": "p1_turn"}}
        else:
            new_values = {"$set": {"game_status": "finished"}}
        game_col.update_one(my_query, new_values)

        return jsonify({'result': game_info})


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
    >>> api.add_resource(MakeMoveApi, '/play/<game_code>/')
    """

    @staticmethod
    def post(game_code) -> Response:
        data = request.get_json()
        game_info = game.objects.get(game_code=game_code)
        status = data.get('game_status')
        board = data.get('board')
        column = int(data.get('move'))
        piece = " "
        p1_name = game_info.player_1
        p2_name = game_info.player_2
        game_over = False

        active = False
        msg = None

        my_client = pymongo.MongoClient(DB_URL)
        my_db = my_client["Connect5"]
        game_col = my_db["game"]
        my_query = {"game_code": game_code}

        if status == "p1_turn":
            piece = "x"
            active = True
            curr_player = p1_name
        elif status == "p2_turn":
            piece = "o"
            active = True
            curr_player = p2_name

        row = 0

        if active:
            column = column - 1
            i = 5
            for i in range(5, -1, -1):
                if i == -1:
                    print("Column Full!")
                    new_values = {"$set": {"msg": i}}

                    game_col.update_one(my_query, new_values)

                    return jsonify({'result': game_info})
                    # Break out and tell them return original board and say re-enter
                if board[i][column] != "[x]" and board[i][column] != "[o]":
                    board[i][column] = f"[{piece}]"
                    row = i
                    break

        else:
            print("Game Over")
            game_over = True
            return jsonify({'result': game_info})

            # Break out and say game over
        # Checking for the four different win types - Vertical, Horizontal, and the 2 diagonals

        # Checking for diagonal win

        diag_win = 0
        for a in range(5, -5, -1):
            x = row + a
            y = column + a
            if 0 <= x < 6 and 0 <= y < 9:
                if board[x][y] == f"[{piece}]":
                    diag_win = diag_win + 1

                    if diag_win == 5:
                        print("You've Won Diagonally!")
                        break
                else:
                    diag_win = 0

        vert_win = 0
        # Checking for vertical win
        for b in range(4, -4, -1):
            x = row + b
            y = column
            if 0 <= x < 6 and 0 <= y < 9:
                if board[x][y] == f"[{piece}]":
                    vert_win = vert_win + 1
                    if vert_win == 5:
                        print("You've Won Vertically!")
                        break
                else:
                    vert_win = 0

        diag2_win = 0
        # Checking for the second diagonal win
        for c in range(5, -5, -1):
            x = row + c
            y = column - c

            if 0 <= x < 6 and 0 <= y < 9:
                if board[x][y] == f"[{piece}]":
                    diag2_win = diag_win + 1

                    if diag2_win == 5:
                        print("You've Won Diagonally!")
                        break
                else:
                    diag2_win = 0

        hor_win = 0
        # Checking for horizontal win
        for d in range(5, -5, -1):
            x = row
            y = column + d
            if 0 <= x < 6 and 0 <= y < 9:
                if board[x][y] == f"[{piece}]":
                    hor_win = hor_win + 1

                    if hor_win == 5:
                        print("You've Won Diagonally!")
                        break
                else:
                    hor_win = 0

        my_client = pymongo.MongoClient(DB_URL)
        my_db = my_client["Connect5"]
        game_col = my_db["game"]
        my_query = {"game_code": game_code}

        if diag_win >= 5 or diag2_win >= 5 or hor_win >= 5 or vert_win >= 5:
            print(f"{curr_player} Wins!")
            if curr_player == p1_name:
                new_values = {"$set": {"game_status": "p1_wins"}}
            elif curr_player == p2_name:
                new_values = {"$set": {"game_status": "p2_wins"}}

            game_over = True

        else:
            if status == "p1_turn":
                new_values = {"$set": {"game_status": "p2_turn", "board": board, "msg": msg}}
            elif status == "p2_turn":
                new_values = {"$set": {"game_status": "p1_turn", "board": board, "msg": msg}}

        game_col.update_one(my_query, new_values)

        return jsonify({'result': game_info})
