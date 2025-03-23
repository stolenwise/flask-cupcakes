from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    
    def test_patch_cupcake(self):
        with app.test_client() as client:
            # Create a new cupcake
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)

            created_cupcake_id = resp.json['cupcake']['id']

            # Ensure the cupcake is created
            self.assertEqual(Cupcake.query.count(), 1)

            # Step 3: Prepare the patch data with new information
            patch_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 8,
                "image": "http://test.com/updated_cupcake.jpg"
            }

            # Send the PATCH request to update the cupcake
            url = f"/api/cupcakes/{created_cupcake_id}"
            resp = client.patch(url, json=patch_data)
            
            # Ensure the response status is 200 (OK)
            self.assertEqual(resp.status_code, 200)

            # Check if the response data is the updated cupcake
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": created_cupcake_id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 8,
                    "image": "http://test.com/updated_cupcake.jpg"
                }
            })

            # Check if the changes were saved in the database
            updated_cupcake = Cupcake.query.get(created_cupcake_id)
            self.assertEqual(updated_cupcake.flavor, "UpdatedFlavor")
            self.assertEqual(updated_cupcake.size, "UpdatedSize")
            self.assertEqual(updated_cupcake.rating, 8)
            self.assertEqual(updated_cupcake.image, "http://test.com/updated_cupcake.jpg")



            
    
    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)

            # Get the id of  the created cupcake
            created_cupcake_id = resp.json['cupcake']['id']

            # Delete the cupcake using the id
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {"message": "deleted"})

            deleted_cupcake = Cupcake.query.get(created_cupcake_id)
            self.assertIsNone(deleted_cupcake)

            self.assertEqual(Cupcake.query.count(), 1)
