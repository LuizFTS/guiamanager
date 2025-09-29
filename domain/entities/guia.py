
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime, UTC
import os

@dataclass
class Guia:
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
    notas: List[str] = field(default_factory=list)
    fretes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: Optional[int] = field(default=None)

    
    # =========================
    # Propriedades calculadas
    # =========================
    @property
    def tipo_destino(self) -> str:
        tipo_map = {
            "ICMS": "ICMS",
            "DIFAL": "DIFAL ENTRADAS",
            "ST": "S.T",
            "ICAN": "ICMS Antecipado",
            "ICAU": "ICAU",
            "FOT": "FOT"
        }
        return tipo_map.get(self.tipo, "DESCONHECIDO")

    @property
    def path_save(self) -> str:
        """
        Retorna o caminho onde o PDF da guia deve ser salvo
        """
        path_to_save = os.path.join(
            r"C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta\GETVALUES\Guias pagas",
            f"Loja {self.filial}",
            str(self.periodo.year),
            self.tipo_destino,
            f"{str(self.periodo.month).zfill(2)}-{self.periodo.year}"
        )
        return path_to_save

    @property
    def file_name(self) -> str:
        """
        Retorna o nome do arquivo PDF da guia
        """
        return f"Lj{self.filial}_{self.tipo_destino}_{str(self.periodo.month).zfill(2)}{str(self.periodo.year)}.pdf"