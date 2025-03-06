from flask import Flask, jsonify, request, abort
from models import Cupcake, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cupcakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()  # Fetch all cupcakes
    results = [
        {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }
        for cupcake in cupcakes
    ]
    return jsonify({"cupcakes": results})

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get(id)  # Get the cupcake by ID
    if cupcake is None:
        abort(404)  # Return 404 if not found
    return jsonify({
        "cupcake": {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }
    })

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.get_json()  # Get JSON data from request body

    # Get fields from the request data
    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', 'https://tinyurl.com/demo-cupcake')  # Use default image if none provided

    # Ensure all fields are present
    if not flavor or not size or not rating:
        abort(400, description="Missing required fields.")

    # Create a new cupcake instance
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify({
        "cupcake": {
            "id": new_cupcake.id,
            "flavor": new_cupcake.flavor,
            "size": new_cupcake.size,
            "rating": new_cupcake.rating,
            "image": new_cupcake.image
        }
    }), 201  # Return 201 (Created)

if __name__ == '__main__':
    app.run(debug=True)
