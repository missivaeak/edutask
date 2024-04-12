import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def usercontroller():
    dao = MagicMock()
    return UserController(dao)

def test_get_user_by_email_valid_email(usercontroller):
    # Arrange
    email = "test@example.com"
    user_data = {"email": email, "name": "Test User"}
    # DAO object's find method to return user_data when called with the email
    usercontroller.dao.find.return_value = [user_data]

    # Act
    user = usercontroller.get_user_by_email(email)
    
    # Assert
    # Verify that a user object is returned when a valid email is provided
    assert user == user_data
    
def test_get_user_by_email_invalid_email(usercontroller):
    # Arrange
    email = "This is an invalid email."

    # Act and Assert
    # Verify that ValueError is raised when an invalid email is provided
    with pytest.raises(ValueError):
        usercontroller.get_user_by_email(email)

def test_get_user_by_email_multiple_users(usercontroller, capsys):
    # Arrange
    email = "test@example.com"
    user_1 = {"email": email, "name": "Test User 1"}
    user_2 = {"email": email, "name": "Test User 2"}
    usercontroller.dao.find.return_value = [user_1, user_2]

    # Act
    user = usercontroller.get_user_by_email(email)

    # Assert
    # Verify that the first user found is returned and a warning message is printed
    assert user == user_1
    captured = capsys.readouterr()
    assert f'Error: more than one user found with mail {email}' in captured.out

def test_get_user_by_email_no_user(usercontroller):
    # Arrange
    email = "test@example.com"
    usercontroller.dao.find.return_value = []

    # Act
    user = usercontroller.get_user_by_email(email)

    # Assert
    # Verify that None is returned when no user is found
    assert user == None

def test_get_user_by_email_db_error(usercontroller):
    # Arrange
    email = "test@example.com"
    usercontroller.dao.find.side_effect = Exception()

    # Act and Assert
    # Verify that an Exception is raised when a database error occurs
    with pytest.raises(Exception):
        usercontroller.get_user_by_email(email)
