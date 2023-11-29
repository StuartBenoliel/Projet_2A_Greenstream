from abc import ABC, abstractmethod

class AbstractTable(ABC):
    """
    Cette classe fournit des services pour intéragir avec différentes tables de la base de données.
    """
    @abstractmethod
    def voir(self, *args, **kwargs):
        pass
            
    @abstractmethod
    def supprimer(self, *args, **kwargs):
        pass
