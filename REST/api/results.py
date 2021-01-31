# flask packages
from flask import jsonify, Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# mongo-engine models
from models.results import results
from api.errors import forbidden


class ResultsApi(Resource):
    """
        Flask-resftul resource for returning db.results collection.
        :Example:
        >>> from flask import Flask
        >>> from flask_restful import Api
        >>> from app import default_config
        # Create flask app, config, and resftul api, then add ResultsApi route
        >>> app = Flask(__name__)
        >>> app.config.update(default_config)
        >>> api = Api(app=app)
        >>> api.add_resource(ResultsApi, '/result/')
        """

    @jwt_required
    def get(self) -> Response:

        """
            GET response method for all documents in result collection.
            JSON Web Token is required.

            :return: JSON object
        """

        output = results.objects()
        return jsonify({'result': output})

    @jwt_required
    def post(self) -> Response:

        """
        POST response method for creating a result.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """

        authorized: bool = results.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            data = request.get_json()
            post_user = results(**data).save()
            output = {'id': str(post_user.id)}
            return jsonify({'result': output})
        else:
            return forbidden()


class ResultApi(Resource):
    """
    Flask-resftul resource for returning db.results collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add ResultApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ResultsApi, '/result/<result_id>')
    """

    @jwt_required
    def get(self, result_id: str) -> Response:

        """
        GET response method for single documents in result collection.
        :return: JSON object
        """

        output = results.objects.get(id=result_id)
        return jsonify({'result': output})

    @jwt_required
    def put(self, result_id: str) -> Response:

        """
        PUT response method for updating a result.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """

        data = request.get_json()
        put_user = results.objects(id=result_id).update(**data)
        return jsonify({'result': put_user})

    @jwt_required
    def delete(self, user_id: str) -> Response:

        """
        DELETE response method for deleting single result.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """

        authorized: bool = results.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = results.objects(id=user_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden()
