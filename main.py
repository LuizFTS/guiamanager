from infrastructure.db.database import Database
from infrastructure.db.migrations import CREATE_TABLES_SCRIPT

from interface.gui.app import GuiaApp
from interface.controllers.excel_controller import ExcelController
from interface.controllers.guia_controller import GuiaController
from interface.controllers.loja_controller import LojaController
from interface.controllers.path_dynamic_controller import PathDynamicController
from interface.controllers.site_controller import SiteController

from application.usecases.gerar_guia_use_case import GerarGuiaUseCase
from application.usecases.importar_guias_excel_use_case import ImportarGuiasExcelUseCase

from infrastructure.db.site_repository_sqlite import SiteRepositorySQLite
from infrastructure.db.loja_repository_sqlite import LojaRepositorySQLite
from infrastructure.db.guia_repository_sqlite import GuiaRepositorySQLite


from application.usecases.adicionar_site_use_case import AdicionarSiteUseCase
from application.usecases.atualizar_site_use_case import AtualizarSiteUseCase
from application.usecases.deletar_site_use_case import DeletarSiteUseCase
from application.usecases.listar_sites_use_case import ListarSitesUseCase
from application.usecases.procurar_site_use_case import ProcurarSiteUseCase

from application.usecases.adicionar_loja_use_case import AdicionarLojaUseCase
from application.usecases.atualizar_loja_use_case import AtualizarLojaUseCase
from application.usecases.deletar_loja_use_case import DeletarLojaUseCase
from application.usecases.listar_lojas_use_case import ListarLojasUseCase
from application.usecases.procurar_loja_use_case import ProcurarLojaUseCase


def setup_database(db: Database):

    print(CREATE_TABLES_SCRIPT)
    db.execute_script(CREATE_TABLES_SCRIPT)

    print("Banco de dados criado e pronto para uso!")

def test_connection(db: Database):

    with db.connect() as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tabelas existentes:", rows)

def main():
    db = Database()
    setup_database(db)
    test_connection(db)

    # Service

    # Repositories
    siteRepository = SiteRepositorySQLite(db)
    lojaRepository = LojaRepositorySQLite(db)
    guiaRepository = GuiaRepositorySQLite(db)

    # UseCases
    gerarGuiaUsecase = GerarGuiaUseCase()
    #importarGuiasExcelUseCase = ImportarGuiasExcelUseCase(siteRepository, lojaRepository, guiaRepository, )

    adicionar_site_use_case = AdicionarSiteUseCase(siteRepository)
    atualizar_site_use_case = AtualizarSiteUseCase(siteRepository)
    deletar_site_use_case = DeletarSiteUseCase(siteRepository)
    listar_sites_use_case = ListarSitesUseCase(siteRepository)
    procurar_site_use_case = ProcurarSiteUseCase(siteRepository)

    adicionar_loja_use_case = AdicionarLojaUseCase(lojaRepository, siteRepository)
    atualizar_loja_use_case = AtualizarLojaUseCase(lojaRepository, siteRepository)
    deletar_loja_use_case = DeletarLojaUseCase(lojaRepository, siteRepository)
    listar_lojas_use_case = ListarLojasUseCase(lojaRepository, siteRepository)
    procurar_loja_use_case = ProcurarLojaUseCase(lojaRepository, siteRepository)

    # Controllers
    site = SiteController(adicionar_site_use_case, atualizar_site_use_case, deletar_site_use_case, listar_sites_use_case, procurar_site_use_case)
    loja = LojaController(adicionar_loja_use_case, atualizar_loja_use_case, deletar_loja_use_case, listar_lojas_use_case, procurar_loja_use_case)
    guia = GuiaController(gerarGuiaUsecase)
    #excel = ExcelController(importarGuiasExcelUseCase)
    path = PathDynamicController(gerarGuiaUsecase)


    # Inicializa Tkinter
    app = GuiaApp(guia, site, loja, path)
    app.mainloop()


if __name__ == "__main__":
    main()