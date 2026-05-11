import uuid
import pytest
from api.auth_api import AuthAPI
from api.club_api import ClubAPI
from api.clubs_api import ClubsAPI

BASE_URL = "https://book-club.qa.guru"


@pytest.fixture
def auth_api():
    return AuthAPI(BASE_URL)


@pytest.fixture
def club_api():
    return ClubAPI(BASE_URL)


@pytest.fixture
def clubs_api():
    return ClubsAPI(BASE_URL)


@pytest.fixture
def existing_user():
    return {
        "username": "j6gh9FQjPRADVNsPtpHwwXgnRQE8MkXblfHieZ6B",
        "password": "string",
    }


@pytest.fixture
def random_user():
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{unique_id}",
        "password": f"pass_{unique_id}",
    }


@pytest.fixture
def register_user(auth_api, random_user):
    def _register():
        return auth_api.register(random_user["username"], random_user["password"])

    return _register


@pytest.fixture
def login_user(auth_api):
    def _login(username, password):
        return auth_api.login(username, password)

    return _login


@pytest.fixture
def auth_token(login_user, existing_user):
    response = login_user(existing_user["username"], existing_user["password"])
    assert response.status_code == 200
    return response.json()["access"]


@pytest.fixture
def create_club(club_api, auth_token):
    def _create_club(data):
        return club_api.create_club(data, auth_token)
    return _create_club