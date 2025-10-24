from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from infrastructure.utils.selenium_driver import SeleniumDriver
from interface.gui.handlers.exception_handler import ExceptionHandler

from time import sleep

class GuiaGeneratorRJSelenium(IGuiaGeneratorService):
    
    def gerar(self, guia: Guia) -> bool:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
        """
        try:
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
            elif tipo == 'icau':
                self._icau(guia)
            elif tipo == "fot":
                self._fot(guia)
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

    # ==========================
    # Funções de geração
    # ==========================
    def _icms(self, guia: Guia):
        s = self.driver

        s.selecionar('//*[@id="tipoPagamentoLista"]', "1")
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(1)
        s.digitar('//*[@id="txtDataPagamento"]', guia.getPaymentDate)
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(2)

        s.selecionar('//*[@id="slcNaturezaLista"]', "1")
        sleep(1)
        s.selecionar('//*[@id="slcListaQualificacao"]', '1')
        sleep(1)
        s.digitar('//*[@id="txtCnpjCpf"]', guia.cnpj)
        sleep(1)
        s.clicar('//*[@id="btnConfirmar"]')
        sleep(2.5)

        s.digitar_blur('//*[@id="txtPeriodoReferencia"]', guia.periodo)
        sleep(1)
        s.digitar('//*[@id="txtJustificativa"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1)

        s.digitar('//*[@id="txtIcmsInformado"]', guia.valor)
        sleep(1)
        s.clicar('//*[@id="okIcms"]')
        sleep(2)

        s.digitar('//*[@id="txtFecpInformado"]', guia.fcp)
        s.clicar('//*[@id="okFecp"]')
        sleep(2)

        s.clicar('//*[@id="formulario"]/fieldset[2]/div[3]/input[1]')
        sleep(1)

        s.clicar('//*[@id="boxResumo_botoes2"]/input')
        sleep(1)
        s.clicar('//*[@id="btnGerarDocs"]')

    def _difal(self, guia: Guia):
        s = self.driver
        time_between = 2

        s.selecionar('//*[@id="tipoPagamentoLista"]', "1")
        sleep(time_between)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(time_between)
        s.digitar('//*[@id="txtDataPagamento"]', guia.getPaymentDate)
        sleep(time_between)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(2)

        s.selecionar('//*[@id="slcNaturezaLista"]', "3")
        sleep(time_between)
        s.digitar('//*[@id="txtCnpjCpf"]', guia.cnpj)
        sleep(time_between)
        s.clicar('//*[@id="btnConfirmar"]')
        sleep(2.5)

        s.digitar_blur('//*[@id="txtPeriodoReferencia"]', guia.periodo)
        sleep(time_between)
        s.digitar('//*[@id="txtJustificativa"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(time_between)

        s.digitar('//*[@id="txtIcmsInformado"]', guia.valor)
        sleep(time_between)
        
        s.clicar('//*[@id="okIcms"]')
        sleep(2)

        s.digitar('//*[@id="txtFecpInformado"]', guia.fcp)
        s.clicar('//*[@id="okFecp"]')
        sleep(2)

        s.clicar('//*[@id="formulario"]/fieldset[2]/div[3]/input[1]')
        sleep(time_between)

        s.clicar('//*[@id="boxResumo_botoes2"]/input')
        sleep(time_between)
        s.clicar('//*[@id="btnGerarDocs"]')

    def _st(self, guia: Guia):
        s = self.driver

        s.selecionar('//*[@id="tipoPagamentoLista"]', "1")
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(1)
        s.digitar('//*[@id="txtDataPagamento"]', guia.getPaymentDate)
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(2)

        s.selecionar('//*[@id="slcNaturezaLista"]', "2")
        sleep(1)
        s.selecionar('//*[@id="slcListaProduto"]', "396")
        sleep(1)
        s.digitar('//*[@id="txtCnpjCpf"]', guia.cnpj)
        sleep(1)
        s.clicar('//*[@id="btnConfirmar"]')
        sleep(2.5)

        s.digitar_blur('//*[@id="txtPeriodoReferencia"]', guia.periodo)
        sleep(1)
        s.digitar('//*[@id="txtJustificativa"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1)

        s.digitar('//*[@id="txtIcmsInformado"]', guia.valor)
        sleep(1)
        s.clicar('//*[@id="okIcms"]')
        sleep(2)

        s.digitar('//*[@id="txtFecpInformado"]', guia.fcp)
        s.clicar('//*[@id="okFecp"]')
        sleep(2)

        s.clicar('//*[@id="formulario"]/fieldset[2]/div[3]/input[1]')
        sleep(1)

        s.clicar('//*[@id="boxResumo_botoes2"]/input')
        sleep(1)
        s.clicar('//*[@id="btnGerarDocs"]')

    def _icau(self, guia: Guia):
        s = self.driver

        s.selecionar('//*[@id="tipoPagamentoLista"]', "1")
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(1)
        s.digitar('//*[@id="txtDataPagamento"]', guia.getPaymentDate)
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(2)

        s.selecionar('//*[@id="slcNaturezaLista"]', "1")
        sleep(1)
        s.selecionar('//*[@id="slcListaQualificacao"]', '5')
        sleep(1)
        s.digitar('//*[@id="txtCnpjCpf"]', guia.cnpj)
        sleep(1)
        s.clicar('//*[@id="btnConfirmar"]')
        sleep(2.5)

        s.digitar_blur('//*[@id="txtPeriodoReferencia"]', guia.periodo)
        sleep(1)
        s.digitar('//*[@id="txtJustificativa"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1)

        s.digitar('//*[@id="txtIcmsInformado"]', guia.valor)
        sleep(1)
        s.clicar('//*[@id="okIcms"]')
        sleep(2)

        s.digitar('//*[@id="txtFecpInformado"]', guia.fcp)
        s.clicar('//*[@id="okFecp"]')
        sleep(2)

        s.clicar('//*[@id="formulario"]/fieldset[2]/div[3]/input[1]')
        sleep(1)

        s.clicar('//*[@id="boxResumo_botoes2"]/input')
        sleep(1)
        s.clicar('//*[@id="btnGerarDocs"]')

    def _fot(self, guia: Guia):
        s = self.driver

        s.selecionar('//*[@id="tipoPagamentoLista"]', "1")
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(1)
        s.digitar('//*[@id="txtDataPagamento"]', guia.getPaymentDate)
        sleep(1)
        s.clicar('//*[@id="btnAlterarDataPagamento"]')
        sleep(2)

        s.selecionar('//*[@id="slcNaturezaLista"]', "61")
        sleep(1)
        s.digitar('//*[@id="txtCnpjCpf"]', guia.cnpj)
        sleep(1)
        s.clicar('//*[@id="btnConfirmar"]')
        sleep(2.5)

        s.digitar_blur('//*[@id="txtPeriodoReferencia"]', guia.periodo)
        sleep(1)
        s.digitar('//*[@id="txtJustificativa"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        sleep(1)

        s.digitar('//*[@id="txtIcmsInformado"]', guia.valor)
        sleep(1)
        s.clicar('//*[@id="okIcms"]')
        sleep(2)

        s.clicar('//*[@id="formulario"]/fieldset[2]/div[3]/input[1]')
        sleep(1)

        s.clicar('//*[@id="boxResumo_botoes2"]/input')
        sleep(1)
        s.clicar('//*[@id="btnGerarDocs"]')