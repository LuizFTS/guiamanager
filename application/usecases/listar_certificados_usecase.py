from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class ListarSitesUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self) -> list[Site]:
        """ 
        Listar todos os sites que estão na tabela Sites.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.site_repo.list_all()        
        if not saved:
            raise DomainError("Erro ao listar as informações dos sites.")
        
        return saved