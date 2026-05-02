from jsonschema import validate
from tests.schemas.clubs_schema import clubs_schema


def test_get_clubs_status_code(get_clubs):
    response = get_clubs()
    assert response.status_code == 200


def test_get_clubs_schema_validation(get_clubs):
    response = get_clubs()
    validate(instance=response.json(), schema=clubs_schema)


def test_get_clubs_structure(get_clubs):
    body = get_clubs().json()
    assert "count" in body
    assert "next" in body
    assert "previous" in body
    assert "results" in body
    assert isinstance(body["count"], int)
    assert isinstance(body["results"], list)


def test_get_clubs_pagination(get_clubs):
    response = get_clubs(params={"page": 1, "page_size": 2})
    body = response.json()
    assert len(body["results"]) <= 2


def test_get_clubs_search(get_clubs):
    search_term = "Толстой"
    response = get_clubs(params={"search": search_term})
    body = response.json()
    validate(instance=body, schema=clubs_schema)

    if body["count"] > 0:
        for club in body["results"]:
            assert (
                search_term.lower() in club["bookTitle"].lower()
                or search_term.lower() in club["bookAuthors"].lower()
            )


def test_get_clubs_verify_club_fields(get_clubs):
    body = get_clubs().json()
    if body["count"] > 0:
        first_club = body["results"][0]
        required_fields = ["id", "bookTitle", "owner", "members", "created", "modified"]
        for field in required_fields:
            assert field in first_club, f"Поле '{field}' отсутствует в клубе"


def test_get_clubs_has_results(get_clubs):
    body = get_clubs().json()
    assert body["count"] >= 0
    if body["count"] > 0:
        assert len(body["results"]) > 0
