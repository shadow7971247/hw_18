import requests


class AuthAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token_url = f"{base_url}/api/v1/auth/token/"
        self.register_url = f"{base_url}/api/v1/users/register/"

    def register(self, username: str, password: str):
        return requests.post(
            self.register_url,
            json={"username": username, "password": password},
        )

    def login(self, username: str, password: str):
        return requests.post(
            self.token_url,
            json={"username": username, "password": password},
        )