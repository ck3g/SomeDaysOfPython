from .utils import *
from routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_users(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": test_user.id,
        "username": test_user.username,
        "email": test_user.email,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "role": test_user.role,
        "phone_number": test_user.phone_number,
    }


def test_change_password_success(test_user):
    response = client.put(
        "/user/change_password",
        json={
            "current_password": "testpassword",
            "new_password": "new_testpassword",
            "password_confirmation": "new_testpassword",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/change_password",
        json={
            "current_password": "wrong-testpassword",
            "new_password": "new_testpassword",
            "password_confirmation": "new_testpassword",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "invalid password"}


def test_change_password_invalid_password_confirmation(test_user):
    response = client.put(
        "/user/change_password",
        json={
            "current_password": "testpassword",
            "new_password": "new_testpassword",
            "password_confirmation": "new_testpassword_does_not_match",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": "password and password confirmation to not match"
    }
