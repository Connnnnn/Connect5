from __future__ import print_function, unicode_literals
import hashlib
import random
import sys
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt
import requests
import time

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

f = Figlet(font='slant')
print(f.renderText('Connect 5'))


class Account:

    def login(self, user_name):
        questions = [
            {
                'type': 'password',
                'message': 'Enter password',
                'name': 'password'
            }
        ]
        login_answers = prompt(questions, style=style)

        # login api-endpoint
        login = "http://127.0.0.1:5000/authentication/login/"
        password_input = login_answers.get("password")

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "userName": user_name,
            "password": password_input
        }

        login_req = requests.post(url=login, json=PARAMS)

        if login_req.status_code == 200:
            self.play(user_name)
        else:
            print("Incorrect password, try again")
            self.login(user_name)

    def register(self, user_name):
        questions = [
            {
                'type': 'password',
                'message': 'Enter password',
                'name': 'password'
            }
        ]
        reg_answers = prompt(questions, style=style)

        # register api-endpoint
        check = "http://127.0.0.1:5000/authentication/signup/"
        password_input = reg_answers.get("password")
        userId = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:10]

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "userId": userId,
            "userName": user_name,
            "password": password_input
        }

        reg_req = requests.post(url=check, json=PARAMS)

        if reg_req.status_code == 200:
            print("Account found, enter password:")
            self.login(user_name)
        else:
            print("Error making account, try again")
            self.register(user_name)

    def name_check(self):
        questions = [
            {
                'type': 'input',
                'message': 'Enter Username',
                'name': 'userName'
            }
        ]
        check_answers = prompt(questions, style=style)

        # checkUser api-endpoint
        check = "http://127.0.0.1:5000/authentication/checkUser/"
        user_name_input = check_answers.get("userName")

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "userName": user_name_input
        }

        acc_req = requests.post(url=check, json=PARAMS)

        if acc_req.status_code == 200:
            print("Account found, enter password:")
            self.login(user_name_input)
        else:
            print("Account not found, enter password to create:")
            self.register(user_name_input)

    def play(self, user_name):
        print(f.renderText('Play!'))

        questions = [
            {
                'type': 'input',
                'message': 'Host or Join Game? (input = "host" or "join")',
                'name': 'playType'
            }
        ]
        play_answers = prompt(questions, style=style)
        playType = play_answers.get("playType")

        if playType == "host":
            print("Hosting Selected")
            self.host(user_name)

        elif playType == "join":
            print("Joining Selected")

            self.join(user_name)

        elif playType != "host" or playType != "join":
            print("Incorrect Option, please Re-enter Lobby choice")

    def host(self, user_name):
        game_code = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:5]
        game_id = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:10]

        default_board = [['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         ['[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'],
                         [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']]

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "game_id": game_id,
            "game_code": game_code,
            "player_1": user_name,
            "game_status": "open",
            "board": default_board
        }
        host = f"http://127.0.0.1:5000/host/{game_code}/"
        host_req = requests.post(url=host, json=PARAMS)

        if host_req.status_code == 200:
            print("Game Made Successfully")
            print(f"Your Game code is - {game_code}")
            self.load_match(user_name, game_code)
        else:
            print("Problem creating game, please try again")
            self.host(user_name)

    def join(self, user_name):
        questions = [
            {
                'type': 'input',
                'message': 'Please Enter Game Code',
                'name': 'game_code'
            }
        ]
        join_answers = prompt(questions, style=style)
        game_code = join_answers.get("game_code")

        join = f"http://127.0.0.1:5000/join/{game_code}/"

        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "game_code": game_code,
            "player_2": user_name
        }

        join_req = requests.post(url=join, json=PARAMS)
        game_info = join_req.json()

        if join_req.status_code == 200:

            if game_info.get('result').get('game_code') == game_code:
                print("Correct game code")

                if game_info.get('result').get('game_status') == "open":
                    self.load_match(user_name, game_code)

                elif game_info.get('result').get('game_status') == "ongoing" or game_info.get('result').get(
                        'game_status') == "p1_turn" or game_info.get('result').get('game_status') == "p2_turn":
                    print("Error - Game ongoing")
                    self.join(user_name)
                elif game_info.get('result').get('game_status') == "closed":
                    print("Game finished")
                    self.join(user_name)
                else:
                    print("Error - Null Game Status")
                    self.join(user_name)
            else:
                print("Error Joining Game - Try Again")
                self.join(user_name)

        else:
            print("Game not found, try again")
            self.join(user_name)

    def load_match(self, user_name, game_code):

        # checkUser api-endpoint
        game = f"http://127.0.0.1:5000/game/{game_code}/"

        join_req = requests.get(url=game)
        game_info = join_req.json()

        p1 = game_info.get('result').get('player_1')
        p2 = game_info.get('result').get('player_2')
        print(p2)
        print("Waiting for Other Player...")
        while p2 is None:
            time.sleep(5)
            join_req = requests.get(url=game)
            game_info = join_req.json()
            p2 = game_info.get('result').get('player_2')

        print(f"Player 1 is {p1}")

        print(f"Player 2 is {p2}")

        if user_name == p1:
            print("GAME START")
            self.make_move(game_code, user_name)

        elif user_name == p2:
            print("GAME START")
            self.wait_for_move(game_code, user_name)

    def make_move(self, game_code, user_name):
        game = f"http://127.0.0.1:5000/game/{game_code}/"
        info_req = requests.get(url=game)
        game_info = info_req.json()

        p1 = game_info.get('result').get('player_1')
        p2 = game_info.get('result').get('player_2')
        board = game_info.get('result').get('board')
        status = game_info.get('result').get('game_status')

        for list in board:
            print(list)

        if status == "p1_wins":
            print(f"{p1} wins!")
            time.sleep(2)
            print("Closing game")
            time.sleep(1)
            sys.exit("...")

        elif status == "p2_wins":
            print(f"{p2} wins!")
            time.sleep(2)
            print("Closing game")
            time.sleep(1)
            sys.exit("...")

        elif status == "finished":
            print("Game over")
            time.sleep(2)
            print("Closing game")
            time.sleep(1)
            sys.exit("...")

        questions = [
            {
                'type': 'input',
                'message': 'Enter a number between 0-9 to make your move',
                'name': 'move'
            }
        ]

        move_answer = prompt(questions, style=style)
        curr_move = move_answer.get("move")

        move_req = f"http://127.0.0.1:5000/play/{game_code}/"

        PARAMS1 = {
            "game_code": game_code,
            "board": board,
            "move": curr_move,
            "game_status": status
        }

        make_move_req = requests.post(url=move_req, json=PARAMS1)
        updated_info = make_move_req.json()

        msg = updated_info.get('result').get('msg')

        if msg is not None:
            for list in msg:
                print(f"{list} full!")

        if user_name == p1:
            print(f"Your turn {p1}!")
        elif user_name == p2:
            print(f"Your turn {p2}!")

        print(f"{curr_move} selected")

        self.wait_for_move(game_code, user_name)

    def wait_for_move(self, game_code, user_name):
        game = f"http://127.0.0.1:5000/game/{game_code}/"
        join_req = requests.get(url=game)
        game_info = join_req.json()

        p1 = game_info.get('result').get('player_1')
        p2 = game_info.get('result').get('player_2')

        status = game_info.get('result').get('game_status')

        if user_name == p1:
            print(f"Waiting for {p2} to make move...")

            while status == "p2_turn":
                time.sleep(2)
                join_req = requests.get(url=game)
                game_info = join_req.json()
                status = game_info.get('result').get('game_status')

            self.make_move(game_code, user_name)

        elif user_name == p2:
            print(f"Waiting for {p1} to make move...")

            while status == "p1_turn":
                time.sleep(2)
                join_req = requests.get(url=game)
                game_info = join_req.json()
                status = game_info.get('result').get('game_status')

            self.make_move(game_code, user_name)


def main():
    acc = Account()
    acc.name_check()


if __name__ == "__main__":
    main()
