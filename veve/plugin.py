from abc import ABC, abstractmethod


class Plugin(ABC):

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def setup(self, args):
        pass

    @abstractmethod
    def run(self, credentials):
        pass

    @abstractmethod
    def options(self, parser):
        pass
