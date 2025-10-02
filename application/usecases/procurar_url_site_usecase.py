from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class ProcurarUrlSiteUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self, uf: str, tipo: str) -> str:
        """ 
        Procurar site por id que está na tabela Sites.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.site_repo.get_url_by_uf_and_type(uf, tipo)      
        if not saved:
            raise DomainError("Site não encontrado.")
        
        return saved