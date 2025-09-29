from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class AdicionarSiteUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self, site: Site) -> None:
        """ 
        Adicionar site na tabela Sites e se
        der erro, dispara DomainError
        """
        is_not_unique = self.site_repo.get_by_uf(site.uf)
        if(is_not_unique):
            raise DomainError("UF já cadastrada.")
        
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.site_repo.save(site)        
        if not saved:
            raise DomainError("Erro ao salvar as informações do site.")