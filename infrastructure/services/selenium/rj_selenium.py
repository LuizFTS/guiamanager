from domain.services.i_guia_generator_service import IGuiaGeneratorService
from infrastructure.utils.selenium_driver import SeleniumDriver

class GuiaGeneratorRJSelenium(IGuiaGeneratorService):
    
    def __init__(self, driver, handler_cls: type[SeleniumDriver], path_to_save: str, file_name: str):
        self.driver = driver
        self.handler_cls = handler_cls(driver)
        self.path = path_to_save
        self.file_name = file_name