from abc import ABC, abstractmethod

class ISalary(ABC):
    
    @abstractmethod
    def calculate(self):
        pass