from mongoengine import Document, StringField, IntField, EmbeddedDocument, BooleanField, EmbeddedDocumentField
from flask_bcrypt import generate_password_hash, check_password_hash


class Access(EmbeddedDocument):
    """
    Custom EmbeddedDocument to set user authorizations.
    :param user: boolean value to signify if user is a user
    :param admin: boolean value to signify if user is an admin
    """
    user = BooleanField(default=True)
    admin = BooleanField(default=False)


class user(Document):
    """
        Template for a mongoengine document, which represents a user.
        Password is automatically hashed before saving.
        :param userId: unique required user_id-string value
        :param password: required string value, longer than 6 characters
        :param access: Access object
        :param userName: required string username
        :param numWins: optional int value

        :Example:
        >>> import mongoengine
        >>> from app import default_config
        >>> mongoengine.connect(**default_config['MONGODB_SETTINGS'])
        MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
        >>> new_user = user(userId= "002", password= "password2",access={"admin": True}, userName= "Eve")
        >>> new_user.save()

        """

    userId = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    access = EmbeddedDocumentField(Access, default=Access(user=True, admin=False))
    userName = StringField(unique=True)

    def generate_pw_hash(self):
        self.password = generate_password_hash(password=self.password).decode('utf-8')

    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(pw_hash=self.password, password=password)

    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_pw_hash()
        super(user, self).save(*args, **kwargs)

