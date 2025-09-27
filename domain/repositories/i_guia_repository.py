from abc import ABC, abstractmethod
from domain.entities.guia import Guia
from typing import List, Optional

class IGuiaRepository(ABC):
    @abstractmethod
    def save(self, guia: Guia) -> bool:
        # Salvar uma guia no repositório.
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        # Retorna uma guia pelo ID ou None.
        pass

    @abstractmethod
    def update(self, uf: str) -> bool:
        # Retorna uma guia pelo ID ou None.
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Guia]:
        # Retorna uma guia pelo ID ou None.
        pass

    @abstractmethod
    def get_by_uf(self, uf: str) -> Optional[Guia]:
        # Retorna uma guia pelo ID ou None.
        pass

    @abstractmethod
    def list_all(self) -> List[Guia]:
        # Retorna todas as guias.
        pass