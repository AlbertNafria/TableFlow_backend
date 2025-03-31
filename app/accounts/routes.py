import re
from flask import g, jsonify, request, session
from app.accounts import bp
from app.extensions import db, auth
from app.models.user import User


# Login route
@bp.route("/login", methods=["POST"])
def login():
    # Collect info from the request
    username, password = request.get_json()['username'], request.get_json()['password']
    user = User.query.filter_by(username=username).first()
    if session.get('username'):
        return jsonify({"KO": "Already logged"})
    if user and user.check_password(password):
        session["username"] = username
        return jsonify({"OK": session['username']})
    else:
        return jsonify({"KO": "Bad Credentials"})


# Register a new user
@bp.route("/register", methods=["POST", "PUT"])
def register():
    username, password = request.get_json()['username'], request.get_json()['password']
    if username is None or password is None:
        return jsonify({"KO": "Missing arguments"}), 400
    elif User.query.filter_by(username=username).first():
        return jsonify({"KO": "User already registered!"})
    elif re.match("^\S*$", username): #regular expresion to find spaces inbetween username
        return jsonify({"KO": "Don't use spaces"})
    else:
        new_user = User(username=username)#, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return jsonify({"OK": 12345}), 201


# Logout route
@bp.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    return jsonify({"KO": "Logged Out"})


# Query a user
@bp.route("/query_user/<int:id>", methods=["GET"])
def query_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"KO": "El usuario con id: {id} no existe"})
    return jsonify(user.to_dict())


# List Users
@bp.route("/list_users", methods=["GET"])
def list_users():
    result = db.session.execute(db.select(User))
    all_users = result.scalars().all()
    return jsonify(Users=[user.to_dict() for user in all_users])


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


# Request a JSON Web Token
@bp.route("/token")
@auth.login_required
def get_auth_token():
    user = User.query.filter_by(username=username).first()
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })