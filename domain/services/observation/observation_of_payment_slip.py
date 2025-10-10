from domain.exceptions.domain_error import DomainError

class ObservationOfPaymentSlipService:

    @classmethod
    def generate_text(cls, tipo: str, periodo: str, uf: str, notas: list[str], fretes: list[str]) -> str:
        tipo_map = {
            "DIFAL": "diferencial de aliquotas",
            "ST": "substituicao tributaria",
            "ICMS": "ICMS apurado",
            "ICAU": "ICMS dos fretes autonomos apurado",
            "ICAN": "ICMS antecipado apurado",
            "FOT": "FOT apurado"
        }

        tipo_genero = {
            "DIFAL": "o",
            "ST": "a",
            "ICMS": "o",
            "ICAU": "o",
            "ICAN": "o",
            "FOT": "o"
        }

        if tipo not in tipo_map:
            raise DomainError("Tipo de guia inválido para observação.")

        # Casos especiais
        if tipo in ("DIFAL",) and uf == "BA":
            return f"Referente ao {tipo_map[tipo]} do periodo {periodo}."
        if tipo in ("ST",) and uf == "BA":
            return f"Referente a {tipo_map[tipo]} do periodo {periodo}."
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
            raise DomainError("Nenhuma observacao foi informada.")
        
        # Função para escolher artigo correto baseado na primeira palavra de cada parte
        def artigo_para_parte(parte: str) -> str:
            if parte.startswith("nota fiscal"):
                return "da"
            if parte.startswith("notas fiscais"):
                return "das"
            if parte.startswith("conhecimento de transporte"):
                return "do"
            if parte.startswith("conhecimentos de transporte"):
                return "dos"
            return "do"

        # Define artigo das partes
        if len(partes) == 2:
            # plural, unir com 'e'
            texto_partes = f"{partes[0]} e {partes[1]}"
            artigo_partes = artigo_para_parte(partes[0])
        else:
            texto_partes = partes[0]
            artigo_partes = artigo_para_parte(partes[0])

        # Artigo do tipo
        artigo_tipo = "a" if tipo_genero[tipo] == "a" else "ao"

        return f"Referente {artigo_tipo} {tipo_map[tipo]} {artigo_partes} {texto_partes} do periodo {periodo}."
