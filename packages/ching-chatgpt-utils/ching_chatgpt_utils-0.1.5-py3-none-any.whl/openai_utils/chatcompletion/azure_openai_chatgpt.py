"""
A wrapper for openai.ChatCompletion and for azure openai. 
"""
import openai
from pydantic import BaseModel
from .base import ChatGPT

"""
Store your configurations in a YAML file. 
The structure of the YAML file must follow this Config class.
All attributes must be openai valid
"""
class AzureOpenAIChatGPTConfig(BaseModel):
    api_key: str
    api_base: str
    api_version: str
    engine: str
    parameters: dict = {}
    instructions: str = None

class AzureOpenAIChatGPT(ChatGPT):

    def __init__(self, config):
        self.config = AzureOpenAIChatGPTConfig(**config)

    """
    This essentially calls openai.ChatCompletion 
    """
    def respond(self, messages) -> str:
        self.set_config()
        completion = openai.ChatCompletion.create(
                engine = self.config.engine, 
                messages = messages,
                **self.config.parameters
            )
        return completion['choices'][0]['message']['content']


    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = self.config.api_base
        openai.api_version = self.config.api_version
        openai.api_type = "azure"
    