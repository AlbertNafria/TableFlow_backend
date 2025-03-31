from flask import Flask, session
from config import Config
from app.extensions import db

#login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #config_class.init_app(app)

    # Inicialización extensiones
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.accounts import bp as accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/api/v1')

    @app.route('/test/')
    def test():
        return '<h1>Test</h1>'

    return app
