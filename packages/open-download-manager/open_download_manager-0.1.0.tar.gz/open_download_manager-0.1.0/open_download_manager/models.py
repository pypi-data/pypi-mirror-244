from sqlalchemy_serializer import SerializerMixin

from open_download_manager.ext.database import db


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))

class Download(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    running = db.Column(db.Boolean())
    status = db.Column(db.Float())
    path = db.Column(db.String())
    content_length = db.Column(db.Integer())