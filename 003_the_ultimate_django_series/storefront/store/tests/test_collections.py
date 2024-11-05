from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip # Skipping tests
    def test_if_user_is_anonymous_returns_401(self):
        # AAA (Arrange, Act, Assert)

        # Arrange

        # Act
        client = APIClient()
        response = client.post("/store/collections/", {"title": "Test Collection"})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
