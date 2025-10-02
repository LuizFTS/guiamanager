from domain.repositories.i_guia_repository import IGuiaRepository
from domain.exceptions.domain_error import DomainError

class DeletarGuiaUseCase:
    
    def __init__(self, guia_repo: IGuiaRepository):
        self.guia_repo = guia_repo
        
    def execute(self, id: str) -> None:
        """ 
        Deletar loja na tabela Lojas e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.guia_repo.delete(id)        
        if not saved:
            raise DomainError("Erro ao deletar a loja.")