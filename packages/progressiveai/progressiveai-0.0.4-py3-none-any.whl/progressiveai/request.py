import requests


class Chat:
    def __init__(self, api_key, text, model):
        self.api_key = api_key
        self.text = text
        self.model = model
        # self.temperature = 0.7
        # self.max_tokens = 50
        self.session = requests.Session()  # Create a Session object

    def get_response(self):
        params = {
            'api_key': self.api_key,
            'prompt': self.text,
            # 'temperature': self.temperature,
            # 'max_tokens': self.max_tokens
        }
        response = self.session.get(  # Use session.get instead of requests.get
            f'https://api.progressiveai.org/v1/{self.model}', params=params)
        try:
            data = response.json()
        except Exception as e:
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            raise
        if 'error' in data:
            raise Exception(data['error'])
        return data['response']
