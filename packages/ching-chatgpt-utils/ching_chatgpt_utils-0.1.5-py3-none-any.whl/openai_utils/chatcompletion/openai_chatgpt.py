"""
A wrapper for openai.ChatCompletion
"""
import openai
from pydantic import BaseModel
from .base import ChatGPT


"""
Store your configurations in a YAML file. 
The structure of the YAML file must follow this Config class.
All attributes must be openai valid
"""
class OpenAIChatGPTConfig(BaseModel):
    api_key: str
    model: str
    parameters: dict = {}
    instructions: str = None

class OpenAIChatGPT(ChatGPT):
    def __init__(self, config):
        self.config = OpenAIChatGPTConfig(**config)

    """
    This essentially calls openai.ChatCompletion 
    """
    def respond(self, messages) -> str:
        self.set_config()
        completion = openai.ChatCompletion.create(
                model = self.config.model, 
                messages = messages,
                **self.config.parameters
            )
        return completion['choices'][0]['message']['content']

    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = "https://api.openai.com/v1"
        openai.api_version = ""
        openai.api_type = "open_ai"
    