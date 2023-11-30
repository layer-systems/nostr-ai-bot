import requests

class OllamaApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def call_api(self, data):
        # response = requests.post(self.api_url, json=data)
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     return None
        model = "llama2"
        r = requests.post(self.api_url,
                        json={
                            'model': model,
                            'prompt': data,
                            'context': [],
                            'stream': False,
                        },
                        stream=False)
        return(r.json())
