from application.usecases.adicionar_certificado_usecase import AdicionarCertificadoUseCase
from application.usecases.atualizar_certificado_usecase import AtualizarCertificadoUseCase
from application.usecases.deletar_certificado_usecase import DeletarCertificadoUseCase
from application.usecases.procurar_certificado_by_id_usecase import ProcurarCertificadoByIdUseCase
from application.usecases.procurar_certificado_by_loja_id_usecase import ProcurarCertificadoByLojaIdUseCase
from application.usecases.listar_certificados_usecase import ListarSitesUseCase

from domain.entities.certificado import Certificado
from typing import List

class CertificadoController:

    def __init__(
            self,
            adicionar_certificado_usecase: AdicionarCertificadoUseCase,
            atualizar_certificado_usecase: AtualizarCertificadoUseCase,
            deletar_certificado_usecase: DeletarCertificadoUseCase,
            procurar_certificado_by_id_usecase: ProcurarCertificadoByIdUseCase,
            procurar_certificado_by_loja_id_usecase: ProcurarCertificadoByLojaIdUseCase,
            listar_certificados_usecase: ListarSitesUseCase
    ):
        self.adicionar_certificado_usecase = adicionar_certificado_usecase
        self.atualizar_certificado_usecase = atualizar_certificado_usecase
        self.deletar_certificado_usecase = deletar_certificado_usecase
        self.procurar_certificado_by_id_usecase = procurar_certificado_by_id_usecase
        self.procurar_certificado_by_loja_id_usecase = procurar_certificado_by_loja_id_usecase
        self.listar_certificados_usecase = listar_certificados_usecase

    def get_all(self) -> List[Certificado]:
        certificados = self.listar_certificados_usecase.execute()
        return certificados
    
    def delete(self, id: int) -> None:
        self.deletar_certificado_usecase.execute(id)

    def atualizar(self, certificado: Certificado) -> None:
        self.atualizar_certificado_usecase.execute(certificado)

    def add(self, certificado: Certificado) -> None:
        self.adicionar_certificado_usecase.execute(certificado)

    def find_by_id(self, id: int) -> Certificado:
        certificado = self.procurar_certificado_by_id_usecase.execute(id)
        return certificado
    
    def find_by_loja_id(self, loja_id: int) -> Certificado:
        certificado = self.procurar_certificado_by_loja_id_usecase.execute(loja_id)
        return certificado