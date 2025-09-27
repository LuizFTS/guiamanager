from domain.entities.site import Site
from domain.exceptions.domain_error import DomainError

from typing import Optional

from dataclasses import dataclass, field
from datetime import datetime, UTC

@dataclass
class Loja:
    id: Optional[int] = field(default=None)
    filial: str
    uf: str
    cnpj: str
    ie: str
    site: Site
    created_at: datetime = field(default_factory=datetime.now(UTC))
    
    def __post_init__(self):
        self._normalize()
        self._validate()
        
    def _normalize(self) -> None:
        self.filial = self.filial.strip()
        self.cnpj = self.cnpj.strip()
        self.ie = self.ie.strip()
        self.uf = self.uf.strip().upper()
        
    def _validate(self) -> None:
        if not all([self.filial, self.cnpj, self.ie, self.uf]):
            raise DomainError("Todos os campos da loja são obrigatórios.")
        
        if len(self.cnpj) != 14 or not self.cnpj.isdigit():
            raise DomainError("CNPJ deve ter exatamente 14 dígitos numéricos.")
        
        if len(self.uf) != 2:
            raise DomainError("UF deve ter exatamente 2 caracteres.")
        
        if len(self.ie) < 2 or not self.ie.isdigit():
            raise DomainError("Inscrição Estadual inválida.")