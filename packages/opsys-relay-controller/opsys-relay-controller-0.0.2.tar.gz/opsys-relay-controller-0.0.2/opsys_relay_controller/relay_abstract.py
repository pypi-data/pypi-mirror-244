from abc import ABC, abstractmethod


class RelayAbstract(ABC):  
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def switch_off(self, switch_number: int):
        pass
    
    @abstractmethod
    def switch_on(self, switch_number: int):
        pass
    
    @abstractmethod
    def switch_status(self, switch_number: int):
        pass
    