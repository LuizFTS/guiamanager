from domain.entities.guia import Guia
from application.usecases.gerar_guia_use_case import GerarGuiaUseCase


class GuiaController:
    def __init__(self, gerar_guia_usecase: GerarGuiaUseCase):
        self.gerar_guia_usecase = gerar_guia_usecase

    def gerar_guia(self, guia: Guia):
        return self.gerar_guia_usecase.execute(guia)
    
    def find(self):
        