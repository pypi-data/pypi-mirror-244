"""
A wrapper for openai.ChatCompletion
"""
import openai
from pydantic import BaseModel
from .base import ChatGPT

class OpenAIChatGPTConfig(BaseModel):
    api_key: str
    model: str

class OpenAIChatGPT(ChatGPT):
    def __init__(self, config):
        self.config = OpenAIChatGPTConfig(**config)

    def respond(self, messages, **arguments):
        self.set_config()
        completion = openai.ChatCompletion.create(
                model = self.config.model, 
                messages = messages,
                **arguments
            )
        return completion['choices'][0]['message']['content']

    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = "https://api.openai.com/v1"
        openai.api_version = ""
        openai.api_type = "open_ai"
    