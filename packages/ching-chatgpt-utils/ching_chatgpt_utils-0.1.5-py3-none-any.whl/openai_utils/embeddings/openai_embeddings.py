import requests
from pydantic import BaseModel
from typing import Union, List
from .base import Embedder

class OpenAIEmbeddingConfig(BaseModel):
    api_key: str
    model: str

class OpenAIAPIEmbedder(Embedder):
    def __init__(self, config: dict):
        self.config = OpenAIEmbeddingConfig(**config)

    def embed(self, texts: Union[List, str]):
        HEADERS = {"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"}
        URL = "https://api.openai.com/v1/embeddings"
        response = requests.post(URL, headers=HEADERS, json={"input": texts, "model":self.config.model, "encoding_format": "float"}).json()
        embeddings = list(map(lambda element:element['embedding'], response['data']))
        if isinstance(texts, str):
            return embeddings[0]
        return embeddings
    