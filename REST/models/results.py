from mongoengine import Document, StringField, ReferenceField
from models.user import user


class results(Document):
    """
        Template for a mongoengine document, which represents a games results
        :param game_id: required string value
        :param player_1_id: required reference user value
        :param player_2_id: required reference user value
        :param winner: required reference user value

        :Example:
        >>> import mongoengine
        >>> from app import default_config
        >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
        MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
        >>> new_results = results(game_id= "002", player_1_id= "001", player_2_id="002", winner="002")
        >>> new_results.save()
        <results: results object>
        """

    game_id = StringField(required=True)
    player_1 = ReferenceField(user, required=True)
    player_2 = ReferenceField(user, required=True)
    winner = ReferenceField(user, required=True)


