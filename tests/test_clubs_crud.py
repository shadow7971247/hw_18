import allure
import uuid
from jsonschema import validate

from tests.schemas.club_schema import create_club_schema


def club_payload(*, title: str, authors: str, year: int, description: str, tg_link: str):
    return {
        "bookTitle": title,
        "bookAuthors": authors,
        "publicationYear": year,
        "description": description,
        "telegramChatLink": tg_link,
    }


@allure.feature("Club API")
@allure.story("CRUD - Создание клуба")
def test_create_club(create_club):
    unique_id = uuid.uuid4().hex[:8]
    data = club_payload(
        title=f"Test Book {unique_id}",
        authors="Test Author",
        year=2024,
        description="Test description",
        tg_link="https://t.me/qa.guru",
    )
    response = create_club(data)

    assert response.status_code == 201
    body = response.json()
    validate(instance=body, schema=create_club_schema)
    assert body["bookTitle"] == data["bookTitle"]
    assert body["bookAuthors"] == data["bookAuthors"]


@allure.feature("Club API")
@allure.story("CRUD - Просмотр клуба")
def test_get_club_by_id(club_api):
    response = club_api.get_clubs()
    body = response.json()
    assert body["count"] > 0

    club_id = body["results"][0]["id"]
    response = club_api.get_club_by_id(club_id)

    assert response.status_code == 200
    validate(instance=response.json(), schema=create_club_schema)


@allure.feature("Club API")
@allure.story("CRUD - Редактирование клуба (PUT)")
def test_update_club(create_club, club_api, auth_token):
    unique_id = uuid.uuid4().hex[:8]
    data = club_payload(
        title=f"Original Title {unique_id}",
        authors="Original Author",
        year=2023,
        description="Original description",
        tg_link="https://t.me/qa.guru",
    )
    club = create_club(data).json()

    updated_data = club_payload(
        title=f"Updated Title {unique_id}",
        authors="Updated Author",
        year=2025,
        description="Updated description",
        tg_link="https://t.me/qa.guru",
    )
    response = club_api.update_club(club["id"], updated_data, auth_token)

    assert response.status_code == 200
    body = response.json()
    assert body["bookTitle"] == updated_data["bookTitle"]
    assert body["bookAuthors"] == updated_data["bookAuthors"]
    assert body["modified"] is not None


@allure.feature("Club API")
@allure.story("CRUD - Редактирование клуба (PATCH)")
def test_patch_club(create_club, club_api, auth_token):
    unique_id = uuid.uuid4().hex[:8]
    data = club_payload(
        title=f"Patch Test {unique_id}",
        authors="Patch Author",
        year=2022,
        description="Patch description",
        tg_link="https://t.me/qa.guru",
    )
    club = create_club(data).json()

    new_title = f"Patched Title {unique_id}"
    response = club_api.patch_club(club["id"], {"bookTitle": new_title}, auth_token)

    assert response.status_code == 200
    body = response.json()
    assert body["bookTitle"] == new_title
    assert body["bookAuthors"] == club["bookAuthors"]


@allure.feature("Club API")
@allure.story("CRUD - Удаление клуба")
def test_delete_club(create_club, club_api, auth_token):
    unique_id = uuid.uuid4().hex[:8]
    data = club_payload(
        title=f"Delete Test {unique_id}",
        authors="Delete Author",
        year=2021,
        description="Delete description",
        tg_link="https://t.me/qa.guru",
    )
    club = create_club(data).json()

    response = club_api.delete_club(club["id"], auth_token)
    assert response.status_code == 204

    get_response = club_api.get_club_by_id(club["id"])
    assert get_response.status_code == 404


@allure.feature("Club API")
@allure.story("CRUD - Негативные тесты")
def test_delete_club_without_token(create_club, club_api):
    unique_id = uuid.uuid4().hex[:8]
    data = club_payload(
        title=f"No Token Test {unique_id}",
        authors="No Token Author",
        year=2020,
        description="No token description",
        tg_link="https://t.me/qa.guru",
    )
    club = create_club(data).json()

    response = club_api.delete_club(club["id"])
    assert response.status_code == 401