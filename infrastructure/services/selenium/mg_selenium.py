from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from infrastructure.utils.selenium_driver import SeleniumDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GuiaGeneratorMGSelenium(IGuiaGeneratorService):

    def gerar(self, guia: Guia) -> str:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
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


    # ==========================
    # Funções de geração
    # ==========================
    def _icms(self, guia: Guia):
        s = self.driver

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/input', "ICMS APURADO NO PERIODO")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/div[2]/span[text()="ICMS APURADO NO PERIODO"]')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[3]/tbody/tr/td/a')

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[2]/input', f"{guia.ie}")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[3]/a')

        s.clicar('//*[@id="divReceita"]/div/input')
        s.clicar('//*[@id="divReceita"]/div/div[2]/span[10]')

        s.digitar('//*[@id="dtVencimento"]', guia.vencimento)
        s.digitar('//*[@id="dtPagamento"]', guia.vencimento)

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/input')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/div[2]/span[2]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/div[2]/span[text()="{guia.get_periodo_month_name}"]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/div[2]/span[text()="{guia.get_periodo_year}"]')

        WebDriverWait(s.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input'))
        )

        s.digitar('//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input', guia.valor)
        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[12]/td[2]/textarea', 
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[5]/tbody/tr/td[1]/a')
        s.clicar('//*[@id="formasPagamento"]/div[6]/button/a')

    def _difal(self, guia: Guia):
        s = self.driver

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/input', "ICMS OUTROS")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/div[2]/span[text()="ICMS OUTROS"]')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[3]/tbody/tr/td/a')

        s.clicar('//*[@id="divTipoIdentificacao"]/div/input')
        s.clicar('//*[@id="divTipoIdentificacao"]/div/div[2]/span[text()="Inscrição Estadual"]')

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[2]/input', f"{guia.ie}")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[3]/a')

        s.clicar('//*[@id="divReceita"]/div/input')
        s.clicar('//*[@id="divReceita"]/div/div[2]/span[text()="0317-8 - ICMS DIFERENCA DE ALIQUOTA"]')

        s.digitar('//*[@id="dtVencimento"]', guia.vencimento)
        s.digitar('//*[@id="dtPagamento"]', guia.vencimento)

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/input')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/div[2]/span[2]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/div[2]/span[text()="{guia.get_periodo_month_name}"]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/div[2]/span[text()="{guia.get_periodo_year}"]')

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[10]/td[2]/input', guia.notas[0] if len(guia.notas) > 0 else guia.fretes[0])

        WebDriverWait(s.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input'))
        )

        s.digitar('//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input', guia.valor)
        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[12]/td[2]/textarea', 
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[5]/tbody/tr/td[1]/a')
        s.clicar('//*[@id="formasPagamento"]/div[6]/button/a')

    def _st(self, guia: Guia):
        s = self.driver

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/input', "ICMS SUBSTITUICAO TRIBUTARIA")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[2]/td[2]/div/div[2]/span[text()="ICMS SUBSTITUICAO TRIBUTARIA"]')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[3]/tbody/tr/td/a')

        s.clicar('//*[@id="divTipoIdentificacao"]/div/input')
        s.clicar('//*[@id="divTipoIdentificacao"]/div/div[2]/span[text()="Inscrição Estadual"]')

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[2]/input', f"{guia.ie}")
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[2]/tbody/tr[3]/td[3]/a')

        s.clicar('//*[@id="divReceita"]/div/input')
        s.clicar('//*[@id="divReceita"]/div/div[2]/span[text()="0313-7 - ICMS ST RECOLHIMENTO ANTECIPADO"]')

        s.digitar('//*[@id="dtVencimento"]', guia.vencimento)
        s.digitar('//*[@id="dtPagamento"]', guia.vencimento)

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/input')
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[6]/td[3]/div/div[2]/span[2]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[7]/td[2]/div/div[2]/span[text()="{guia.get_periodo_month_name}"]')

        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/input')
        s.clicar(f'//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[8]/td[2]/div/div[2]/span[text()="{guia.get_periodo_year}"]')

        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[10]/td[2]/input', guia.notas[0] if len(guia.notas) > 0 else guia.fretes[0])

        WebDriverWait(s.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input'))
        )

        s.digitar('//*[@id="divMultaJurosCalcular"]/table/tbody/tr[1]/td[2]/input', guia.valor)
        s.digitar('//*[@id="containerConteudoPrincipal"]/div/form/table[4]/tbody/tr[12]/td[2]/textarea', 
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="containerConteudoPrincipal"]/div/form/table[5]/tbody/tr/td[1]/a')
        s.clicar('//*[@id="formasPagamento"]/div[6]/button/a')