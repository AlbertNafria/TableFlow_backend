from datetime import timedelta
from flask import Flask
from flask_session import Session
from flask_jwt_extended import JWTManager # type: ignore
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialización extensiones
    db.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)
    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)

    # Create a permanent session
#    app.permanent_session_lifetime = timedelta(days=1)

    # Register blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/api/v1')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/api/v1')

    @app.route('/test/')
    def test():
        return '<h1>Test</h1>'

    return app
