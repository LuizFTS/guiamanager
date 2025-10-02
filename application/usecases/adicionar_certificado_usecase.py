from domain.repositories.i_loja_repository import ILojaRepository
from domain.repositories.i_certificado_repository import ICertificadoRepository
from domain.exceptions.domain_error import DomainError
from domain.entities.certificado import Certificado

class AdicionarCertificadoUseCase:
    
    def __init__(self, cert_repo: ICertificadoRepository, loja_repo: ILojaRepository):
        self.loja_repo = loja_repo
        self.cert_repo = cert_repo
        
    def execute(self, certificado: Certificado) -> bool:
        """ 
        Adicionar certificado na tabela Certificados e retornar
        true/false se operação deu certo
        """
        
        # ✅ Verifica se existe loja na tabela Lojas
        loja = self.loja_repo.get_by_filial(certificado.filial)
        if not loja:
            raise DomainError("Verifique se a loja já foi cadastrado.")
        
        certificado.loja_id = loja.id

        is_there_a_guia = self.cert_repo.get_by_cnpj(loja.cnpj)
        if is_there_a_guia:
            return
        
        
        # ✅ Se a entidade foi criada com sucesso, já passou nas validações
        saved = self.cert_repo.save(certificado)        
        if not saved:
            raise DomainError("Erro ao salvar as informações do certificado.")
        
        return saved