from django.contrib.auth.models import User
from rest_framework import status
import pytest
from store.models import Collection
from model_bakery import baker


@pytest.fixture
def auth_user(api_client):
    def do_auth_user(user):
        api_client.force_authenticate(user=user)

    return do_auth_user


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip # Skipping tests
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # AAA (Arrange, Act, Assert)

        # Arrange

        # Act
        response = create_collection({"title": "Test Collection"})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, auth_user, create_collection):
        auth_user({})
        response = create_collection({"title": "Test Collection"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, auth_user, create_collection):
        auth_user(User(is_staff=True))
        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self, auth_user, create_collection):
        auth_user(User(is_staff=True))
        response = create_collection({"title": "Test Collection"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        # Collection.objects.create(title="Test Collection")
        collection = baker.make(Collection)

        response = api_client.get(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }
