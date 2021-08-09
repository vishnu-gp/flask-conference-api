from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()

# Many to Many Relationship connecting tables
speakers = db.Table('speakers',
    db.Column('talk_id', db.Integer, db.ForeignKey('talks.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

participants = db.Table('participants',
    db.Column('talk_id', db.Integer, db.ForeignKey('talks.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Conference(db.Model):
    __tablename__ = 'conferences'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    talks = db.relationship('Talk', cascade="all,delete", backref='talks', lazy=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, title, description, start_date, end_date, talks):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.talks = talks

class Talk(db.Model):
    __tablename__ = 'talks'
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id'), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_min = db.Column(db.Integer, nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    speakers = db.relationship('User', cascade="all,delete", secondary=speakers, lazy='subquery',
        backref=db.backref('speakers', lazy=True))
    participants = db.relationship('User', cascade="all,delete", secondary=participants, lazy='subquery',
        backref=db.backref('participants', lazy=True))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, title, description, duration_min, scheduled_at, speakers, participants):
        self.title = title
        self.description = description
        self.duration_min = duration_min
        self.scheduled_at = scheduled_at
        self.speakers = speakers
        self.participants = participants

class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    email = fields.String(required=True)

class ConferenceSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

class TalkSchema(ma.Schema):
    id = fields.Integer()
    conference_id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=False)
    duration_min = fields.Integer(required=True)
    scheduled_at = fields.Date(required=True)
    speakers = fields.List(fields.Nested("UserSchema"))
    participants = fields.List(fields.Nested("UserSchema"))