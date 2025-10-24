import traceback
from tkinter import messagebox
from domain.exceptions.domain_error import DomainError
from application.exceptions.application_exception import ApplicationException
from infrastructure.exceptions.infrastructure_exception import InfrastructureException

class ExceptionHandler:

    @staticmethod
    def handle(exception: Exception):
        """ 
        Decide como mostrar a exceção ao usuário. 
        """
        if isinstance(exception, DomainError):
            messagebox.showwarning("Erro de Negócio", str(exception))

        elif isinstance(exception, ApplicationException):
            messagebox.showerror("Erro de Aplicação", str(exception))

        elif isinstance(exception, InfrastructureException):
            messagebox.showerror("Erro Técnico", f"{str(exception)}\n\nVerifique logs.")

        else:
            # Erros inesperados → logar + mostrar genérico
            traceback.print_exc()
            messagebox.showerror("Erro Desconhecido", "Ocorreu um erro inesperado.")