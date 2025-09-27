
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime, UTC

@dataclass
class Guia:
    id: Optional[int] = field(default=None)
    filial: str
    cnpj: str
    ie: str
    uf: str
    periodo: datetime
    vencimento: datetime
    tipo: str
    valor: str
    fcp: str
    site: str
    notas: list[str]
    fretes: list[str]
    created_at: datetime = field(default_factory=datetime.now(UTC))
