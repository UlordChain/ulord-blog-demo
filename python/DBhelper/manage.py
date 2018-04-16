# coding=utf-8
# @File  : manage.py
# @Author: PuJi
# @Date  : 2018/4/10 0010
import os, sys

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from passlib.apps import custom_app_context as pwd_context
from flask_cors import CORS
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

sys.path.append('../')
from config import DevConfig

# initialization
app = Flask(__name__)
# dbpath = os.path.join(os.path.join(app.root_path,'DBhelper'), 'sqlite.db')
# app.config['SECRET_KEY'] = 'ulord platform is good'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(dbpath)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.from_object(DevConfig)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)


blogs_tags = db.Table('blogs_tags',
                        db.Column('blog_id', db.String(45), db.ForeignKey('blogs.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


users_blogs = db.Table('users_blogs',
                        db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
                        db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id')))


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    cellphone = db.Column(db.String(12))
    token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(10))
    balance = db.Column(db.Float)
    wallet = db.Column(db.String(34))
    pay_password = db.Column(db.String(128))
    reads = db.relationship(
        'Blog',
        secondary=users_blogs,
        backref=db.backref('blogs', lazy='dynamic')
    )
    # reads = db.Column(db.String(128))
    # Reserved field
    pre1= db.Column(db.String())
    pre2 = db.Column(db.String())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(32), index=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(46))
    amount = db.Column(db.Float, index=True)
    tags = db.relationship(
        'Tag',
        secondary=blogs_tags,
        backref=db.backref('blogs', lazy='dynamic'))
    description = db.Column(db.String(128))
    views = db.Column(db.Integer)
    date = db.Column(db.Integer)
    claimID = db.Column(db.String(40))

    # Reserved field
    pre1 = db.Column(db.String())
    pre2 = db.Column(db.String())


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(32), index=True)
    # Reserved field
    pre1 = db.Column(db.String())
    pre2 = db.Column(db.String())

    def __init__(self, name):
        self.tagname = name


class Billing(db.Model):
    __tablename__ = 'billings'
    id = db.Column(db.Integer, primary_key=True)
    payer = db.Column(db.Integer, index=True)
    amount = db.Column(db.Float)
    payee = db.Column(db.Integer, index=True)
    titleid = db.Column(db.Integer, db.ForeignKey('blogs.id')) # title_id foreign key

    # Reserved field
    pre1 = db.Column(db.String())
    pre2 = db.Column(db.String())


if __name__ == '__main__':
    db.create_all()

