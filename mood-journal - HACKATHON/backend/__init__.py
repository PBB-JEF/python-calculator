from flask import Flask
from flask_cors import CORS
from .extensions import db, login_manager
from .routes import auth_bp, mood_bp
from .models import User, MoodEntry

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood_journal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(mood_bp, url_prefix='/mood')
    
    return app