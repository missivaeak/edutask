import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController as uc

# Initialize UserController instance with a mock DAO object
user_controller = uc(Mock())

class dbErrDao:
    def find(self, query):
        raise Exception("Database error")

def test_get_user_by_email_valid_email():
    # Arrange
    email = "test@example.com"
    user_data = {"email": email, "name": "Test User"}
    # DAO object's find method to return user_data when called with the email
    user_controller.dao.find.return_value = [user_data]

    # Act
    user = user_controller.get_user_by_email(email)
    
    # Assert
    # Verify that a user object is returned when a valid email is provided
    assert user == user_data
    
def test_get_user_by_email_invalid_email():
    # Arrange
    email = "This is an invalid email."

    # Act and Assert
    # Verify that ValueError is raised when an invalid email is provided
    with pytest.raises(ValueError):
        user_controller.get_user_by_email(email)

def test_get_user_by_email_multiple_users(capsys):
    # Arrange
    email = "test@example.com"
    user_1 = {"email": email, "name": "Test User 1"}
    user_2 = {"email": email, "name": "Test User 2"}
    user_controller.dao.find.return_value = [user_1, user_2]

    # Act
    user = user_controller.get_user_by_email(email)

    # Assert
    # Verify that the first user found is returned and a warning message is printed
    assert user == user_1
    captured = capsys.readouterr()
    assert f'Error: more than one user found with mail {email}' in captured.out

def test_get_user_by_email_no_user():
    # Arrange
    email = "test@example.com"
    user_controller.dao.find.return_value = []

    # Act
    user = user_controller.get_user_by_email(email)

    # Assert
    # Verify that None is returned when no user is found
    assert user == None

def test_get_user_by_email_db_error():
    # Arrange
    email = "test@example.com"
    db_user_controller = uc(dbErrDao())

    # Act and Assert
    # Verify that an Exception is raised when a database error occurs
    with pytest.raises(Exception):
        db_user_controller.get_user_by_email(email)
    
