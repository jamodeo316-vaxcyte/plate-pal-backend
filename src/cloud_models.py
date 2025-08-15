import os
from openai import AzureOpenAI


API_VERSION = os.getenv("API_VERSION")
ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_KEY = os.getenv("AZURE_API_KEY")


class AzureModel:
    def __init__(self, model, temp=0.0, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
        self.client = AzureOpenAI(api_version=API_VERSION, azure_endpoint=ENDPOINT, api_key=API_KEY)
        self.chat_args = {
            "model": model,
            "temperature": temp,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "max_completion_tokens": 16384,
        }    
    def get_response(self, messages):
        response = self.client.chat.completions.create(messages=messages, **self.chat_args)
        return response.choices[0].message.content
