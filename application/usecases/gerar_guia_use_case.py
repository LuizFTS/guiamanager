from domain.entities.guia import Guia
from infrastructure.factories.guia_generator_factory import GuiaGeneratorFactory

class GerarGuiaUseCase:
    def execute(self, guia: Guia) -> str:
        """ 
         Orquestra a geração da guia:
        - Seleciona a tecnologia correta
        - Chama o serviço de geração
        - Retorna o caminho do PDF
        """

        generator = GuiaGeneratorFactory.create(guia.uf)
        pdf_path = generator.gerar(guia)
        return pdf_path
    
    