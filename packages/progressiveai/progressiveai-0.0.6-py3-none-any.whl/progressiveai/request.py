import requests
from .exceptions import APIError


class Chat:
    def __init__(self, api_key, text, model):
        self.api_key = api_key
        self.text = text
        self.model = model
        self.session = requests.Session()

    def get_response(self):
        params = {
            'api_key': self.api_key,
            'prompt': self.text,
        }
        response = self.session.get(
            f'https://api.progressiveai.org/v1/{self.model}', params=params)
        try:
            data = response.json()
        except Exception as e:
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            raise
        if 'error' in data:
            raise APIError(data['error'])
        return data['response']
