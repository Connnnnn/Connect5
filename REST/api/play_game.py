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


def check_for_win(board, piece, x, y, amount_in_a_row):
    if 0 <= x < 6 and 0 <= y < 9:
        if board[x][y] == f"[{piece}]":
            amount_in_a_row = amount_in_a_row + 1

            if amount_in_a_row == 5:
                print("You've Won!")
                return True, amount_in_a_row

        else:
            amount_in_a_row = 0
    return False, amount_in_a_row


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

        # Checking for the four different win types - Vertical, Horizontal, and the 2 diagonals

        # Checking for vertical win

        vertical_win_check = False
        vertical_pieces_in_a_row = 0
        for a in range(5, -5, -1):
            vertical_win_check, vertical_pieces_in_a_row = check_for_win(board, piece, row + a, column,
                                                                         vertical_pieces_in_a_row)
            if vertical_win_check is True:
                break

        # Checking for left diagonal win

        left_diagonal_win_check = False
        left_diagonal_pieces_in_a_row = 0
        for a in range(5, -5, -1):
            left_diagonal_win_check, left_diagonal_pieces_in_a_row = check_for_win(board, piece, row + a, column + a,
                                                                                   left_diagonal_pieces_in_a_row)
            if left_diagonal_win_check is True:
                break

        # Checking for right diagonal win

        right_diagonal_win_check = False
        right_diagonal_pieces_in_a_row = 0
        for a in range(5, -5, -1):
            right_diagonal_win_check, right_diagonal_pieces_in_a_row = check_for_win(board, piece, row + a, column - a,
                                                                                     right_diagonal_pieces_in_a_row)
            if right_diagonal_win_check is True:
                break

        # Checking for horizontal win

        horizontal_win_check = False
        horizontal_pieces_in_a_row = 0
        for a in range(5, -5, -1):
            horizontal_win_check, horizontal_pieces_in_a_row = check_for_win(board, piece, row, column + a,
                                                                             horizontal_pieces_in_a_row)
            if horizontal_win_check is True:
                break

        my_client = pymongo.MongoClient(DB_URL)
        my_db = my_client["Connect5"]
        game_col = my_db["game"]
        my_query = {"game_code": game_code}

        if left_diagonal_win_check is True or right_diagonal_win_check is True or horizontal_win_check is True or vertical_win_check is True:
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
