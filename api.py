import requests
from typing import Dict, List


class SessionBase:
    def __init__(self, base_url: str, token: str, secret: str = None):
        self.base_url = base_url
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {token}",
        }
        if secret:
            self.headers["X-Secret"] = secret
        self._session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._session.close()

    def _get(self, path, params):
        response = self._session.get(url=self.base_url + path, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def _post(self, path, data):
        response = self._session.post(url=self.base_url + path, json=data, headers=self.headers)
        if response.status_code == 200:
            return response.json()


class Cleaner(SessionBase):
    BASE_URL = 'https://cleaner.dadata.ru/api/v1/'

    def __init__(self, token: str, secret: str = None):
        super().__init__(base_url=self.BASE_URL, token=token, secret=secret)

    def clean(self, entity_name: str, entity_source: str) -> List[Dict]:
        path = f'clean/{entity_name}'
        return self._post(path=path, data=[entity_source])


class Suggester(SessionBase):
    BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/"

    def __init__(self, token: str, secret: str = None):
        super().__init__(base_url=self.BASE_URL, token=token, secret=secret)

    def suggest(self, entity_name: str, query: str, **kwargs) -> Dict:
        path = f"suggest/{entity_name}"
        data = {'query': query}
        data.update(kwargs)
        response = self._post(path=path, data=data)
        return response if response else None

