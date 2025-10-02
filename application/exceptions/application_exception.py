

class ApplicationException(Exception):
    """Exceções da camada de aplicação (serviços)."""
    def __init__(self, message: str):
        super().__init__(message)