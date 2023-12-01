from abc import ABC, abstractmethod

class Embedder(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def embed(self):
        pass
