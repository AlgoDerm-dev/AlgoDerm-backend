from constants import DATABASE_URL
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import session, request
import json
import time
import uuid
import datetime as date
from datetime import datetime as dt
from flask import Flask, request, jsonify, send_from_directory,send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from models import *
import hashlib
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    with app.app_context():
        db.create_all() #needed to create the tables 
    return app


app = create_app()
oauth = OAuth2Provider(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)


#@oauth.require_oauth()

@app.route('/api/users', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.json.get("username")
        email = request.json.get("email") #validate email 
        user = User.query.filter_by(username = username).first()
        if not user:
            user = User(**request.json)
            db.session.add(user)
            db.session.commit()
            userjson = model_to_dict(user, User)
            del userjson["password"]
            m = hashlib.md5()
            m.update(str(userjson["id"]).encode("utf-8"))
            userjson["id"] = str(int(m.hexdigest(), 16))[0:12]
            return jsonify({"result" : userjson})
        else:
            return jsonify({"error" : "username already taken"}), 403


@app.route('/client')
def client():
    user = User.query.filter_by(id=1).first()
    if not user:
        return jsonify({'error': 'no user found'}), 404
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
            ]),
        _default_scopes='email',
        user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok

@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect('/login')
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)
    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    if user.verify_password(password):
        return user
    return None


def current_user():
    if session.get('id'):
        uid = session["id"]
        return User.query.get(uid)
    return None
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
