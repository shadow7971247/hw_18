import allure
from jsonschema import validate
from tests.schemas.club_schema import clubs_schema


@allure.feature("Club API")
@allure.story("GET /club")
def test_club_data_structure(club_api):
    response = club_api.get_clubs()
    body = response.json()
    validate(instance=body, schema=clubs_schema)


@allure.feature("Club API")
@allure.story("GET /club")
def test_club_verify_fields(club_api):
    body = club_api.get_clubs().json()
    assert body["count"] > 0

    first_club = body["results"][0]
    required_fields = ["id", "bookTitle", "owner", "members", "created"]
    missing_fields = [field for field in required_fields if field not in first_club]
    assert not missing_fields, f"Отсутствуют поля: {missing_fields}"