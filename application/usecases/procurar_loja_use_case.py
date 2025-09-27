from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.loja import Loja

class ProcurarLojaUseCase:
    
    def __init__(self, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self, id: int) -> Loja:
        """ 
        Procurar loja por id que está na tabela Lojas.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.loja_repo.get_by_id(id)      
        if not saved:
            raise DomainError("Loja não encontrada.")
        
        return saved