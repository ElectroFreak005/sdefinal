#database
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    source=db.Column(db.String(100))
    dest=db.Column(db.String(100))
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    name=db.Column(db.String(100))
    username=db.Column(db.String(100))
    apno=db.Column(db.String(10))
    notes=db.relationship('Note')

class Service(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True)
    occupation=db.Column(db.String(20))
    phno=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(20),unique=True)

class Announcement(db.Model,UserMixin):
    a_id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())

class To_do(db.Model,UserMixin):
    user_id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(20),unique=True)
    rent=db.Column(db.Boolean,default=False,nullable=False)
    main=db.Column(db.Boolean,default=False,nullable=False)
    dr=db.Column(db.Boolean,default=False,nullable=False)
    eb=db.Column(db.Boolean,default=False,nullable=False)