from abc import abstractmethod
from domain.entities.guia import Guia

class IReadExcelService:
    @abstractmethod
    def read(self, path: str) -> list[Guia]:
        """ 
        Gera a guia e retorna o path do PDF salvo.
        Pode levantar DomainError em caso de falha.
        """
        raise NotImplementedError