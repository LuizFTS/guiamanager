import locale
import base64
import os
from time import sleep
from selenium.webdriver.common.keys import Keys
from domain.entities.guia import Guia
from domain.services.i_guia_generator_service import IGuiaGeneratorService
from infrastructure.utils.selenium_driver import SeleniumDriver
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService

from domain.services.i_guia_generator_service import IGuiaGeneratorService

class GuiaGeneratorBASelenium(IGuiaGeneratorService):
    
    def __init__(self, driver, handler_cls: type[SeleniumDriver], path_to_save: str, file_name: str):
        self.driver = driver
        self.handler_cls = handler_cls(driver)
        self.path = path_to_save
        self.file_name = file_name
    
    def gerar(self, guia: Guia) -> str:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
        """
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        tipo = guia.tipo.lower()
        if tipo == "icms":
            self._icms(guia)
        elif tipo == "st":
            self._st(guia)
        elif tipo == "ican":
            self._antecipacao(guia)
        else:
            raise ValueError(f"Tipo de guia {guia.tipo} não suportado para BA.")

        return os.path.join(self.path, self.file_name)


    # ==========================
    # Métodos privados por tipo
    # ==========================
    def _icms(self, guia: Guia):
        s = self.handler_cls
        s.selecionar('//*[@id="PHConteudo_ddl_contribuinte_inscrito"]', "759|campanha")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('//*[@id="PHconteudoSemAjax_txt_num_inscricao_estad"]', guia.ie)
        self._preencher_datas_valores(s, guia)
        s.digitar('//*[@id="PHconteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"),
                                               guia.uf, guia.notas, guia.fretes))
        self.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        self.driver.close()

    def _antecipacao(self, guia: Guia):
        s = self.selHandler
        s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "2175|formulario")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('//*[@id="PHconteudoSemAjax_txt_num_inscricao_estad"]', guia.ie)
        self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = ('//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal"]'
                          if i == 1 else f'//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal{i}"]')
            s.digitar(input_path, valor)

        s.digitar('//*[@id="PHConteudoSemAjax_txt_qtd_nota_fiscal"]', str(len(guia.notas)))
        s.digitar('//*[@id="PHConteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"),
                                               guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body', Keys.END)
        self.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        self.driver.close()

    def _st(self, guia: Guia):
        s = self.selHandler
        s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "1145|campanha")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('//*[@id="PHconteudoSemAjax_txt_num_inscricao_estad"]', guia.ie)
        self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = ('//*[@id="PHConteudoSemAjax_txt_num_nota_fiscal"]'
                          if i == 1 else f'//*[@id="PHConteudoSemAjax_txt_num_nota_fiscal{i}"]')
            s.digitar(input_path, valor)

        s.digitar('//*[@id="PHConteudoSemAjax_txt_qtd_nota_fiscal"]', str(len(guia.notas)))
        s.digitar('//*[@id="PHConteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"),
                                               guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body', Keys.END)
        self.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        self.driver.close()

    # ==========================
    # Auxiliares
    # ==========================
    def _preencher_datas_valores(self, s: SeleniumDriver, guia: Guia):
        element = s.get_element('//*[@id="PHconteudoSemAjax_txt_dtc_vencimento"]')
        self.driver.execute_script(f"""
            arguments[0].value = '{guia.vencimento.strftime('%d/%m/%Y')}';
            arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('blur', {{ bubbles: true }}));
        """, element)
        s.digitar_blur('//*[@id="PHconteudoSemAjax_txt_dtc_max_pagamento"]', guia.vencimento.strftime("%d%m%Y"))
        s.digitar_blur('//*[@id="PHConteudoSemAjax_txt_val_principal"]', guia.valor)
        s.digitar_blur('//*[@id="PHConteudoSemAjax_txt_mes_ano_referencia_6anos"]', guia.periodo.strftime("%m%Y"))

    def _salvar_como_pdf(self, s: SeleniumDriver):
        handles_antes = self.driver.window_handles
        s.clicar('//*[@id="PHConteudo_rep_dae_receita_btn_imprimir_0"]')

        while True:
            handles_depois = self.driver.window_handles
            novos = [h for h in handles_depois if h not in handles_antes]
            if novos:
                popup_handle = novos[0]
                break
            sleep(0.5)

        file_path = os.path.join(self.path, self.file_name)
        self.driver.switch_to.window(popup_handle)
        pdf = self.driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(pdf['data']))