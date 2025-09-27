from domain.services.i_guia_generator_service import IGuiaGeneratorService

from infrastructure.services.selenium.ba_selenium import GuiaGeneratorBASelenium

class GuiaGeneratorFactory:
    @staticmethod
    def create(uf: str) -> IGuiaGeneratorService:
        uf = uf.upper()
        if uf == "BA":
            return GuiaGeneratorBASelenium()
        
        raise ValueError(f"Não há serviço de geração para {uf}.")