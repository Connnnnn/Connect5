# flask packages
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

# project resources
from models.results import results
from models.user import user
from api.errors import unauthorized

# external packages
import datetime


class SignUpApi(Resource):
    """
    Flask-resftul resource for creating new user.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add SignUpApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(SignUpApi, '/authentication/signup')
    """

    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """

        data = request.get_json()
        post_user = user(**data)
        post_user.save()

        output = {'id': str(post_user.id)}
        return jsonify({'result': output})


class LoginApi(Resource):
    """
    Flask-resftul resource for retrieving user web token.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add LoginApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(LoginApi, '/authentication/login')
    """

    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.
        :return: JSON object
        """

        print(request)

        data = request.get_json()
        print(data)
        us = user.objects.get(userName=data.get('userName'))

        auth_success = us.check_pw_hash(password=data.get('password'))
        if not auth_success:
            return unauthorized()
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{us.userName}"}})


class CheckForUserApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user. Used to see if user already has registered
        :return: JSON object
        """

        data = request.get_json()
        us = user.objects.get(userName=data.get('userName'))

        return jsonify({'User': f"{us.userName}"})


