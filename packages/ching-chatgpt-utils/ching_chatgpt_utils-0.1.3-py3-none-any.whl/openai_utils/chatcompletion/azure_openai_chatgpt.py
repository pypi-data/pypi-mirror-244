"""
A wrapper for openai.ChatCompletion
"""
import openai
from pydantic import BaseModel
from .base import ChatGPT


class AzureOpenAIChatGPTConfig(BaseModel):
    api_key: str
    api_base: str
    api_version: str
    engine: str

class AzureOpenAIChatGPT(ChatGPT):

    def __init__(self, config):
        self.config = AzureOpenAIChatGPTConfig(**config)

    def respond(self, messages, **arguments):
        self.set_config()
        completion = openai.ChatCompletion.create(
                engine = self.config.engine, 
                messages = messages,
                **arguments
            )
        return completion['choices'][0]['message']['content']


    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = self.config.api_base
        openai.api_version = self.config.api_version
        openai.api_type = "azure"
    