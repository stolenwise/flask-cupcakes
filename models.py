from cupcakes import db

"""Models for Cupcake app."""
class Cupcake:
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False, default="https://tinyurl.com/demo-cupcake")

    

