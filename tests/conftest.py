import pytest
import requests

BASE_URL = "https://book-club.qa.guru"
CLUBS_ENDPOINT = f"{BASE_URL}/api/v1/clubs/"


@pytest.fixture
def clubs_endpoint():
    return CLUBS_ENDPOINT


@pytest.fixture
def get_clubs():
    def _get_clubs(params=None):
        response = requests.get(CLUBS_ENDPOINT, params=params)
        return response

    return _get_clubs
