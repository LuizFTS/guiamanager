from domain.services.i_guia_generator_service import IGuiaGeneratorService
from infrastructure.utils.selenium_driver import SeleniumDriver
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService
from domain.entities.guia import Guia

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep



class GuiaGeneratorTOSelenium(IGuiaGeneratorService):

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

    
    def _get_municipio(self, filial):

        mun_map = {
            "77": "1702109",
            "30": "1702109",
            "45": "1716109"
        }

        mun = mun_map.get(filial)
        return mun
    
    def _wait_loading_spin_disapear(self, s: SeleniumDriver):
        sleep(0.3)
        WebDriverWait(s.driver, 10, 0.5).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="gx_ajax_notification"]/div'))
        )
    # ==========================
    # Funções de geração
    # ==========================
    def _icms(self, guia: Guia):
        s = self.driver

        s.digitar('//*[@id="vINSCRICAOESTADUAL"]', guia.ie)
        s.clicar('//*[@id="TABLE2"]/tbody/tr[5]/td/p/input')
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vDRECDGMUN"]', self._get_municipio(guia.filial))
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vDRECDGRCT"]', '110')
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vSUBCDGRCT"]', '1')
        self._wait_loading_spin_disapear(s)

        campo_data = s.driver.find_element(By.XPATH, '//*[@id="vDREDTAVEN"]')
        self._wait_loading_spin_disapear(s)
        s.driver.execute_script(f"""
        arguments[0].value = '{guia.vencimento}';
        """ + """
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, campo_data)
        self._wait_loading_spin_disapear(s)

        s.clear('//*[@id="vDREREFCHAR"]')
        s.digitar('//*[@id="vDREREFCHAR"]', guia.periodo)
        self._wait_loading_spin_disapear(s)
        s.clear('//*[@id="vDREVLRPRI"]')
        s.digitar('//*[@id="vDREVLRPRI"]', guia.valor)
        self._wait_loading_spin_disapear(s)
        s.clicar('//*[@id="TABLE4"]/tbody/tr[5]/td[4]/input')
        self._wait_loading_spin_disapear(s)

        s.digitar('//*[@id="vDREINFCOM"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        self._wait_loading_spin_disapear(s)
        s.clicar('//*[@id="TABLE5"]/tbody/tr/td[1]/input')
        WebDriverWait(s.driver, 10).until(EC.alert_is_present()).accept()
        s.clicar('//*[@id="IMGIMPDARE"]')

    def _difal(self, guia: Guia):
        s = self.driver

        s.digitar('//*[@id="vINSCRICAOESTADUAL"]', guia.ie)
        s.clicar('//*[@id="TABLE2"]/tbody/tr[5]/td/p/input')
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vDRECDGMUN"]', self._get_municipio(guia.filial))
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vDRECDGRCT"]', '150')
        self._wait_loading_spin_disapear(s)
        s.selecionar('//*[@id="vSUBCDGRCT"]', '1')
        self._wait_loading_spin_disapear(s)

        campo_data = s.driver.find_element(By.XPATH, '//*[@id="vDREDTAVEN"]')
        self._wait_loading_spin_disapear(s)


        s.driver.execute_script(f"""
        arguments[0].value = '{guia.vencimento}';
        """ + """
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, campo_data)
        self._wait_loading_spin_disapear(s)

        s.clear('//*[@id="vDREREFCHAR"]')
        self._wait_loading_spin_disapear(s)
        s.digitar('//*[@id="vDREREFCHAR"]', guia.periodo)
        self._wait_loading_spin_disapear(s)
        s.clear('//*[@id="vDREVLRPRI"]')
        s.digitar('//*[@id="vDREVLRPRI"]', guia.valor)
        self._wait_loading_spin_disapear(s)
        s.clicar('//*[@id="TABLE4"]/tbody/tr[5]/td[4]/input')
        self._wait_loading_spin_disapear(s)

        s.digitar('//*[@id="vDREINFCOM"]', ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes))
        self._wait_loading_spin_disapear(s)
        s.clicar('//*[@id="TABLE5"]/tbody/tr/td[1]/input')
        WebDriverWait(s.driver, 10).until(EC.alert_is_present()).accept()
        s.clicar('//*[@id="IMGIMPDARE"]')

