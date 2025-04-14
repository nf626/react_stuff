#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 3 """

import unittest
from app.models.user import User
from app.api.v1.auth import Login

class TestUser(unittest.TestCase):
    """Test that the User model works as expected
    """

    def test_create_user(self):
        """Tests creation of User instances """
        user = User(first_name="Peter", last_name="Parker", email="iluvspiderman@dailybugle.com", password="spidey")

        assert user.first_name == "Peter"
        assert user.last_name == "Parker"
        assert user.email == "iluvspiderman@dailybugle.com"
        assert user.is_admin is False  # Default value
        print("Peter creation test passed!")

    def test_create_user2(self):
        """Tests creation of User instances """
        user = User(first_name="John", last_name="Doe", email="john.doe@gmail.com", password="123")

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@gmail.com"
        assert user.is_admin is False  # Default value
        print("John creation test passed!")

    def test_create_user3(self):
        """Tests creation of User instances """
        user = User(first_name="Jane", last_name="Doe", email="jane.doe@gmail.com", password="456")

        assert user.first_name == "Jane"
        assert user.last_name == "Doe"
        assert user.email == "jane.doe@gmail.com"
        assert user.is_admin is False  # Default value
        print("Jane creation test passed!")

if __name__ == '__main__':
    unittest.main()
