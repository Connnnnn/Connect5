from mongoengine import Document, StringField, ReferenceField
from models.user import user


class game(Document):
    """
        Template for a mongoengine document, which represents a games results
        :param game_id: required string value
        :param player_1_id: required reference user value
        :param player_2_id: required reference user value
        :param game_status: required reference user value

        :Example:
        >>> import mongoengine
        >>> from app import default_config
        >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
        MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
        >>> new_game = game(game_id= "002", player_1_id= "53b4d13008", player_2_id="7fadbde4ee", game_status="active")
        >>> new_game.save()
        <game: game object>
        """

    game_id = StringField(required=True, unique=True)
    game_code = StringField(required=True)
    player_1 = ReferenceField(user, required=True)
    player_2 = ReferenceField(user)
    game_status = StringField(required=True)


