# test_app.py
import unittest
from fastapi.testclient import TestClient
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_user1(self):
        response = self.client.post(
            "/users",
            json={"username": "testusser", "email": "tesst@example.com", "hashed_password": "testpassword"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "username": "testusser", "email": "tesst@example.com"})
        print(response.json())  #


if __name__ == "__main__":
    unittest.main()