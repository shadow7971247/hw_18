import requests


class ClubsAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/v1/clubs/"

    def get_clubs(self, params=None):
        return requests.get(self.endpoint, params=params)