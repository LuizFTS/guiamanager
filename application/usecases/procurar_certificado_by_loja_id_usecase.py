from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.repositories.i_loja_repository import ILojaRepository
from domain.exceptions.domain_error import DomainError

class ProcurarCertificadoByLojaIdUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository, loja_repo: ILojaRepository):
        self.cert_repo = cert_repo
        self.loja_repo = loja_repo
        
    def execute(self, filial: str) -> bool:
        """ 
        Procurar certificado na tabela Certificados e se der erro
        será disparado DomainError
        """

        loja = self.loja_repo.get_by_filial(filial)
        if not loja:
            raise DomainError("Verifique se a loja já foi cadastrado.")
        
    
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        searched = self.cert_repo.get_by_loja_id(loja.id)        
        if not searched:
            raise DomainError("Erro ao encontrar o certificado.")