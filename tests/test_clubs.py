import allure
from jsonschema import validate
from tests.schemas.clubs_schema import clubs_schema


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_status_code(clubs_api):
    response = clubs_api.get_clubs()
    assert response.status_code == 200


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_schema_validation(clubs_api):
    response = clubs_api.get_clubs()
    validate(instance=response.json(), schema=clubs_schema)


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_structure(clubs_api):
    body = clubs_api.get_clubs().json()
    assert "count" in body
    assert "next" in body
    assert "previous" in body
    assert "results" in body
    assert isinstance(body["count"], int)
    assert isinstance(body["results"], list)


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_pagination(clubs_api):
    response = clubs_api.get_clubs(params={"page": 1, "page_size": 2})
    body = response.json()
    assert 1 <= len(body["results"]) <= 2


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_search(clubs_api):
    all_clubs = clubs_api.get_clubs().json()
    assert all_clubs["count"] > 0, "Нет данных для теста"

    first_club = all_clubs["results"][0]
    search_term = first_club["bookTitle"]

    response = clubs_api.get_clubs(params={"search": search_term})
    body = response.json()
    validate(instance=body, schema=clubs_schema)

    assert body["count"] > 0, f"По search_term '{search_term}' ничего не найдено"

    for club in body["results"]:
        assert (search_term.lower() in club["bookTitle"].lower() or
                search_term.lower() in club["bookAuthors"].lower()), \
            f"Клуб не содержит '{search_term}' в bookTitle или bookAuthors"


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_verify_club_fields(clubs_api):
    body = clubs_api.get_clubs().json()
    assert body["count"] > 0, "Список клубов пуст"

    first_club = body["results"][0]
    required_fields = ["id", "bookTitle", "owner", "members", "created", "modified"]
    missing_fields = [field for field in required_fields if field not in first_club]
    assert len(missing_fields) == 0, f"Отсутствуют поля: {', '.join(missing_fields)}"


@allure.feature("Clubs API")
@allure.story("GET /clubs")
def test_get_clubs_has_results(clubs_api):
    body = clubs_api.get_clubs().json()
    assert body["count"] > 0, "Список клубов пуст"
    assert len(body["results"]) > 0, "Результаты отсутствуют"