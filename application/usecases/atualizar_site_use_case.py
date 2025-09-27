from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.site import Site

class AtualizarLojaUseCase:
    
    def __init__(self, site_repo: ISiteRepository):
        self.site_repo = site_repo
        
    def execute(self, site: Site) -> None:
        """ 
        Atualizar site na tabela Sites e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        updated = self.site_repo.update(site)      
        if not updated:
            raise DomainError("Erro ao atualizar as informações da loja.")