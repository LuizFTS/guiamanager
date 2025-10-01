from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from domain.entities.guia import Guia
from infrastructure.utils.playwright_driver import PlaywrightDriver

import asyncio
import os
import locale

class GuiaGeneratorMAPlayWright(IGuiaGeneratorService):

    async def gerar(self, guia: Guia) -> str:
        """
        Gera a guia de acordo com o tipo.
        Retorna o path do PDF gerado.
        """
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

        
        driver = PlaywrightDriver()
        await driver.async_init(headless=False)
        await driver.page.goto(guia.site)

        tipo = guia.tipo.lower()
        if tipo == "icms":
            await self._icms(guia, driver)
        elif tipo == "st":
            await self._st(guia, driver)
        elif tipo == "ican":
            await self._antecipacao(guia, driver)
        else:
            raise ValueError(f"Tipo de guia {guia.tipo} não suportado para BA.")

        return os.path.join(guia.path_save, guia.file_name)
    
    
    # ==========================
    # Métodos privados por tipo
    # ==========================
    async def _icms(self, guia: Guia, driver: PlaywrightDriver):
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        s = driver

        # Espera a frame estar disponível e troca o contexto
        await s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie, frame_name="mainFrame")
        await s.clicar('//*[@id="form1:buscarIe"]', frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.selecionar('//*[@id="form1:codigoTipoDare"]', "1", frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.selecionar('//*[@id="form1:codigoReceita"]', "101", frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo.strftime('%m%Y'), frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.digitar_blur('//*[@id="form1:valorPrincipal"]', str(guia.valor).replace('.', ','), frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.clicar('//*[@id="form1:cmdAdicionarDocumento"]', frame_name="mainFrame")
        await self._wait_loading_spin_disapear()
        await s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"), guia.uf, guia.notas, guia.fretes), frame_name="mainFrame")
        await s.clicar('//*[@id="form1:cmdEmitir"]', frame_name="mainFrame")

        await s.waitDownload('//*[@id="form1:cmdEmitir"]', "mainFrame")


    async def _antecipacao(self, guia: Guia, driver: PlaywrightDriver):
        s = driver
        await s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "2175|formulario")
        await s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        await s.digitar('//*[@id="PHconteudoSemAjax_txt_num_inscricao_estad"]', guia.ie)
        await self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = ('//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal"]'
                          if i == 1 else f'//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal{i}"]')
            await s.digitar(input_path, valor)

        await s.digitar('//*[@id="PHConteudoSemAjax_txt_qtd_nota_fiscal"]', str(len(guia.notas)))
        await s.digitar('//*[@id="PHConteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"),
                                               guia.uf, guia.notas, guia.fretes))
        await s.press('/html/body', "End")
        await s.click_js("//*[@id='PHconteudoSemAjax_btn_visualizar']")
        await self._salvar_como_pdf(s, guia)
        await s.close()

    async def _st(self, guia: Guia, driver: PlaywrightDriver):
        s = driver
        await s.selecionar('//*[@id="PHConteudo_ddl_antecipacao_tributaria"]', "1145|campanha")
        await s.clicar('//*[@id="PHConteudo_rb_dae_normal_1"]')
        await s.digitar('//*[@id="PHconteudoSemAjax_txt_num_inscricao_estad"]', guia.ie)
        await self._preencher_datas_valores(s, guia)

        for i, valor in enumerate(guia.notas[:15], start=1):
            input_path = ('//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal"]'
                          if i == 1 else f'//*[@id="PHconteudoSemAjax_txt_num_nota_fiscal{i}"]')
            await s.digitar(input_path, valor)

        await s.digitar('//*[@id="PHconteudoSemAjax_txt_qtd_nota_fiscal"]', str(len(guia.notas)))
        await s.digitar('//*[@id="PHconteudoSemAjax_txt_des_informacoes_complementares"]',
                  ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo.strftime("%m/%Y"),
                                               guia.uf, guia.notas, guia.fretes))
        await s.press('/html/body', "End")
        await s.click_js("//*[@id='PHconteudoSemAjax_btn_visualizar']")
        await self._salvar_como_pdf(s, guia)
        await s.close()

    # ==========================
    # Auxiliares
    # ==========================
    async def _wait_loading_spin_disapear(self):
        await asyncio.sleep(2) 
        
    
    async def difal(self, guia: Guia):
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        s = self.selHandler

        # Espera a frame estar disponível e troca o contexto
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mainFrame"))

        s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie)
        s.clicar('//*[@id="form1:buscarIe"]')
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoTipoDare"]', "1")
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoReceita"]', "101")
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo.strftime('%m%Y'))
        self._wait_loading_spin_disapear()
        s.digitar_blur('//*[@id="form1:valorPrincipal"]', guia.valor)
        self._wait_loading_spin_disapear()
        s.clicar('//*[@id="form1:cmdAdicionarDocumento"]')
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlip.get(guia.tipo, guia.periodo.strftime("%m/%Y"), guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="form1:cmdEmitir"]')

    async def antecipacao(self, guia: Guia):
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        s = self.selHandler

        # Espera a frame estar disponível e troca o contexto
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it("mainFrame"))

        s.digitar('//*[@id="form1:inscricaoEstadual"]', guia.ie)
        s.clicar('//*[@id="form1:buscarIe"]')
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoTipoDare"]', "1")
        self._wait_loading_spin_disapear()
        s.selecionar('//*[@id="form1:codigoReceita"]', "101")
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:periodoReferencia"]', guia.periodo.strftime('%m%Y'))
        self._wait_loading_spin_disapear()
        s.digitar_blur('//*[@id="form1:valorPrincipal"]', guia.valor)
        self._wait_loading_spin_disapear()
        s.clicar('//*[@id="form1:cmdAdicionarDocumento"]')
        self._wait_loading_spin_disapear()
        s.digitar('//*[@id="form1:informacoesComplementares"]', ObservationOfPaymentSlip.get(guia.tipo, guia.periodo.strftime("%m/%Y"), guia.uf, guia.notas, guia.fretes))
        s.clicar('//*[@id="form1:cmdEmitir"]')