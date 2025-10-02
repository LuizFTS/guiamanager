from domain.repositories.i_guia_repository import IGuiaRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.guia import Guia

class ProcurarGuiaUseCase:
    
    def __init__(self, guia_repo: IGuiaRepository, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.guia_repo = guia_repo
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self, filial: str, tipo: str) -> Guia:
        """ 
        Procurar site por id que está na tabela Sites.
        Caso der errado, disparar DomainError
        """
        
        loja = self.loja_repo.get_by_filial(filial)

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.guia_repo.get_by_loja_id_and_tipo(loja.id, tipo)
        
        if saved:
            loja = self.loja_repo.get_by_id(saved.loja_id)
            saved.filial = loja.filial
            saved.cnpj = loja.cnpj
            saved.ie = loja.ie
            saved.uf = loja.uf
            
            site = self.site_repo.get_url_by_uf_and_type(saved.uf, saved.tipo)
            saved.site = site
            
            return saved        
            