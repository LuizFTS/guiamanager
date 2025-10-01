from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from infrastructure.utils.selenium_driver import SeleniumDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep


class GuiaGeneratorMASelenium(IGuiaGeneratorService):

    def gerar(self, guia: Guia) -> bool:
        """
        Gera a guia do estado da MA de acordo com o tipo.
        Retorna o bool caso o PDF foi gerado.
        """
        self.path = guia.path_save
        self.file_name = guia.file_name
        
        self.driver = SeleniumDriver(guia.path_save, headless=True)
        self.driver.driver.get(guia.site)

        tipo = guia.tipo.lower()
        if tipo == "icms":
            self._icms(guia)
        elif tipo == "difal":
            self._difal(guia)
        elif tipo == "ican":
            self._antecipacao(guia)
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

        # Espera a frame estar disponível e troca o contexto
        WebDriverWait(s.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mainFrame"))

        s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie)
        s.clicar('//*[@id="form1:buscarIe"]')
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoTipoDare"]', "1")
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoReceita"]', "101")
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo)
        self._wait_loading_spin_disapear()
        s.digitar_blur('//*[@id="form1:valorPrincipal"]', guia.valor)
        self._wait_loading_spin_disapear()
        s.clicar('//*[@id="form1:cmdAdicionarDocumento"]')
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="form1:cmdEmitir"]')

    def _difal(self, guia: Guia):
        s = self.driver

        # Espera a frame estar disponível e troca o contexto
        WebDriverWait(s.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mainFrame"))

        s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie)
        s.clicar('//*[@id="form1:buscarIe"]')
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoTipoDare"]', "1")
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoReceita"]', "101")
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo)
        self._wait_loading_spin_disapear()
        s.digitar_blur('//*[@id="form1:valorPrincipal"]', guia.valor)
        self._wait_loading_spin_disapear()
        s.clicar('//*[@id="form1:cmdAdicionarDocumento"]')
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="form1:cmdEmitir"]')

    def _antecipacao(self, guia: Guia):
        s = self.driver

        # Espera a frame estar disponível e troca o contexto
        WebDriverWait(s.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mainFrame"))

        s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie)
        s.clicar('//*[@id="form1:buscarIe"]')
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoTipoDare"]', "1")
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoReceita"]', "101")
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo)
        self._wait_loading_spin_disapear()
        s.digitar_blur('//*[@id="form1:valorPrincipal"]', guia.valor)
        self._wait_loading_spin_disapear()
        s.clicar('//*[@id="form1:cmdAdicionarDocumento"]')
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="form1:cmdEmitir"]')


    def _wait_loading_spin_disapear(self):
        sleep(0.3)
        WebDriverWait(self.driver.driver, 10, 0.5).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="form1:j_id5:status.start"]/img'))
        )