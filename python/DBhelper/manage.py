# coding=utf-8
# @File  : manage.py
# @Author: PuJi
# @Date  : 2018/4/10 0010
import sys

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from passlib.apps import custom_app_context as pwd_context
from flask_cors import CORS

sys.path.append('../')
from config import DevConfig

# initialization
app = Flask(__name__)

app.config.from_object(DevConfig)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    cellphone = db.Column(db.String(12))
    token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(10))
    wallet = db.Column(db.String(34))
    pay_password = db.Column(db.String(128))
    # Reserved field
    pre1= db.Column(db.String())
    pre2 = db.Column(db.String())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


if __name__ == '__main__':
    db.create_all()

