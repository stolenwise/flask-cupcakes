# app.py
from flask import Flask, jsonify, request, render_template
from models import db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# from flask import Flask, jsonify, request, abort
# from flask_sqlalchemy import SQLAlchemy

# # Initialize the app
# app = Flask(__name__)

# # Database setup
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)  # directly initializing SQLAlchemy here

# # Define the Cupcake model
# class Cupcake(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     flavor = db.Column(db.String(100), nullable=False)
#     size = db.Column(db.String(100), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     image = db.Column(db.String(100), nullable=False, default="https://tinyurl.com/demo-cupcake")

# # Create the database (for the first time)
# with app.app_context():
#     db.create_all()


@app.route('/')
def show_homepage():
    return render_template('index.html')

# Define the routes
@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    results = [{"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image} for cupcake in cupcakes]
    return jsonify({"cupcakes": results})

# Create a new cupcake via POST
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.get_json()
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image']
    )
    db.session.add(new_cupcake)
    db.session.commit()
    
    print("Added cupcake:", new_cupcake)  # <-- Add this line

    return jsonify({"cupcake": {
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image
    }})


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and new data passed in the body."""
    cupcake = Cupcake.query.get(id)

    # If the cupcake does not exist, return a 404 error
    if cupcake is None: 
        return jsonify({"message": "Cupcake not found"}), 404
    
    #Get the data from the request
    data = request.get_json()

    if "flavor" in data:
        cupcake.flavor = data["flavor"]
    if "size" in data:
        cupcake.size = data["size"]
    if "rating" in data:
        cupcake.rating = data["rating"]
    if "image" in data:
        cupcake.image = data["image"]

    db.session.commit()

    return jsonify({
        "cupcake": {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }
    })

@app.route('/api/cupcakes/<id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get(id)
    if cupcake:
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200
    else:
        return jsonify({"error": "Cupcake not found"}), 404




if __name__ == "__main__":
    app.run(debug=True, port=5001)
