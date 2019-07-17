import sqlite3
from db import db
from password import hashing
from flask_bcrypt import Bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.Text())

    def __init__(self, username, password):
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def json(self):
        return {
            'id': self.id,
            'username': self.username, 
            'password': self.password
            }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)