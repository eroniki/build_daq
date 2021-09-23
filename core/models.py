from sqlalchemy.sql import func
from flask_login import UserMixin
from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), nullable=False)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def is_active(self):
        """True, as all users are active."""
        return True

    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
	#     return User.query.get(int(user_id))

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
