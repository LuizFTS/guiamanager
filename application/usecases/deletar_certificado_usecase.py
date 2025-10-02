from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.exceptions.domain_error import DomainError

class DeletarCertificadoUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository):
        self.cert_repo = cert_repo
        
    def execute(self, id: int) -> bool:
        """ 
        Deletar certificado na tabela Certificados e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.cert_repo.delete(id)        
        if not saved:
            raise DomainError("Erro ao deletar a certificado.")