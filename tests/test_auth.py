import allure
from jsonschema import validate
from tests.schemas.auth_schema import auth_schema, error_schema


@allure.feature("Auth API")
@allure.story("Регистрация и авторизация")
def test_auth_new_user(register_user, login_user, random_user):
    register_user()
    response = login_user(random_user["username"], random_user["password"])

    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()
    assert len(response.json()["access"].split(".")) == 3
    assert len(response.json()["refresh"].split(".")) == 3
    validate(instance=response.json(), schema=auth_schema)


@allure.feature("Auth API")
@allure.story("Регистрация и авторизация")
def test_auth_existing_user(login_user, existing_user):
    response = login_user(existing_user["username"], existing_user["password"])

    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()
    validate(instance=response.json(), schema=auth_schema)


@allure.feature("Auth API")
@allure.story("Негативные тесты")
def test_auth_wrong_password(login_user, existing_user):
    response = login_user(existing_user["username"], "wrong_password")
    assert response.status_code == 401
    assert "detail" in response.json()
    validate(instance=response.json(), schema=error_schema)


@allure.feature("Auth API")
@allure.story("Негативные тесты")
def test_auth_wrong_username(login_user):
    response = login_user("nonexist_user", "some_password")
    assert response.status_code == 401
    assert "detail" in response.json()
    validate(instance=response.json(), schema=error_schema)


@allure.feature("Auth API")
@allure.story("Негативные тесты")
def test_auth_empty_password(login_user, existing_user):
    response = login_user(existing_user["username"], "")
    assert response.status_code == 400
    assert "password" in response.json()


@allure.feature("Auth API")
@allure.story("Негативные тесты")
def test_auth_empty_username(login_user, existing_user):
    response = login_user("", existing_user["password"])
    assert response.status_code == 400
    assert "username" in response.json()


@allure.feature("Auth API")
@allure.story("Негативные тесты")
def test_auth_empty_both_fields(login_user):
    response = login_user("", "")
    assert response.status_code == 400
    assert "username" in response.json()
    assert "password" in response.json()