from abc import ABC, abstractmethod

class ChatGPT(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    @abstractmethod
    def set_config(self):
        pass
