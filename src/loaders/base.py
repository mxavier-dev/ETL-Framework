from abc import ABC, abstractmethod

class Loader(ABC):
    @abstractmethod
    def loader(self, data, destination):
        pass
