from abc import ABC, abstractmethod
from domain.entities.loja import Loja
from typing import List, Optional

class ILojaRepository(ABC):
    @abstractmethod
    def save(self, loja: Loja, site_id: int) -> bool:
        # Salvar uma loja no repositório.
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        # Retorna uma loja pelo ID ou None.
        pass

    @abstractmethod
    def update(self, filial: str, site_id: int) -> bool:
        # Retorna uma loja pelo ID ou None.
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Loja]:
        # Retorna uma loja pelo ID ou None.
        pass

    @abstractmethod
    def get_by_filial(self, filial: str) -> Optional[Loja]:
        # Retorna uma loja pelo ID ou None.
        pass

    @abstractmethod
    def list_all(self) -> List[Loja]:
        # Retorna todas as lojas.
        pass