from abc import ABCMeta, abstractmethod

class Command(metaclass=ABCMeta):
    def _init__(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass
