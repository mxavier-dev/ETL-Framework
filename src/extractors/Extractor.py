from abc import ABC, abstractmethod

class Extrator(ABC):
    @abstractmethod
    def extractor(self, source):
        pass
