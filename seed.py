from app import app
from models import db, Cupcake



# This ensures that the Flask app context is active when interacting with the database
with app.app_context():
    db.drop_all()
    db.create_all()

    c1 = Cupcake(
        flavor="cherry",
        size="large",
        rating=5,
    )

    c2 = Cupcake(
        flavor="chocolate",
        size="small",
        rating=9,
        image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
    )

    c3 = Cupcake(
        flavor="strawberry",
        size="large",
        rating=8,
        image="https://images.unsplash.com/photo-1532678465554-94846274c297?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    )

    db.session.add_all([c1, c2])
    db.session.commit()
