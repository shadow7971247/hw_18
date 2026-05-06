import pytest
from api.clubs_api import ClubsAPI

BASE_URL = "https://book-club.qa.guru"


@pytest.fixture
def clubs_api():
    return ClubsAPI(BASE_URL)