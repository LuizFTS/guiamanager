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
        
    def gerar(self, guia: Guia) -> str:
        """
        Gera a guia do estado da BA de acordo com o tipo.
        Retorna o bool caso o PDF foi gerado.
        """
        self.path = guia.path_save
        self.file_name = guia.file_name
        
        self.driver = SeleniumDriver(guia.path_save, headless=True)
        self.driver.driver.get(guia.site)


        tipo = guia.tipo.lower()
        if tipo == "icms":
            self._icms(guia)
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

    # ==========================
    # Métodos privados por tipo
    # ==========================
    def _icms(self, guia: Guia):
        s = self.driver
        s.selecionar('//*[@id="PHConteudo_ddl_contribuinte_inscrito"]', "759|campanha")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[1]/div/input', guia.ie)
        self._preencher_datas_valores(s, guia)
        s.digitar('//*[@id="PHconteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo,
                                               guia.uf, guia.notas, guia.fretes))
        s.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        s.driver.close()

    def _antecipacao(self, guia: Guia):
        s = self.driver
        s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "2175|formulario")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[1]/div/input', guia.ie)
        self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = (f'/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[6]/div/input[{i}]')
            s.digitar(input_path, valor)

        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[7]/div/input', str(len(guia.notas)))
        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[8]/div/input',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo,
                                               guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body', Keys.END)
        s.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        s.driver.close()

    def _st(self, guia: Guia):
        s = self.driver
        s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "1145|campanha")
        s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[1]/div/input', guia.ie)
        self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = (f'/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[6]/div/input[{i}]')
            s.digitar(input_path, valor)

        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[7]/div/input', str(len(guia.notas)))
        s.digitar('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[8]/div/input',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo,
                                               guia.uf, guia.notas, guia.fretes))
        s.digitar('/html/body', Keys.END)
        s.driver.execute_script("document.getElementById('PHconteudoSemAjax_btn_visualizar').click()")
        self._salvar_como_pdf(s)
        s.driver.close()

    # ==========================
    # Auxiliares
    # ==========================
    def _preencher_datas_valores(self, s: SeleniumDriver, guia: Guia):
        element_vencimento = s.get_element('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/input')
        s.driver.execute_script(f"""
            arguments[0].value = '{guia.vencimento}';
            arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('blur', {{ bubbles: true }}));
        """, element_vencimento)

        element_pagamento = s.get_element('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[3]/div/div/input')
        s.driver.execute_script(f"""
            arguments[0].value = '{guia.vencimento}';
            arguments[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
            arguments[0].dispatchEvent(new Event('blur', {{ bubbles: true }}));
        """, element_pagamento)
        s.digitar_blur('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[4]/div/input', guia.valor)
        s.digitar_blur('/html/body/form/section/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[5]/div/input', guia.periodo)

    def _salvar_como_pdf(self, s: SeleniumDriver):
        handles_antes = s.driver.window_handles
        s.clicar('//*[@id="PHConteudo_rep_dae_receita_btn_imprimir_0"]')

        while True:
            handles_depois = s.driver.window_handles
            novos = [h for h in handles_depois if h not in handles_antes]
            if novos:
                popup_handle = novos[0]
                break
            sleep(0.5)

        file_path = os.path.join(self.path, self.file_name)
        s.driver.switch_to.window(popup_handle)
        pdf = s.driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(pdf['data']))