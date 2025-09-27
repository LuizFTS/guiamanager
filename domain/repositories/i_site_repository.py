from abc import ABC, abstractmethod
from domain.entities.site import Site
from typing import List, Optional

class ISiteRepository(ABC):
    @abstractmethod
    def save(self, site: Site) -> bool:
        # Salvar uma site no repositório.
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def update(self, filial: str) -> bool:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Site]:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def get_by_uf(self, uf: str) -> Optional[Site]:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def list_all(self) -> List[Site]:
        # Retorna todas as sites.
        pass