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
import datetime
force_auto_coercion() #for the password
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    name = db.Column(db.String(50), nullable = True)
    last_name = db.Column(db.String(100), nullable = True)
    signed_up = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    gender = db.Column(db.String(100), nullable = True)
    complexion = db.Column(db.String(100), nullable = True)
    race = db.Column(db.String(100), nullable = True)
    img_path = db.Column(db.String(100), nullable = True)
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



class UserImage(db.Model):
    __tablename__ = 'user_image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey("disease.id"), nullable=True) #if this image has been identified to a disease
    size = db.Column(db.String(100))
    img_description = db.Column(db.Text)
    color = db.Column(db.String(100))
    physical_appearance = db.Column(db.String(100))
    def __repr__(self):
        return "<UserImage(%s)>" % (self.patient_id)


class Disease(db.Model):
    __tablename__ = 'disease'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    region = db.Column(db.String(100), nullable = False)
    color = db.Column(db.String(100), nullable = False)
    physical_appearance = db.Column(db.String(100), nullable = True)
    age_range_high = db.Column(db.Integer, nullable = True) 
    age_range_low = db.Column(db.Integer, nullable = True) #constraints needed on age 
    symptoms = db.Column(db.Text, nullable = False)
    more_info = db.Column(db.Text, nullable = True)
    def __repr__(self):
        return "<Disease(%s, %s)>" % (self.id, self.name)





class DiseaseImage(db.Model):
    __tablename__ = 'disease_image'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    path = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    disease_id = db.Column(db.Integer, db.ForeignKey("disease.id", ondelete='CASCADE'), nullable=False)
    def __repr__(self):
        return "<DiseaseImage for(%s, %s)>" % (self.disease_id, self.path)





def list_model_to_dict(inst, cls):
    items = []
    for obj in inst:
        items.append(model_to_dict(obj, cls))
    return items



def model_to_dict(inst, cls):
#can use inst.__class instead of cls **** looking into this
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
