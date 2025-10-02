from domain.entities.guia import Guia
from application.usecases.gerar_guia_usecase import GerarGuiaUseCase
from application.usecases.procurar_guia_usecase import ProcurarGuiaUseCase
from application.usecases.adicionar_guia_usecase import AdicionarGuiaUseCase
from application.usecases.listar_guias_usecase import ListarGuiasUseCase
from application.usecases.deletar_guia_usecase import DeletarGuiaUseCase
from application.usecases.procurar_guia_by_id_usecase import ProcurarGuiaByIdUseCase
from application.usecases.atualizar_guia_usecase import AtualizarGuiaUseCase

class GuiaController:
    def __init__(self, 
                 gerar_guia_usecase: GerarGuiaUseCase,
                 procurar_guia_usecase: ProcurarGuiaUseCase,
                 adicionar_guia_usecase: AdicionarGuiaUseCase,
                 listar_guias_usecase: ListarGuiasUseCase,
                 deletar_guia_usecase: DeletarGuiaUseCase,
                 procurar_guia_by_id_usecase: ProcurarGuiaByIdUseCase,
                 atualizar_guia_usecase: AtualizarGuiaUseCase
                 ):
        self.gerar_guia_usecase = gerar_guia_usecase
        self.procurar_guia_usecase = procurar_guia_usecase
        self.adicionar_guia_usecase = adicionar_guia_usecase
        self.listar_guias_usecase = listar_guias_usecase
        self.deletar_guia_usecase = deletar_guia_usecase
        self.procurar_guia_by_id_usecase = procurar_guia_by_id_usecase
        self.atualizar_guia_usecase = atualizar_guia_usecase

    def gerar_guia(self, guia: Guia):
        return self.gerar_guia_usecase.execute(guia)
    
    def add(self, guia: Guia) -> int:
        return self.adicionar_guia_usecase.execute(guia)
    
    def update(self, guia: Guia):
        return self.atualizar_guia_usecase.execute(guia)
    
    def delete(self, id: int):
        return self.deletar_guia_usecase.execute(id)
    
    def find(self, filial: str, tipo: str) -> Guia:
        return self.procurar_guia_usecase.execute(filial, tipo)
    
    def find_by_id(self, id: int) -> Guia:
        return self.procurar_guia_by_id_usecase.execute(id)
    
    def get_all(self) -> list[Guia]:
        return self.listar_guias_usecase.execute()