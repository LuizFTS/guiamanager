from dataclasses import dataclass, field
from domain.entities.site import Site
import uuid

@dataclass
class Loja:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    filial: str
    uf: str
    cnpj: str
    ie: str
    site: Site