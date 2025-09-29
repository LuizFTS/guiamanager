from domain.exceptions.domain_error import DomainError
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional

@dataclass
class Site:
    uf: str
    icms: str
    difal: str
    st: str
    icau: str
    fot: str
    ican: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: Optional[int] = field(default=None)
    
    def __post_init__(self):
        self._normalize()
        self._validate()
        
    def _normalize(self) -> None:
        self.uf = self.uf.strip().upper()
        self.icms = self.icms.strip()
        self.difal = self.difal.strip()
        self.st = self.st.strip()
        self.icau = self.icau.strip()
        self.fot = self.fot.strip()
        self.ican = self.ican.strip()
        
    def _validate(self) -> None:
        if len(self.uf) != 2:
            raise DomainError("UF deve ter exatamente 2 caracteres.")