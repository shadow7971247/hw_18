import requests


class ClubAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/v1/clubs/"

    @staticmethod
    def _auth_headers(token: str | None):
        return {"Authorization": f"Bearer {token}"} if token else {}

    def get_clubs(self, params=None):
        return requests.get(self.endpoint, params=params)

    def get_club_by_id(self, club_id):
        return requests.get(f"{self.endpoint}{club_id}/")

    def create_club(self, data, token=None):
        return requests.post(self.endpoint, json=data, headers=self._auth_headers(token))

    def update_club(self, club_id, data, token=None):
        return requests.put(
            f"{self.endpoint}{club_id}/",
            json=data,
            headers=self._auth_headers(token),
        )

    def patch_club(self, club_id, data, token=None):
        return requests.patch(
            f"{self.endpoint}{club_id}/",
            json=data,
            headers=self._auth_headers(token),
        )

    def delete_club(self, club_id, token=None):
        return requests.delete(
            f"{self.endpoint}{club_id}/",
            headers=self._auth_headers(token),
        )