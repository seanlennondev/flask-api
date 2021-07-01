# from enum import Enum, unique
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from gameover.api.ext.database import db
from .mixins import DateTimeMixin
from .news import News

""" @unique
class Role(Enum):
    ADMIN = 'admin_only'
    SUPERUSER = 'superuser_only'
    USER = 'user_only' """

class User(DateTimeMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, index=True, nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    surname = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    __password_hash = db.Column(db.String, nullable=False)
    __is_superuser = db.Column(db.Boolean, default=False)
    __role = db.Column(db.String(100), index=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    news = db.relationship(News, backref='user', lazy=True)

    @property
    def is_superuser(self):
        return self.__is_superuser

    @is_superuser.setter
    def is_superuser(self, is_superuser):
        self.__is_superuser = is_superuser

    @property
    def password(self):
        return self.__password_hash

    @password.setter
    def password(self, password):
        self.__password_hash = generate_password_hash(password)

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    def __repr__(self):
        return f'<User username({self.username})>'

    def __init__(self, username, name, surname, email, password):
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def jsonify(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'password': self.password,
            'is_superuser': self.is_superuser,
            'role': self.role,
            'is_active': self.is_active
        }

    def insert(self):
        db.session.add(self)

    def update(self, name, surname):
        self.name = name
        self.surname = surname

    def delete(self):
        db.session.delete(self)

    def superuser(self, is_superuser):
        self.is_superuser = is_superuser

    def add_role(self, role):
        self.role = role

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def generate_access_token(self):
        return create_access_token(identity=self.email, additional_claims={
            'username': self.username,
            'role': self.role,
            'is_superuser': self.is_superuser
        })

    def check_password(self, current_password):
        return check_password_hash(self.password, current_password)

    def change_password(self, new_password):
        self.password = new_password

    def commit(self):
        db.session.commit()
