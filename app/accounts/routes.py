import datetime
import config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required # type: ignore
from flask import jsonify, request, session
from app.accounts import bp
from app.extensions import db, auth
from app.models.user import User

# Login route
@bp.route("/login", methods=["POST"])
def login():
    # Collect info from the request
    username, password = request.get_json()['username'], request.get_json()['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        session['username'] = username
        session['token'] = access_token
        return jsonify({"OK": access_token})

    return jsonify({"KO": "Invalid Credentials"}), 401


# Register a new user
@bp.route("/register", methods=["POST", "PUT"])
def register():
    try:
        username, password = request.get_json()['username'], request.get_json()['password']
        if username is None or password is None:
            return jsonify({"KO": "Missing arguments"}), 400
        elif User.query.filter_by(username=username).first():
            return jsonify({"KO": "User already registered!"})
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        return jsonify({"OK": 12345}), 201
    except:
        return jsonify({"KO": "Missing arguments"}), 400


# Logout route
@bp.route("/logout", methods=["GET"])
#@jwt_required
def logout():
    session["username"] = None
    session.pop("token", None)
    return jsonify({"KO": "Logged Out"})


# Query a user
@bp.route("/query_user/<int:id>", methods=["GET"])
#@jwt_required
def query_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"KO": f"El usuario con id: {id} no existe"})
    return jsonify(user.to_dict())


# List Users
@bp.route("/list_users", methods=["GET"])
#@jwt_required
def list_users():
    result = db.session.execute(db.select(User))
    all_users = result.scalars().all()
    return jsonify(Users=[user.to_dict() for user in all_users])
