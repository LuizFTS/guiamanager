from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class DeletarSiteUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self, site: Site) -> None:
        """ 
        Deletar site na tabela Sites e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.site_repo.delete(site.id)        
        if not saved:
            raise DomainError("Erro ao deletar site.")