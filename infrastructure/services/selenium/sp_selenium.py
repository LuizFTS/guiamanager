from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from infrastructure.utils.selenium_driver import SeleniumDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
from time import sleep

class GuiaGeneratorSPSelenium(IGuiaGeneratorService):
    
    def gerar(self, guia: Guia) -> str:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
        """
        self.path = guia.path_save
        self.file_name = guia.file_name
        
        self.driver = SeleniumDriver(guia.path_save, headless=False)
        self.driver.driver.get(guia.site)

        tipo = guia.tipo.lower()
        if tipo == "icms":
            self._icms(guia)
        elif tipo == "st":
            self._st(guia)
        else:
            raise ValueError(f"Tipo de guia {guia.tipo} não suportado para BA.")

        pdf_saved = self.driver.compare_files_before_and_after_download_pdf_file(self.path, self.file_name)
        if pdf_saved:
            print(f"PDF da loja {guia.filial} salva: {self.file_name}")
            self.driver.quit()
            return True
        else:
            print(f"Erro ao salvar pdf da loja {guia.filial}.")
            self.driver.quit()
            return False
        

    def _icms(self, guia: Guia):
        s = self.driver

        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[1]/div/input[1]', guia.cnpj)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[1]/div/button')
        s.selecionar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[1]/select', '4601', 300)
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[2]/input', guia.periodo)
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[3]/input', guia.vencimento)
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[7]/input', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[8]/input', guia.valor)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[8]/button')
        sleep(1.5)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[11]/button')
        WebDriverWait(s.driver, 10).until(EC.alert_is_present()).accept()


    def _st(self, guia: Guia):
        s = self.driver

        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[1]/div/input[1]', guia.cnpj)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[1]/div/button')
        s.selecionar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[1]/select', '6308')
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[2]/input', guia.periodo)
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[3]/input', guia.vencimento)
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[4]/input', guia.notas[0])
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[7]/input', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[8]/input', guia.valor)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[8]/button')
        sleep(1.5)
        s.clicar('/html/body/div[1]/div[2]/div/main/div[5]/fieldset[6]/div/div[11]/button')
        WebDriverWait(s.driver, 10).until(EC.alert_is_present()).accept()
