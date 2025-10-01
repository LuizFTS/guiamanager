from domain.entities.guia import Guia
from infrastructure.factories.guia_generator_factory import GuiaGeneratorFactory

class GerarGuiaUseCase:
    def execute(self, guia: Guia) -> bool:
        """ 
         Orquestra a geração da guia:
        - Seleciona a tecnologia correta
        - Chama o serviço de geração
        - Retorna o booleano se pdf foi salvo na pasta ou não
        """

        generator = GuiaGeneratorFactory.create(guia.uf)

        guia.valor = f"{float(guia.valor):.2f}".replace(".", ",")
        guia.periodo = guia.periodo.strftime('%m/%Y')
        guia.vencimento = guia.vencimento.strftime('%d/%m/%Y')
        
        pdf_path = generator.gerar(guia)
        return pdf_path
    
    