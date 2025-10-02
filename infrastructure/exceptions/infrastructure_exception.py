

class InfrastructureException(Exception):
    """Exceções da camada de infraestrutura (arquivos, db, rede)."""
    def __init__(self, message: str):
        super().__init__(message)