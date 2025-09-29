from domain.entities.site import Site
from application.usecases.adicionar_site_use_case import AdicionarSiteUseCase
from application.usecases.atualizar_site_use_case import AtualizarSiteUseCase
from application.usecases.deletar_site_use_case import DeletarSiteUseCase
from application.usecases.listar_sites_use_case import ListarSitesUseCase
from application.usecases.procurar_site_use_case import ProcurarSiteUseCase
from typing import List


class SiteController:
    def __init__(self, 
                 adicionar_site_usecase: AdicionarSiteUseCase,
                 atualizar_site_usecase: AtualizarSiteUseCase,
                 deletar_site_usecase: DeletarSiteUseCase,
                 listar_sites_usecase: ListarSitesUseCase,
                 procurar_site_usecase: ProcurarSiteUseCase
                 ):
        self.adicionar_site_usecase = adicionar_site_usecase
        self.atualizar_site_usecase = atualizar_site_usecase
        self.deletar_site_usecase = deletar_site_usecase
        self.listar_sites_usecase = listar_sites_usecase
        self.procurar_site_usecase = procurar_site_usecase

    def get_all(self) -> List[Site]:
        sites = self.listar_sites_usecase.execute()
        return sites
    
    def delete(self, uf: str) -> None:
        self.deletar_site_usecase.execute(uf)

    def atualizar(self, site: Site) -> None:
        self.atualizar_site_usecase.execute(site)

    def add(self, site: Site ) -> None:
        self.adicionar_site_usecase.execute(site)

    def find(self, uf: str) -> Site:
        return self.procurar_site_usecase.execute(uf)
    