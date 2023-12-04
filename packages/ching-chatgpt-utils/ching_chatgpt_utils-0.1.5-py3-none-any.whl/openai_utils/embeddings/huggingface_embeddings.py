"""
Wrapper for Huggingface feature-extraction
"""
import requests
from pydantic import BaseModel
from typing import Union, List
from .base import Embedder

class HuggingFaceEmbeddingConfig(BaseModel):
    api_key: str
    model: str

class HuggingFaceAPIEmbedder(Embedder):
    def __init__(self, config: dict):
        self.config = HuggingFaceEmbeddingConfig(**config)

    def embed(self, texts: Union[List, str]):
        HF_EMBEDDING_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.config.model}"
        HEADERS = {"Authorization": f"Bearer {self.config.api_key}"}
        response = requests.post(HF_EMBEDDING_API_URL, headers=HEADERS, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()
