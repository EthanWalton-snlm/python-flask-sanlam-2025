import uuid

from flask_login import UserMixin

from extensions import db


# User - id, username, password
# Create - User Model & User Schema
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))

    # Object -> Dict
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
