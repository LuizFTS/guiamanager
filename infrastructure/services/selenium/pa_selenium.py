from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from infrastructure.utils.selenium_driver import SeleniumDriver
from interface.gui.handlers.exception_handler import ExceptionHandler

from time import sleep

class GuiaGeneratorPASelenium(IGuiaGeneratorService):
    
    def gerar(self, guia: Guia) -> bool:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
        """

        try:
            self.path = guia.path_save
            self.file_name = guia.file_name
            
            self.driver = SeleniumDriver(guia.path_save, headless=False)
            self.driver.driver.get(guia.site)

            tipo = guia.tipo.lower()
            if tipo == "icms":
                self._icms(guia)
            elif tipo == "difal":
                self._difal(guia)
            elif tipo == "st":
                self._st(guia)
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
        except Exception as e:
            ExceptionHandler.handle(e)
            return False
        finally:
            self.driver.quit()
        
    
    def _icms(self, guia: Guia):
        s = self.driver

        s.clicar('//*[@id="select_15"]')
        s.clicar('//*[@id="select_option_21"]')
        s.clicar('//tr[td[@data-label="Receita" and text()="1131-2"]]//td/md-checkbox')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="form"]/md-card[2]/md-card-content/div/div/md-input-container[2]/input', guia.ie)

        s.aguardar_captcha()

        s.clicar('//*[@id="form"]/md-card[2]/md-card-actions/div/button')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[1]/md-input-container/input', guia.periodo)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[1]/md-datepicker/div[1]/input', guia.vencimento)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[2]/md-datepicker/div[1]/input', guia.getPaymentDate)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[3]/input', guia.valor)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/md-input-container/div[1]/textarea', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1.3)
        s.clicar('//*[@id="avancar"]')
        s.clicar('//*[@id="avancar"]/span')
        s.clicar('//*[@id="content"]/div/div/div[1]/async-loader/div/div/button[3]')
        s.clicar('//*[@id="content"]/div/div/div/div[2]/button[2]')

    def _difal(self, guia: Guia):
        s = self.driver

        s.clicar('//*[@id="select_15"]')
        s.clicar('//*[@id="select_option_21"]')
        s.clicar('//tr[td[@data-label="Receita" and text()="1141-0"]]//td/md-checkbox')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="form"]/md-card[2]/md-card-content/div/div/md-input-container[2]/input', guia.ie)

        s.aguardar_captcha()
        
        s.clicar('//*[@id="form"]/md-card[2]/md-card-actions/div/button/span')
        s.clicar('//*[@id="form"]/md-card[2]/md-card-actions/div/button')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[1]/md-input-container/input', guia.periodo)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[1]/md-datepicker/div[1]/input', guia.vencimento)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[2]/md-datepicker/div[1]/input', guia.getPaymentDate)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[3]/input', guia.valor)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/div/md-input-container/input', guia.notas[0] if len(guia.notas) > 0 else guia.fretes[0])
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/md-input-container/div[1]/textarea', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1.3)
        s.clicar('//*[@id="avancar"]')
        s.clicar('//*[@id="avancar"]/span')
        s.clicar('//*[@id="content"]/div/div/div[1]/async-loader/div/div/button[3]')
        s.clicar('//*[@id="content"]/div/div/div/div[2]/button[2]')

    def _antecipacao(self, guia: Guia):
        s = self.driver
        s.clicar('//*[@id="select_15"]')
        s.clicar('//*[@id="select_option_21"]')
        s.clicar('//tr[td[@data-label="Receita" and text()="1173-8"]]//td/md-checkbox')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="form"]/md-card[2]/md-card-content/div/div/md-input-container[2]/input', guia.ie)

        s.aguardar_captcha()

        s.clicar('//*[@id="form"]/md-card[2]/md-card-actions/div/button')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[1]/md-input-container/input', guia.periodo)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[1]/md-datepicker/div[1]/input', guia.vencimento)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[2]/md-datepicker/div[1]/input', guia.getPaymentDate)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[3]/input', guia.valor)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/div/md-input-container/input', guia.notas[0] if len(guia.notas) > 0 else guia.fretes[0])
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/md-input-container/div[1]/textarea', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1.3)
        s.clicar('//*[@id="avancar"]')
        s.clicar('//*[@id="avancar"]/span')
        s.clicar('//*[@id="content"]/div/div/div[1]/async-loader/div/div/button[3]')
        s.clicar('//*[@id="content"]/div/div/div/div[2]/button[2]')

    def _st(self, guia: Guia):
        s = self.driver
        s.clicar('//*[@id="select_15"]')
        s.clicar('//*[@id="select_option_21"]')
        s.clicar('//tr[td[@data-label="Receita" and text()="1146-0"]]//td/md-checkbox')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="form"]/md-card[2]/md-card-content/div/div/md-input-container[2]/input', guia.ie)

        s.aguardar_captcha()

        s.clicar('//*[@id="form"]/md-card[2]/md-card-actions/div/button')
        s.clicar('//*[@id="avancar"]')
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[1]/md-input-container/input', guia.periodo)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[1]/md-datepicker/div[1]/input', guia.vencimento)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[2]/md-datepicker/div[1]/input', guia.getPaymentDate)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[1]/div[2]/md-input-container[3]/input', guia.valor)
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/div/md-input-container/input', guia.notas[0] if len(guia.notas) > 0 else guia.fretes[0])
        s.digitar('//*[@id="content"]/div/div/div/form/async-loader/div/md-card/md-card-content/div[2]/md-input-container/div[1]/textarea', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1.3)
        s.clicar('//*[@id="avancar"]')
        s.clicar('//*[@id="avancar"]/span')
        s.clicar('//*[@id="content"]/div/div/div[1]/async-loader/div/div/button[3]')
        s.clicar('//*[@id="content"]/div/div/div/div[2]/button[2]')
