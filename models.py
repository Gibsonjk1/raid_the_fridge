from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db=SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):
    """Connects Database """

    db.app = app
    db.init_app(app)

class Recipe(db.Model):
    __tablename__ = "recipes"

    recipe_index = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.Text, nullable=False, unique=True)
    recipe_details = db.Column(db.Text, nullable = False)

class Customer(db.Model):
    __tablename__="customers"

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_username = db.Column(db.Text, nullable=False, unique=True)
    customer_password = db.Column(db.Text, nullable=False)
    customer_first_name = db.Column(db.Text, nullable=False)
    customer_last_name = db.Column(db.Text, nullable=False)

class Customer_Recipe(db.Model):
    __tablename__="customer_recipes"

    customer_recipe_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Text, nullable="false")
    recipe_id = db.Column(db.Text, nullable="false")

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True,)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False