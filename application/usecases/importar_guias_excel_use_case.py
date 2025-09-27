from domain.repositories.i_guia_repository import IGuiaRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.entities.guia import Guia

class ImportarGuiasExcelUseCase():
    
    def __init__(self, site_repo: ISiteRepository, loja_repo: ILojaRepository, guia_repo: IGuiaRepository, excel_service):
        self.guia_repo = guia_repo
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        self.excel_service = excel_service
        
    def execute(self, file_path: str) -> int:
        """ 
        Importa guias do Excel, salva no banco
        e retorna a quantidade de guias importadas.
        """
        # 1. Lê a planilha
        guias_data = self.excel_service.read_excel(file_path)
        
        
        count = 0
        for data in guias_data:
            # 2. Cria a entity Guia
            guia = Guia(**data)

            # 3. Resolve IDs ()
            loja = self.loja_repo.get_by_filial(guia.filial)
            site = self.site_repo.get_by_uf(guia.uf)
            if not loja or not site:
                raise Exception("Verificar se loja está cadastrada e se há o cadastro dos sites para UF da loja.")
            
            if self.guia_repo.save(guia, loja.id, site.id):
                count += 1
                
        return count