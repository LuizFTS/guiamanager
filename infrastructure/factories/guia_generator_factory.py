from domain.services.i_guia_generator_service import IGuiaGeneratorService

from infrastructure.services.playwright.ba_playwright import GuiaGeneratorBAPlayWright
from infrastructure.services.playwright.ma_playwright import GuiaGeneratorMAPlayWright

class GuiaGeneratorFactory:
    @staticmethod
    def create(uf: str) -> IGuiaGeneratorService:
        uf = uf.upper()
        if uf == "BA":
            return GuiaGeneratorBAPlayWright()
        elif uf == "MA":
            return GuiaGeneratorMAPlayWright()
        
        raise ValueError(f"Não há serviço de geração para {uf}.")