from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.loja import Loja

class AdicionarLojaUseCase:
    
    def __init__(self, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        
    def execute(self, loja: Loja) -> None:
        """ 
        Adicionar loja na tabela Lojas e retornar
        true/false se operação deu certo
        """
        
        # ✅ Verifica se existe site para a UF informada
        site = self.site_repo.get_by_uf(loja.uf)
        if not site:
            raise DomainError("Verifique se o site para essa UF já foi cadastrado.")
        
        
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.loja_repo.save(loja, site.id)        
        if not saved:
            raise DomainError("Erro ao salvar as informações da loja.")