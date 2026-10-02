from abc import ABC, abstractmethod

class Extrator(ABC):
    @abstractmethod
    def extract(self, source):
        pass
