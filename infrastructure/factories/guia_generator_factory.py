from domain.services.i_guia_generator_service import IGuiaGeneratorService

from infrastructure.services.selenium.ba_selenium import GuiaGeneratorBASelenium
from infrastructure.services.selenium.ma_selenium import GuiaGeneratorMASelenium
from infrastructure.services.selenium.mg_selenium import GuiaGeneratorMGSelenium
from infrastructure.services.selenium.pa_selenium import GuiaGeneratorPASelenium
from infrastructure.services.selenium.rj_selenium import GuiaGeneratorRJSelenium
from infrastructure.services.selenium.to_selenium import GuiaGeneratorTOSelenium
from infrastructure.services.selenium.sp_selenium import GuiaGeneratorSPSelenium
from infrastructure.services.requests.mt_request import GuiaGeneratorMTRequest
from infrastructure.services.webservice.es_webservice import GuiaGeneratorESWebService

class GuiaGeneratorFactory:
    @staticmethod
    def create(uf: str) -> IGuiaGeneratorService:
        uf = uf.upper()
        if uf == "BA":
            return GuiaGeneratorBASelenium()
        elif uf == "MA":
            return GuiaGeneratorMASelenium()
        elif uf == "MG":
            return GuiaGeneratorMGSelenium()
        elif uf == "PA":
            return GuiaGeneratorPASelenium()
        elif uf == "RJ":
            return GuiaGeneratorRJSelenium()
        elif uf == "TO":
            return GuiaGeneratorTOSelenium()
        elif uf == "ES":
            return GuiaGeneratorESWebService()
        elif uf == "MT":
            return GuiaGeneratorMTRequest()
        elif uf == "SP":
            return GuiaGeneratorSPSelenium()
        
        raise ValueError(f"Não há serviço de geração para {uf}.")