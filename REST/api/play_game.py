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
        print(data)
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

        print(game_code)
        game_info = game.objects.get(game_code=game_code)

        return jsonify({'result': game_info})

    @staticmethod
    def post(game_code: str) -> Response:
        """
        Post response method used to check game status and to add the second player
        :return: JSON object
        """
        player_2 = request.get_json().get('player_2')

        print(game_code)
        game_info = game.objects.get(game_code=game_code)

        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = my_client["test_db"]
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

        print(f"Game Code - {game_code}")
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

        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = my_client["test_db"]
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
        move = int(data.get('move'))
        piece = " "
        p1_name = game_info.player_1
        p2_name = game_info.player_2
        game_over = False

        in_a_row_top_left = 1
        in_a_row_top_right = 1
        in_a_row_hor = 1
        in_a_row_vert = 1
        active = False
        msg = None

        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = my_client["test_db"]
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
            move = move - 1
            i = 5
            for i in range(5, -1, -1):
                if i == -1:
                    print("Column Full!")
                    new_values = {"$set": {"msg": i}}

                    game_col.update_one(my_query, new_values)

                    return jsonify({'result': game_info})
                    # Break out and tell them return original board and say re-enter
                if board[i][move] != "[x]" and board[i][move] != "[o]":
                    board[i][move] = f"[{piece}]"
                    row = i
                    break

        else:
            print("Game Over")
            game_over = True
            return jsonify({'result': game_info})

            # Break out and say game over

        # Check for win
        #
        #
        #          [a]        [b]        [c]
        #          [d]     [row][move]   [e]
        #          [f]        [g]        [h]
        #
        #   in_a_row_top_left is the diagonal line in both directions from a through middle and to h
        #   in_a_row_top_right is the diagonal line in both directions from c through middle and to f
        #   in_a_row_hor is the horizontal line in both directions from d through middle and to e
        #   in_a_row_vert is the vertical line in both directions from b through middle and to g

        # Checking for in_a_row_top_left win

        # a
        if row > 0 and move > 0 and board[row - 1][move - 1] == f"[{piece}]":
            in_a_row_top_left += 1

            if row > 1 and move > 1 and board[row - 2][move - 2] == f"[{piece}]":
                in_a_row_top_left += 1

                if row > 2 and move > 2 and board[row - 3][move - 3] == f"[{piece}]":
                    in_a_row_top_left += 1

                    if row > 3 and move > 3 and board[row - 4][move - 4] == f"[{piece}]":
                        in_a_row_top_left += 1

        # h
        if row < 4 and move < 8 and board[row + 1][move + 1] == f"[{piece}]":
            in_a_row_top_left += 1

            if row < 3 and move < 7 and board[row + 2][move + 2] == f"[{piece}]":
                in_a_row_top_left += 1

                if row < 2 and move < 6 and board[row + 3][move + 3] == f"[{piece}]":
                    in_a_row_top_left += 1

                    if row < 1 and move < 5 and board[row + 4][move + 4] == f"[{piece}]":
                        in_a_row_top_left += 1

        # Checking for in_a_row_vert win

        # b
        if row > 0 and board[row - 1][move] == f"[{piece}]":
            in_a_row_vert += 1

            if row > 1 and board[row - 2][move] == f"[{piece}]":
                in_a_row_vert += 1

                if row > 2 and board[row - 3][move] == f"[{piece}]":
                    in_a_row_vert += 1

                    if row > 3 and board[row - 4][move] == f"[{piece}]":
                        in_a_row_vert += 1

        #  g
        if row < 5 and board[row + 1][move] == f"[{piece}]":
            in_a_row_vert += 1

            if row < 4 and board[row + 2][move] == f"[{piece}]":
                in_a_row_vert += 1

                if row < 3 and board[row + 3][move] == f"[{piece}]":
                    in_a_row_vert += 1

                    if row < 2 and board[row + 4][move] == f"[{piece}]":
                        in_a_row_vert += 1

        # Checking for in_a_row_top_right win

        # c
        if row > 0 and move < 8 and board[row - 1][move + 1] == f"[{piece}]":
            in_a_row_top_right += 1

            if row > 1 and move < 7 and board[row - 2][move + 2] == f"[{piece}]":
                in_a_row_top_right += 1

                if row > 2 and move < 6 and board[row - 3][move + 3] == f"[{piece}]":
                    in_a_row_top_right += 1

                    if row > 3 and move < 5 and board[row - 4][move + 4] == f"[{piece}]":
                        in_a_row_top_right += 1

        # f
        if row < 5 and move > 0 and board[row + 1][move - 1] == f"[{piece}]":
            in_a_row_top_right += 1

            if row < 4 and move > 1 and board[row + 2][move - 2] == f"[{piece}]":
                in_a_row_top_right += 1

                if row < 3 and move > 2 and board[row + 3][move - 3] == f"[{piece}]":
                    in_a_row_top_right += 1

                    if row < 2 and move > 3 and board[row + 4][move - 4] == f"[{piece}]":
                        in_a_row_top_right += 1

        # Checking for in_a_row_hor win

        # d

        if move > 0 and board[row][move - 1] == f"[{piece}]":
            in_a_row_hor += 1
            if move > 1 and board[row][move - 2] == f"[{piece}]":
                in_a_row_hor += 1
                if move > 2 and board[row][move - 3] == f"[{piece}]":
                    in_a_row_hor += 1
                    if move > 3 and board[row][move - 4] == f"[{piece}]":
                        in_a_row_hor += 1

        # e

        if move < 8 and board[row][move + 1] == f"[{piece}]":
            in_a_row_hor += 1
            if move < 7 and board[row][move + 2] == f"[{piece}]":
                in_a_row_hor += 1
                if move < 6 and board[row][move + 3] == f"[{piece}]":
                    in_a_row_hor += 1
                    if move < 5 and board[row][move + 4] == f"[{piece}]":
                        in_a_row_hor += 1

        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = my_client["test_db"]
        game_col = my_db["game"]
        my_query = {"game_code": game_code}

        if in_a_row_top_left >= 5 or in_a_row_top_right >= 5 or in_a_row_hor >= 5 or in_a_row_vert >= 5:
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
