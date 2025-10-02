
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime, UTC
import os
import calendar
import locale

@dataclass
class Guia:
    filial: str
    loja_id: int
    site_id: int
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
    def tipo_arquivo(self) -> str:
        tipo_map = {
            "ICMS": "ICMS",
            "DIFAL": "DIFE",
            "ST": "ICST",
            "ICAN": "ICAN",
            "ICAU": "ICAU",
            "FOT": "FOT"
        }
        return tipo_map.get(self.tipo, "DESCONHECIDO")

    @property
    def path_save(self) -> str:
        """
        Retorna o caminho onde o PDF da guia deve ser salvo
        """
        if isinstance(self.periodo, datetime):
            year = str(self.periodo.year)
            month = str(self.periodo.month).zfill(2)
        else:
            dt = datetime.strptime(str(self.periodo), "%m/%Y")
            year = str(dt.year)
            month = str(dt.month).zfill(2)

        path_to_save = os.path.join(
            #r"C:\Users\lu9887091\Nutrien\Tax Brasil - TAX - Indiretos Litigation e Outros\Fechamentos e outros por empresa\Fechamento CDA & CASAL\Escrita Fiscal\Guias pagas",
            r"C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta\GETVALUES\Guias pagas",
            f"Loja {self.filial}",
            year,
            self.tipo_destino,
            f"{month}-{year}"
        )
        return path_to_save

    @property
    def file_name(self) -> str:
        """
        Retorna o nome do arquivo PDF da guia
        """
        if isinstance(self.periodo, datetime):
            year = str(self.periodo.year)
            month = str(self.periodo.month).zfill(2)
        else:
            dt = datetime.strptime(str(self.periodo), "%m/%Y")
            year = str(dt.year)
            month = str(dt.month).zfill(2)

        file_name = f"Lj{self.filial}_{self.tipo_arquivo}_{month}{year}.pdf"


        path = self.path_save
        base, ext = os.path.splitext(file_name)
        counter = 1
        new_filename = file_name

        while os.path.exists(os.path.join(path, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1

        return new_filename
    
    @property
    def get_periodo_month_name(self):
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

        if isinstance(self.periodo, datetime):
            month = self.periodo.month
            return calendar.month_name[month].capitalize()
        else:
            dt = datetime.strptime(str(self.periodo), "%m/%Y")
            month = dt.month
            return calendar.month_name[month].capitalize()
        
    @property
    def get_periodo_year(self):
        if isinstance(self.periodo, datetime):
            year = self.periodo.year
            return year
        else:
            dt = datetime.strptime(str(self.periodo), "%m/%Y")
            year = dt.year
            return year
        
    @property
    def get_full_path(self):
        path = self.path_save
        file = self.file_name
        return os.path.join(path, file)