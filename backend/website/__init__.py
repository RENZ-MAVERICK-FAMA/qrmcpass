from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO  # Import SocketIO

db = SQLAlchemy()
DB_NAME = "database.db"

socketio = SocketIO()  # Create a SocketIO instance

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'QRMCPASS'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/qrmcpass'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')

app = create_app()

# Initialize the database
create_database(app)

# Initialize SocketIO with your Flask app
socketio.init_app(app)
