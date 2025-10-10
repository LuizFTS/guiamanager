from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional

@dataclass
class Certificado:
    loja_id: int
    cnpj: str
    filial: str
    cert_path: str
    key_path: str
    updated_at: datetime
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: Optional[int] = field(default=None)
    
    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()
