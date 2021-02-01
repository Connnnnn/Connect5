from flask_restful import Api

from api.results import ResultsApi, ResultApi
from api.authentication import SignUpApi, LoginApi, CheckForUserApi
from api.play_game import MakeMoveApi, CreateGameApi, JoinGameApi
from api.user import UsersApi, UserApi


def create_routes(api):
    """Adds resources to the api.
        :param api: Flask-RESTful Api Object
        :Example:
            api.add_resource(HelloWorld, '/', '/hello')
            api.add_resource(Foo, '/foo', endpoint="foo")
            api.add_resource(FooSpecial, '/special/foo', endpoint="foo")
        """

    api.add_resource(SignUpApi, '/authentication/signup/')
    api.add_resource(LoginApi, '/authentication/login/')
    api.add_resource(CheckForUserApi, '/authentication/checkUser/')

    api.add_resource(UsersApi, '/user/')
    api.add_resource(UserApi, '/user/<user_id>')

    api.add_resource(ResultsApi, '/result/')
    api.add_resource(ResultApi, '/result/<result_id>/')

    api.add_resource(MakeMoveApi, '/play/')
    api.add_resource(CreateGameApi, '/host/<game_code>/')
    api.add_resource(JoinGameApi, '/join/<game_code>/')
