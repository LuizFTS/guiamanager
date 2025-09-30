from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_site_repository import ISiteRepository
from domain.repositories.i_guia_repository import IGuiaRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.guia import Guia

class AdicionarGuiaUseCase:
    
    def __init__(self, guia_repo: IGuiaRepository, loja_repo: ILojaRepository, site_repo: ISiteRepository):
        self.loja_repo = loja_repo
        self.site_repo = site_repo
        self.guia_repo = guia_repo
        
    def execute(self, guia: Guia) -> bool:
        """ 
        Adicionar loja na tabela Lojas e retornar
        true/false se operação deu certo
        """
        
        # ✅ Verifica se existe site para a UF informada
        site = self.site_repo.get_by_uf(guia.uf)
        loja = self.loja_repo.get_by_filial(guia.filial)
        if not site:
            raise DomainError("Verifique se o site para essa UF já foi cadastrado.")
        
        is_there_a_guia = self.guia_repo.get_by_loja_id_and_tipo(loja.id, guia.tipo)
        if is_there_a_guia:
            return
        
        
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.guia_repo.save(guia, loja.id, site.id)        
        if not saved:
            raise DomainError("Erro ao salvar as informações da loja.")
        
        return True