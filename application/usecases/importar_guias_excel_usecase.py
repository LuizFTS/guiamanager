from domain.repositories.i_guia_repository import IGuiaRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.services.i_read_excel_service import IReadExcelService
from domain.entities.guia import Guia

class ImportarGuiasExcelUseCase():
    
    def __init__(self, site_repo: ISiteRepository, loja_repo: ILojaRepository, guia_repo: IGuiaRepository, excel_service: IReadExcelService):
        self.guia_repo = guia_repo
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        self.excel_service = excel_service
        
    def execute(self, file_path: str) -> int:
        """ 
        Importa guias do Excel, e gera um
        Entity Guia para cada linha importada e retorna
        a lista de todas as guias.
        """
        # 1. Lê a planilha
        guias: list[Guia] = self.excel_service.read(file_path)

        for guia in guias:
            loja = self.loja_repo.get_by_filial(guia.filial)
            site = self.site_repo.get_url_by_uf_and_type(loja.uf, guia.tipo)
            site_id = self.site_repo.get_by_uf(loja.uf).id

            guia.cnpj = loja.cnpj
            guia.ie = loja.ie
            guia.uf = loja.uf
            guia.loja_id = loja.id
            guia.site_id = site_id

            guia.site = site


        return guias