from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Guia:
    id: int
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
