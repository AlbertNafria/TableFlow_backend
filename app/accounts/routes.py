import re
from flask import jsonify, request, session
from app.accounts import bp
from app.extensions import db
from app.models.user import User

# Login route
@bp.route("/api/v1/login", methods=["POST"])
def login():
    # Collect info from the form
    username, password = request.get_json()['username'], request.get_json()['password']
    user = User.query.filter_by(username=username).first()
    if session.get('user_id'):
        return jsonify({"KO": "Already logged"})
    if user and user.check_password(password):
        session["username"] = username
        return jsonify({"OK": 12345})
    else:
        return jsonify({"KO": "Bad Credentials"})

# Register route
@bp.route("/api/v1/register", methods=["POST", "PUT"])
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
@bp.route("/api/v1/logout", methods=["GET"])
def logout():
    session["username"] = None
    return jsonify({"KO": "Logged Out"})


# List Users
@bp.route("/api/v1/list_users", methods=["GET"])
def list_users():
    result = db.session.execute(db.select(User))
    all_users = result.scalars().all()
    return jsonify(Users=[user.to_dict() for user in all_users])

'''
# Query Users
@bp.route("/api/v1/query_user/<id:int>", methods=["GET"])
def query_user():
    result = db.session.execute(db.select(User))
    all_users = result.scalars().all()
    return jsonify(Users=[user.to_dict() for user in all_users])

'''