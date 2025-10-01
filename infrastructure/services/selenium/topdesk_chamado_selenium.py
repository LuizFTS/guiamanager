from domain.entities.guia import Guia
from infrastructure.utils.selenium_driver import SeleniumDriver
from infrastructure.config import Settings


class TopdeskChamadoSelenium:

    def __init__(self):
        self.user = Settings.TOPDESK_USER
        self.password = Settings.TOPDESK_PASSWORD
        self.phone = Settings.TOPDESK_PHONE

    def _cda_or_casal(self, filial: str):
        nFilial = int(filial)
        if nFilial < 70:
            return "ssdformcd84fe60677c4153ac75fcdbfd6e1e67_searchlist2_searchlist_searchlist_option0"
        else:
            return "ssdformcd84fe60677c4153ac75fcdbfd6e1e67_searchlist2_searchlist_searchlist_option1"

    def gerar(self, guia: Guia) -> str:
        """
        Gera a guia do estado da BA de acordo com o tipo.
        Retorna o bool caso o PDF foi gerado.
        """
        self.path = guia.path_save
        self.file_name = guia.file_name
        
        self.driver = SeleniumDriver(guia.path_save, headless=False)
        s = self.driver
        s.driver.get("https://casadoadubo.topdesk.net/tas/public/login/form")

        

        s.digitar('/html/body/div/main/div/div[2]/form/input[1]', self.user)
        s.digitar('/html/body/div/main/div/div[2]/form/input[2]', self.password)
        s.clicar('/html/body/div/main/div/div[2]/form/input[3]') # Login
        s.clicar('/html/body/div/div/main/div/div[3]/a[1]') # Abertura de chamados
        s.clicar('/html/body/div/div/main/div[1]/a[1]') # ADM Central
        s.clicar('/html/body/div/div/main/div[2]/a[4]') # Financeiro
        s.clicar('/html/body/div/div/main/div[1]/a') # Contas a pagar
        s.clicar('/html/body/div/div/main/div[1]/a[9]') # Pagamento Fiscal
        s.digitar('/html/body/form/fieldset[17]/fieldset/div[3]/div[1]/div/input', self.phone) # Celular
        s.digitar('/html/body/form/fieldset[25]/fieldset/div/div[1]/div/input[1]', 'Solicitar serviço') # Solicitar Serviço
        s.digitar('/html/body/form/fieldset[28]/fieldset/div/div[1]/div/input[1]', 'Pagamento Fiscal') # Pagamento Fiscal
        s.selecionar('/html/body/form/fieldset[31]/fieldset/div/div[1]/div/select', self._cda_or_casal(guia.filial)) # Casa do adubo ou Casal
        s.digitar('/html/body/form/fieldset[34]/fieldset/div/div[1]/div/input', "1") # Quantidade de guias
        s.digitar('/html/body/form/fieldset[37]/fieldset/div/div[1]/div/input', guia.valor) # Valor
        s.digitar('/html/body/form/fieldset[39]/fieldset/div/div[1]/div/input', "0,00") # Valor juros/multa
        s.digitar('/html/body/form/fieldset[41]/fieldset/div/div[1]/div/input', guia.valor) # Valor + juros/multa
        s.clicar('/html/body/form/fieldset[43]/fieldset/div/div[1]/div/div[3]/input') # Boleto
        input_file = s.get_element('/html/body/form/fieldset[79]/fieldset/div/div[1]/div/input[2]')
        input_file.send_keys(guia.get_full_path)

