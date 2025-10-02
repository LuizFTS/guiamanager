from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class ProcurarSiteUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self, uf: str) -> Site:
        """ 
        Procurar site por id que está na tabela Sites.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.site_repo.get_by_uf(uf)      
        if not saved:
            raise DomainError("Site não encontrado.")
        
        return saved