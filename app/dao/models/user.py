from marshmallow import Schema, fields

from app.database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=True)
    genre = db.relationship("Genre")
 #   new_password = db.Column(db.String, nullable=True)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()
 #   new_password = fields.Str()
