# Connect5

# Description 

This repo holds the files of a Command line connect 5 game based in python. It allows the user to register an account, log in, host a game or join their friends.

The project works off a Flask web server to implement an API, with a MongoDB Database using the flask module mongo-engine.

### Assumptions 
- Once a user registers, their information is stored in the database and their password hashed. 
- Many pairs of users can play independently of each other.

### Python CLI Application 
The game is mostly contained within the connect.py file which creates a Command line application for the user. The application itself primarly processes the users answers, which are then communicated with the established Flask APIs in order to make requests or to check the game logic. 

### FlaskAPI and Server 
The flask server runs locally on port 5000. The RestAPI was designed to handle the logic of the game and to retrieve and deliver data from the database to the application. The gameflow is as follows: 

<p align="center">
 <img src="https://i.gyazo.com/5e72ddbe910f8442ac0b6799e09fb37c.png" width="385" height="681"/>
</p>

### MongoDB

The database was intially hosted locally and then deployed on MongoDB Atlas so it can be access by anyone. I chose MongoDB due to my past experiences with implementing it to an application. The Schema has two tables: Users and Games. The Users table stores the userId, the password (which is hashed), the access the user has (admin, or user) and the userName. The game table continues the game_id and game_code (both of which are hashed with SHA256 UTF-8), the name for player_1 and player_2, the game_status (open, p1_turn, p2_turn, p1_wins, p2_wins), the board and the current move. 

### Tests
Tests can be found in the tests folder under ConnectTests.py

## Deploying 
**Note : In order to connect to the database for the game to be operational, the config file is required. This can be sent upon request**

In order to streamline the process, I have created two batch files.

- The first is called prereqs.bat which is used for setting the python version, activating the virtual environment, downloading pip and then downloading all dependencies in the requirements.txt file. 

- The second batch file, Connect-5.bat, opens 3 command prompts - app.py which is the flask server application, and two game applications in order for 2 players to play together.

If the above fail to launch the application, then I would reccommend opening the project in PyCharm and selecting the python interpreter as an existing interpreter inside of the venv folder. 
If this still does not work then I am happy to send a video of the operational program or to have a Zoom call where I share my screen. 

## Images 
Here are some photos of the game:

- Launching the application

<a href="https://imgur.com/zQpudp0"><img src="https://i.imgur.com/zQpudp0.png" title="source: imgur.com" /></a>

- Logging in and selecting a game type

<a href="https://imgur.com/aaEgp0n"><img src="https://i.imgur.com/aaEgp0n.png" title="source: imgur.com" /></a>

- The hosting and joining process

<a href="https://imgur.com/pQtzcts"><img src="https://i.imgur.com/pQtzcts.png" title="source: imgur.com" /></a>

- Game Over - Steve wins!

<a href="https://imgur.com/1xHkNBC"><img src="https://i.imgur.com/1xHkNBC.png" title="source: imgur.com" /></a>
