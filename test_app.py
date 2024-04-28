import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def clear_database():
    response = client.post("/clear_db")
    assert response.status_code == 204


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_user(self):
        response = self.client.post(
            "/users",
            json={"username": "testusser", "email": "tesst@example.com", "hashed_password": "testpassword"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "username": "testusser", "email": "tesst@example.com"})
        print(response.json())  #
        clear_database()

    def test_create_book(self):
        response = self.client.post(
            "/books",
            json={"title": "testbook", "author": "testauthor", "description": "testdescription"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "title": "testbook", "author": "testauthor", "description": "testdescription"})
        print(response.json())
        clear_database()

    def test_get_book(self):
        # First, create a book to retrieve
        create_book_response = self.client.post(
            "/books",
            json={"title": "testbook", "author": "testauthor", "description": "testdescription"},
        )
        self.assertEqual(create_book_response.status_code, 201)
        book_id = create_book_response.json()["id"]

        # Now, attempt to retrieve the book
        get_book_response = self.client.get(f"/books/{book_id}")

        # Check if the response is successful
        self.assertEqual(get_book_response.status_code, 200)

        # Check if the retrieved book matches the expected data
        expected_book_data = {"id": book_id, "title": "testbook", "author": "testauthor",
                              "description": "testdescription"}
        self.assertEqual(get_book_response.json(), expected_book_data)
        print(get_book_response.json())

    def test_create_rating1(self):
        response = self.client.post(
            "/ratings",
            json={"user_id": 1, "book_id": 1, "rating": 5},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "user_id": 1, "book_id": 1, "rating": 5})
        print(response.json())
        clear_database()

    def test_get_rating(self):
        # First, create a rating
        create_rating_response = self.client.post(
            "/ratings",
            json={"user_id": 1, "book_id": 1, "rating": 5},
        )
        self.assertEqual(create_rating_response.status_code, 201)
        rating_id = create_rating_response.json()["id"]

        # Now, attempt to retrieve the rating
        get_rating_response = self.client.get(f"/ratings/{rating_id}")

        # Check if the response is successful
        self.assertEqual(get_rating_response.status_code, 200)

        # Check if the retrieved rating matches the expected data
        expected_rating_data = [{"id": rating_id, "user_id": 1, "book_id": 1, "rating": 5}]
        self.assertEqual(get_rating_response.json(), expected_rating_data)
        print(get_rating_response.json())

    def test_create_discussion(self):
        response = self.client.post(
            "/discussions",
            json={"user_id": 1, "book_id": 1, "content": "testcontent"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "user_id": 1, "book_id": 1, "content": "testcontent"})
        print(response.json())
        clear_database()

    def test_get_discussion(self):
        # First, create a discussion
        create_discussion_response = self.client.post(
            "/discussions",
            json={"user_id": 1, "book_id": 1, "content": "testcontent"},
        )
        self.assertEqual(create_discussion_response.status_code, 201)
        discussion_id = create_discussion_response.json()["id"]

        # Now, attempt to retrieve the discussion
        get_discussion_response = self.client.get(f"/discussions/{discussion_id}")

        # Check if the response is successful
        self.assertEqual(get_discussion_response.status_code, 200)

        # Check if the retrieved discussion matches the expected data
        expected_discussion_data = [{"id": discussion_id, "user_id": 1, "book_id": 1, "content": "testcontent"}]
        self.assertEqual(get_discussion_response.json(), expected_discussion_data)
        print(get_discussion_response.json())


if __name__ == "__main__":
    unittest.main()

