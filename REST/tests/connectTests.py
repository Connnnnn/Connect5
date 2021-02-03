import hashlib
import random
from urllib import response

import requests
from nose.tools import assert_true, assert_equals

user_name_p1 = "Con"
user_name_p2 = "Steve"
password = "password"

game_code = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:5]

# checkUser api-endpoint
check = "http://127.0.0.1:5000/authentication/checkUser/"

# login api-endpoint
login = "http://127.0.0.1:5000/authentication/login/"

# register api-endpoint
signup = "http://127.0.0.1:5000/authentication/signup/"

# host api-endpoint
host = f"http://127.0.0.1:5000/host/{game_code}/"

# join api-endpoint
join = f"http://127.0.0.1:5000/join/{game_code}/"

# make_move retrieving game info api-endpoint
game = f"http://127.0.0.1:5000/game/{game_code}/"

# make_move making move api-endpoint
move_req = f"http://127.0.0.1:5000/play/{game_code}/"

default_board = [['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                 [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]

test_board = [['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[ ]', '[x]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[ ]', '[x]', '[o]', '[x]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[x]', '[o]', '[o]', '[o]', '[ ]', '[ ]'],
              ['[ ]', '[ ]', '[x]', '[o]', '[o]', '[0]', '[x]', '[ ]', '[ ]'],
              [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]


def test_name_check_status_code():
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "userName": user_name_p1
    }

    acc_req = requests.post(url=check, json=PARAMS)

    assert acc_req.status_code == 200


def test_name_is_equal():
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "userName": user_name_p1
    }

    acc_req = requests.post(url=check, json=PARAMS)
    user_info = acc_req.json()
    name = user_info.get('User')

    assert_equals(name, user_name_p1)


def test_register_status_code():
    userId = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:10]
    reg_new_name = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:5]

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "userId": userId,
        "userName": reg_new_name,
        "password": password
    }

    reg_res = requests.post(url=signup, json=PARAMS)

    assert reg_res.status_code == 200


def test_login_status_code():
    PARAMS = {
        "userName": user_name_p1,
        "password": password
    }
    login_res = requests.post(url=login, json=PARAMS)

    assert login_res.status_code == 200


def test_host_status_code():
    game_id = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:10]

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "game_id": game_id,
        "game_code": game_code,
        "player_1": user_name_p1,
        "game_status": "open",
        "board": default_board
    }

    host_req = requests.post(url=host, json=PARAMS)
    assert host_req.status_code == 200


def test_join_status_code():
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "game_code": game_code,
        "player_2": user_name_p2
    }

    join_req = requests.post(url=join, json=PARAMS)
    assert join_req.status_code == 200


def test_make_move_get_curr_game_info_status_code():
    info_req = requests.get(url=game)
    assert info_req.status_code == 200


def test_make_move_get_curr_game_status_p1_move():
    info_req = requests.get(url=game)
    game_info = info_req.json()

    status = game_info.get('result').get('game_status')
    print(f"Status {status}")

    assert_equals(status, "p1_turn")


def test_make_move_check_for_p2_turn():
    curr_move = "3"

    status = "p1_turn"

    PARAMS1 = {
        "game_code": game_code,
        "board": default_board,
        "move": curr_move,
        "game_status": status
    }

    make_move_req = requests.post(url=move_req, json=PARAMS1)
    updated_info = make_move_req.json()
    new_status = updated_info.get('result').get('game_status')
    print(f"Status {new_status}")

    assert_equals(new_status, "p2_turn")

def test_make_move_check_for_win():
    curr_move = "3"

    status = "p1_turn"

    PARAMS1 = {
        "game_code": game_code,
        "board": test_board,
        "move": curr_move,
        "game_status": status
    }

    make_move_req = requests.post(url=move_req, json=PARAMS1)
    updated_info = make_move_req.json()
    new_status = updated_info.get('result').get('game_status')
    print(f"Status {new_status}")

    assert_equals(new_status, "p1_wins")



