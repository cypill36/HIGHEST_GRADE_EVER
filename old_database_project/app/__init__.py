from flask import Flask
from .main import main_bp
from .auth import auth_bp
from .models import db
from flask_login import LoginManager


def create_app(conf):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "f6c0bacc8d4f072a552973dfb4e13cf5"
<<<<<<< HEAD
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{conf['user']}:{conf['password']}@{conf['location']}/{conf['database']}"
=======
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{conf['user']}:{conf['password']}@{conf['location']}/{conf['database']}"
>>>>>>> 3e95c82985593e0e87eec8301c088e9f6d3e6601

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    login_manager = LoginManager()
    login_manager.login_view = "auth_bp.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
