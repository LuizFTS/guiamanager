from domain.entities.loja import Loja
from application.usecases.adicionar_loja_usecase import AdicionarLojaUseCase
from application.usecases.atualizar_loja_usecase import AtualizarLojaUseCase
from application.usecases.deletar_loja_usecase import DeletarLojaUseCase
from application.usecases.listar_lojas_usecase import ListarLojasUseCase
from application.usecases.procurar_loja_usecase import ProcurarLojaUseCase

from typing import List

class LojaController:
    def __init__(self, 
                 adicionar_loja_usecase: AdicionarLojaUseCase,
                 atualizar_loja_usecase: AtualizarLojaUseCase,
                 deletar_loja_usecase: DeletarLojaUseCase,
                 listar_lojas_usecase: ListarLojasUseCase,
                 procurar_loja_usecase: ProcurarLojaUseCase
                 ):
        self.adicionar_loja_usecase = adicionar_loja_usecase
        self.atualizar_loja_usecase = atualizar_loja_usecase
        self.deletar_loja_usecase = deletar_loja_usecase
        self.listar_lojas_usecase = listar_lojas_usecase
        self.procurar_loja_usecase = procurar_loja_usecase

    def get_all(self) -> List[Loja]:
        lojas = self.listar_lojas_usecase.execute()
        return lojas
    
    def delete(self, filial: str) -> None:
        self.deletar_loja_usecase.execute(filial)

    def atualizar(self, loja: Loja) -> None:
        self.atualizar_loja_usecase.execute(loja)

    def add(self, loja: Loja ) -> None:
        self.adicionar_loja_usecase.execute(loja)

    def find(self, filial: str) -> Loja:
        return self.procurar_loja_usecase.execute(filial)
    