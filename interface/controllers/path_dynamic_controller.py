from domain.entities.guia import Guia
from application.usecases.gerar_guia_use_case import GerarGuiaUseCase


class PathDynamicController:
    def __init__(self, gerar_guia_usecase: GerarGuiaUseCase):
        self.gerar_guia_usecase = gerar_guia_usecase