from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.certificado import Certificado

class AtualizarCertificadoUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository, loja_repo: ILojaRepository):
        self.cert_repo = cert_repo
        self.loja_repo = loja_repo
        
    def execute(self, certificado: Certificado) -> None:
        """ 
        Atualizar certificado na tabela Certificados e se der erro
        será disparado DomainError
        """

        loja = self.loja_repo.get_by_filial(certificado.filial)
        if not loja:
            raise DomainError("Verifique se a loja já foi cadastrado.")
        
        certificado.loja_id = loja.id

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        updated = self.cert_repo.update(certificado)      
        if not updated:
            raise DomainError("Erro ao atualizar as informações do certificado.")