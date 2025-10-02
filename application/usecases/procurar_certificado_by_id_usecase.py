from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.exceptions.domain_error import DomainError

class ProcurarCertificadoByIdUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository):
        self.cert_repo = cert_repo
        
    def execute(self, id: int) -> bool:
        """ 
        Procurar certificado na tabela Certificados e se der erro
        será disparado DomainError
        """
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        searched = self.cert_repo.get_by_id(id)        
        if not searched:
            raise DomainError("Erro ao encontrar o certificado.")