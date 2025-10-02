from domain.repositories.i_guia_repository import IGuiaRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.guia import Guia

class ListarGuiasUseCase:
    
    def __init__(self, guia_repo: IGuiaRepository, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.guia_repo = guia_repo
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self) -> list[Guia]:
        """ 
        Listar todos os sites que estão na tabela Sites.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.guia_repo.list_all()
            
        if not saved:
            return
        
        guias = []
        for save in saved:
            loja = self.loja_repo.get_by_id(save.loja_id)
            save.filial = loja.filial
            save.cnpj = loja.cnpj
            save.ie = loja.ie
            save.uf = loja.uf
            
            site = self.site_repo.get_url_by_uf_and_type(save.uf, save.tipo)
            save.site = site
            
            guias.append(save)
            
        return guias