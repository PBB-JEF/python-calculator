from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instantiate extensions (do NOT bind to app here)
db = SQLAlchemy()
login_manager = LoginManager()