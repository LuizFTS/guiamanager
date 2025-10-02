from abc import ABC, abstractmethod
from domain.entities.certificado import Certificado
from typing import List, Optional

class ICertificadoRepository(ABC):
    @abstractmethod
    def save(self, certificado: Certificado) -> bool:
        # Salvar uma site no repositório.
        pass

    @abstractmethod
    def delete(self, loja_id: int) -> bool:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def update(self, loja_id: int) -> bool:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Certificado]:
        # Retorna uma site pelo ID ou None.
        pass

    @abstractmethod
    def get_by_loja_id(self, loja_id: int) -> Optional[Certificado]:
        # Retorna uma site pelo ID ou None.
        pass
    

    @abstractmethod
    def list_all(self) -> List[Certificado]:
        # Retorna todas as sites.
        pass