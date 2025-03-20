from flask import Flask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
#    app.secret_key = "secret_key"

    # Inicialización extensiones
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp) # , url_prefix='/api/v1'

    return app
