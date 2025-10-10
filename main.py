from infrastructure.db.database import Database

from interface.gui.app import GuiaApp

from interface.controllers.excel_controller import ExcelController
from interface.controllers.guia_controller import GuiaController
from interface.controllers.loja_controller import LojaController
from interface.controllers.path_dynamic_controller import PathDynamicController
from interface.controllers.site_controller import SiteController

from application.usecases.importar_guias_excel_usecase import ImportarGuiasExcelUseCase

from infrastructure.db.site_repository_sqlite import SiteRepositorySQLite
from infrastructure.db.loja_repository_sqlite import LojaRepositorySQLite
from infrastructure.db.guia_repository_sqlite import GuiaRepositorySQLite


from application.usecases.adicionar_site_usecase import AdicionarSiteUseCase
from application.usecases.atualizar_site_usecase import AtualizarSiteUseCase
from application.usecases.deletar_site_usecase import DeletarSiteUseCase
from application.usecases.listar_sites_usecase import ListarSitesUseCase
from application.usecases.procurar_site_usecase import ProcurarSiteUseCase
from application.usecases.procurar_url_site_usecase import ProcurarUrlSiteUseCase

from application.usecases.adicionar_loja_usecase import AdicionarLojaUseCase
from application.usecases.atualizar_loja_usecase import AtualizarLojaUseCase
from application.usecases.deletar_loja_usecase import DeletarLojaUseCase
from application.usecases.listar_lojas_usecase import ListarLojasUseCase
from application.usecases.procurar_loja_usecase import ProcurarLojaUseCase

from application.usecases.gerar_guia_usecase import GerarGuiaUseCase
from application.usecases.procurar_guia_usecase import ProcurarGuiaUseCase
from application.usecases.adicionar_guia_usecase import AdicionarGuiaUseCase
from application.usecases.listar_guias_usecase import ListarGuiasUseCase
from application.usecases.deletar_guia_usecase import DeletarGuiaUseCase
from application.usecases.procurar_guia_by_id_usecase import ProcurarGuiaByIdUseCase
from application.usecases.atualizar_guia_usecase import AtualizarGuiaUseCase

from infrastructure.excel.excel_service import ExcelService
from infrastructure.db.migrations.migrate import main as run_migrations

def setup_database():

    run_migrations()

    print("Banco de dados criado e pronto para uso!")

def test_connection(db: Database):

    with db.connect() as conn:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tabelas existentes:", rows)

def main():
    db = Database()
    setup_database()
    test_connection(db)

    # Service
    excel_service = ExcelService()

    # Repositories
    siteRepository = SiteRepositorySQLite(db)
    lojaRepository = LojaRepositorySQLite(db)
    guiaRepository = GuiaRepositorySQLite(db)

    # UseCases
    importarGuiasExcelUseCase = ImportarGuiasExcelUseCase(siteRepository, lojaRepository, guiaRepository, excel_service)

    adicionar_site_use_case = AdicionarSiteUseCase(siteRepository)
    atualizar_site_use_case = AtualizarSiteUseCase(siteRepository)
    deletar_site_use_case = DeletarSiteUseCase(siteRepository)
    listar_sites_use_case = ListarSitesUseCase(siteRepository)
    procurar_site_use_case = ProcurarSiteUseCase(siteRepository)
    procurar_url_site_use_case = ProcurarUrlSiteUseCase(siteRepository)

    adicionar_loja_use_case = AdicionarLojaUseCase(lojaRepository, siteRepository)
    atualizar_loja_use_case = AtualizarLojaUseCase(lojaRepository, siteRepository)
    deletar_loja_use_case = DeletarLojaUseCase(lojaRepository, siteRepository)
    listar_lojas_use_case = ListarLojasUseCase(lojaRepository, siteRepository)
    procurar_loja_use_case = ProcurarLojaUseCase(lojaRepository, siteRepository)
    
    gerar_guia_use_case = GerarGuiaUseCase()
    procurar_guia_use_case = ProcurarGuiaUseCase(guiaRepository, lojaRepository, siteRepository)
    adicionar_guia_use_case = AdicionarGuiaUseCase(guiaRepository, lojaRepository, siteRepository)
    listar_guias_use_case = ListarGuiasUseCase(guiaRepository, lojaRepository, siteRepository)
    deletar_guia_use_case = DeletarGuiaUseCase(guiaRepository)
    procurar_guia_by_id_use_case = ProcurarGuiaByIdUseCase(guiaRepository, lojaRepository, siteRepository)
    atualizar_guia_use_case = AtualizarGuiaUseCase(siteRepository, lojaRepository, guiaRepository)

    # Controllers
    site = SiteController(adicionar_site_use_case, atualizar_site_use_case, deletar_site_use_case, listar_sites_use_case, procurar_site_use_case, procurar_url_site_use_case)
    loja = LojaController(adicionar_loja_use_case, atualizar_loja_use_case, deletar_loja_use_case, listar_lojas_use_case, procurar_loja_use_case)
    guia = GuiaController(gerar_guia_use_case, procurar_guia_use_case, adicionar_guia_use_case, listar_guias_use_case, deletar_guia_use_case, procurar_guia_by_id_use_case, atualizar_guia_use_case)
    excel = ExcelController(importarGuiasExcelUseCase)
    path = PathDynamicController(gerar_guia_use_case)


    # Inicializa Tkinter
    app = GuiaApp(excel, guia, site, loja, path)
    app.mainloop()


if __name__ == "__main__":
    main()