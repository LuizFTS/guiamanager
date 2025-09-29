from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.loja import Loja

class DeletarLojaUseCase:
    
    def __init__(self, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self, filial: str) -> None:
        """ 
        Deletar loja na tabela Lojas e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.loja_repo.delete(filial)        
        if not saved:
            raise DomainError("Erro ao deletar a loja.")