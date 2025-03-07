from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance
db = SQLAlchemy()

# Initialize the db object with the app instance in app.py
def init_app(app):
    db.init_app(app)