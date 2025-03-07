# models.py
from db import db  # Import db from db.py

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False, default="https://tinyurl.com/demo-cupcake")
