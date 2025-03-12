import pytest
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def default_test_user():
    return {"username": "test_user",
            "password": "test_password",
            "email": "test@email.local"}


@pytest.fixture
@pytest.mark.django_db
def create_user(django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def not_authorized_api_client():
    api_client = APIClient()

    return api_client


@pytest.fixture
@pytest.mark.django_db
def authorized_api_client(create_user, default_test_user):
    user = create_user(username=f"api_{default_test_user['username']}",
                       password=f"api_{default_test_user['password']}",
                       email=f"api_{default_test_user['email']}")
    token = Token.objects.create(user=user)

    api_client = APIClient()
    api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    return api_client


@pytest.fixture
def not_authorized_ui_client():
    ui_client = Client()

    return ui_client


@pytest.fixture
@pytest.mark.django_db
def authorized_ui_client(create_user, default_test_user):
    user = create_user(username=f"ui_{default_test_user['username']}",
                       password=f"ui_{default_test_user['password']}",
                       email=f"ui_{default_test_user['email']}")

    ui_client = Client()
    ui_client.force_login(user=user)

    return ui_client
