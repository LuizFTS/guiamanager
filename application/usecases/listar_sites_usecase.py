from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.certificado import Certificado

class ListarSitesUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository):
        self.cert_repo = cert_repo
        
    def execute(self) -> list[Certificado]:
        """ 
        Listar todos os certificados que estão na tabela Certificados.
        Caso der errado, disparar DomainError
        """

        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        searched = self.cert_repo.list_all()        
        if not searched:
            raise DomainError("Erro ao listar as informações dos certificados.")
        
        return searched