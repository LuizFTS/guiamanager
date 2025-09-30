from domain.repositories.i_site_repository import ISiteRepository
from domain.repositories.i_guia_repository import IGuiaRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.guia import Guia

class AtualizarGuiaUseCase:
    
    def __init__(self, site_repo: ISiteRepository, loja_repo: ILojaRepository, guia_repo: IGuiaRepository):
        self.site_repo = site_repo
        self.guia_repo = guia_repo
        self.loja_repo = loja_repo
        
    def execute(self, guia: Guia) -> None:
        """ 
        Atualizar site na tabela Sites e se der erro
        será disparado DomainError
        """
        
        loja = self.loja_repo.get_by_filial(guia.filial)
        site = self.site_repo.get_by_uf(loja.uf)
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        updated = self.guia_repo.update(guia, loja.id, site.id)      
        if not updated:
            raise DomainError("Erro ao atualizar as informações da loja.")