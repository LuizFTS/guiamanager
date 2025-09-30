from domain.entities.guia import Guia

from datetime import datetime
import pandas as pd

class ExcelService:

    def _split_values(self, value):
        """Recebe string de notas/fretes e retorna lista limpa."""
        if pd.isna(value):  # verifica se é NaN
            return []
        return [v.strip() for v in str(value).split(",") if v.strip()]
    
    def _parse_datetime(self, value: str) -> datetime:
        """Converte string de data em datetime, assumindo formato padrão."""
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def read(self, path: str):
        """Lê uma planilha Excel e retorna uma lista de objetos Guia."""
        df = pd.read_excel(path)
        guias: list[Guia] = []

        for row in df.itertuples(index=False):
            filial = str(row.FILIAL).zfill(2)
            tipo = str(row.TIPO)

            notas = []
            fretes = []
            if tipo in ("DIFAL", "ST", "ICAN"):
                notas = self._split_values(getattr(row, "NOTAS", None)) if tipo in ("DIFAL", "ST", "ICAN") else []
                fretes = self._split_values(getattr(row, "FRETES", None)) if tipo in ("DIFAL", "ST") else []


            guia = Guia(
                filial=filial,
                cnpj="",
                ie="",
                uf="",
                loja_id="",
                site_id="",
                periodo=self._parse_datetime(str(row.PERIODO)),
                vencimento=self._parse_datetime(str(row.VENCIMENTO)),
                tipo=tipo,
                valor=f"{float(row.VALOR):.2f}",
                fcp=f"{float(row.FCP):.2f}",
                site="",
                notas=notas,
                fretes=fretes
            )
            guias.append(guia)

        return guias