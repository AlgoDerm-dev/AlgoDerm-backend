import json
from flask import Flask
from flask import session, request
from flask_sqlalchemy import SQLAlchemy
from constants import SECRET_KEY
from collections import OrderedDict
from werkzeug.security import gen_salt
import datetime
from sqlalchemy_utils import PasswordType, force_auto_coercion
from datetime import datetime, timedelta
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from statistics import median

force_auto_coercion() #for the password
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    name = db.Column(db.String(50), nullable = True)
    phone = db.Column(db.String(10), nullable = True, unique = True) #add a phonenumber field 
    email = db.Column(db.String(75), nullable = False, unique = True)
    password = db.Column(
        PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
            
        ),
        unique=False,
        nullable=False,
    )
    def verify_password(self, password):
        return self.password == password

    def generate_auth_token(self, expiration = 600):
      s = Serializer(SECRET_KEY, expires_in = expiration)
      return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY) #add env var
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user




class Client(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []



class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []




class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    complexion = db.Column(db.String(100))
    race = db.Column(db.String(100))
    location = db.Column(db.String(100))


    def __init__(self, fname, lname):
            self.fname = fname
            self.lname = lname

    def __repr__(self):
            return "<Patient(%s, %s)>" % (self.fname, self.lname)

class NewImage(db.Model):
    __tablename__ = 'newimage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    date = db.Column(db.Date)
    dbmatch_id = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)

    def __init__(self, name):
            self.name = name

    def __repr__(self):
            return "<NewImage(%s, %s)>" % (self.name)

class Description(db.Model):
    __tablename__ = 'description'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(100))
    img_description = db.Column(db.String(100))
    color = db.Column(db.String(100))
    physical_appearance = db.Column(db.String(100))
    img_id = db.Column(db.Integer, db.ForeignKey("newimage.id"), nullable=False)

    def __init__(self, img_id):
            self.img_id = img_id

    def __repr__(self):
            return "<Description(%s, %s)>" % (self.img_id)

class DBImage(db.Model):
    __tablename__ = 'dbimage'

    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.Integer, db.ForeignKey("newimage.id"), nullable=False)

    def __init__(self, id):
            self.id = id
    def __repr__(self):
            return "<DBImage(%s, %s)>" % (self.id)



def list_model_to_dict(inst, cls):
    items = []
    for obj in inst:
        items.append(model_to_dict(obj, cls))
    return items



def model_to_dict(inst, cls):
  """
  Jsonify the sql alchemy query result. Skips attr starting with "_"
  """
  convert = { "DATETIME": datetime.isoformat}
  d = dict()
  for c in cls.__table__.columns:
    if c.name.startswith("_"):
      continue
    v = getattr(inst, c.name)
    current_type = str(c.type)
    if current_type in convert.keys() and v is not None:
      try:
        d[c.name] = convert[current_type](v)
      except:
        d[c.name] = "Error:  Failed to covert using ", str(convert[c.type], "utf-8")
    elif v is None:
      d[c.name] = str()
    else:
      d[c.name] = v
  return d
