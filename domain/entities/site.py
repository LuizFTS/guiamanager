from dataclasses import dataclass, field
import uuid

@dataclass
class Site:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    uf: str
    icms: str
    difal: str
    st: str
    icau: str
    fot: str
    ican: str