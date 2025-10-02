from domain.entities.guia import Guia
from application.usecases.importar_guias_excel_usecase import ImportarGuiasExcelUseCase


class ExcelController:
    def __init__(self, importar_excel_usecase: ImportarGuiasExcelUseCase):
        self.importar_excel_usecase = importar_excel_usecase

    def importar_excel(self, path: str):
        return self.importar_excel_usecase.execute(file_path=path)