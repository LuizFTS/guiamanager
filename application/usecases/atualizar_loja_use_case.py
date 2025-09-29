from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.loja import Loja

class AtualizarLojaUseCase:
    
    def __init__(self, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self, loja: Loja) -> None:
        """ 
        Atualizar loja na tabela Lojas e se der erro
        será disparado DomainError
        """

        # ✅ Verifica se existe site para a UF informada
        site = self.site_repo.get_by_uf(loja.uf)
        if not site:
            raise DomainError("Verifique se o site para essa UF já foi cadastrado.")
    
        # ✅ Se a entidade foi atualizada com sucesso, já passou nas validações
        updated = self.loja_repo.update(loja, site.id)      
        if not updated:
            raise DomainError("Erro ao atualizar as informações da loja.")