from flask_restful import Api

from api.results import ResultsApi, ResultApi
from api.authentication import SignUpApi, LoginApi
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

    api.add_resource(UsersApi, '/user/')
    api.add_resource(UserApi, '/user/<user_id>')

    api.add_resource(ResultsApi, '/result/')
    api.add_resource(ResultApi, '/result/<result_id>')
