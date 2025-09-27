from abc import ABC, abstractmethod
from domain.entities.guia import Guia

class IGuiaGeneratorService:
    @abstractmethod
    def gerar(self, guia: Guia) -> str:
        """ 
        Gera a guia e retorna o path do PDF salvo.
        Pode levantar DomainError em caso de falha.
        """
        raise NotImplementedError