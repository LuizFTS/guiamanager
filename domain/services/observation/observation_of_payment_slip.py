from domain.exceptions.domain_error import DomainError

class ObservationOfPaymentSlipService:

    @classmethod
    def generate_text(cls, tipo: str, periodo: str, uf: str, notas: list[str], fretes: list[str]) -> str:
        tipo_map = {
            "DIFAL": "diferencial de alíquotas",
            "ST": "substituição tributária",
            "ICMS": "ICMS apurado",
            "ICAU": "ICMS dos fretes autônomos apurado",
            "ICAN": "ICMS antecipado apurado",
            "FOT": "FOT apurado"
        }

        if tipo not in tipo_map:
            raise DomainError("Tipo de guia inválido para observação.")

        # Casos especiais
        if tipo in ("DIFAL", "ST") and uf == "BA":
            return f"Referente ao {tipo_map[tipo]} do período {periodo}."

        if tipo in ("ICMS", "ICAU", "ICAN", "FOT"):
            return f"Referente ao {tipo_map[tipo]} no periodo {periodo}."

        # Construção das partes
        partes = []
        if notas:
            prefixo = "nota fiscal" if len(notas) == 1 else "notas fiscais"
            partes.append(f"{prefixo} {', '.join(notas)}")
        if fretes:
            prefixo = "conhecimento de transporte" if len(fretes) == 1 else "conhecimentos de transporte"
            partes.append(f"{prefixo} {', '.join(fretes)}")

        if not partes:
            raise DomainError("Nenhuma observação foi informada.")

        return f"Referente ao {tipo_map[tipo]} das { ' e dos '.join(partes) if len(partes) == 2 else partes[0] } do período {periodo}."
