from domain.entities.guia import Guia
from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService

import requests
from collections import OrderedDict
import socket
from datetime import datetime, timedelta
import pandas as pd
from math import floor
from requests_toolbelt.multipart.encoder import MultipartEncoder

class GuiaGeneratorMTRequest(IGuiaGeneratorService):

    def __init__(self):
        self.paths = {
            "url1": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/menudarlivre",
            "url2": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/pj/gerardar",
            "url3": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/impirmirdar?chavePix=true"
        }

    def _format_inscEstadual(self, ie: str) -> str:
        # garante que a string tem 9 dígitos
        ie = ie.zfill(9)
        # formata nos padrões: XX.XXX.XXX-X
        return f"{ie[:2]}.{ie[2:5]}.{ie[5:8]}-{ie[8]}"
    
    def _get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # conecta a um IP qualquer da internet sem enviar dados
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip
    
    def _get_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))  # 0 significa porta aleatória
        port = s.getsockname()[1]
        s.close()
        return port

    def _get_mun(self, guia: Guia):
        mun_map = {
            "05": "90000",
            "74": "90000",
            "22": "255009",
            "28": "89001",
            "29": "65005"
        }

        return mun_map.get(guia.filial)
        
    def _get_numr_contribuinte(self, guia: Guia):
        numr_map = {
            "74": "127551969",
            "22": "127584827",
            "05": "80341",
            "28": "127965074",
            "29": "128114367"

        }
        return numr_map.get(guia.filial)

    def _get_valor(self, guia: Guia):

        vencimento = datetime.strptime(guia.vencimento, "%d/%m/%Y")

        if (vencimento.date() < datetime.now().date()):
            data_inicial = vencimento.strftime("%d/%m/%Y")
            data_final = datetime.now().strftime("%d/%m/%Y")

            # Série 4390: Selic acumulada mensal
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
            response = requests.get(url)
            response.raise_for_status()
            
            dados = response.json()
            df = pd.DataFrame(dados)
            
            # Limpeza e conversão para float
            df["valor"] = df["valor"].str.replace(",", ".").astype(float)
            
            if df.empty:
                return 0.0
            
            # Soma das taxas mensais
            df.loc[df.index[0], "valor"] = 0.00
            df.loc[df.index[-1], "valor"] = 1.00

            soma_taxas = df["valor"].sum()

            percentual_juros = float(soma_taxas)/100
            juros = float(guia.valor.replace(",", ".")) * percentual_juros

        else:
            juros = 0.00
        

        days = int(self._ajustar_data(vencimento).get("days"))

        fator_multiplicacao = days * 0.00333

        if fator_multiplicacao > 0.2:
            valor_multa = 0.2 * (float(guia.valor.replace(",", ".")))
            return {
                "valor": str(guia.valor).replace(".", ","),
                "valor_juros": str(floor(juros * 100) / 100).replace(".", ","),
                "valor_multa": str(floor(valor_multa * 100) / 100).replace(".", ","),
                "days": str(days)
            }
        else:
            valor_multa = fator_multiplicacao * (float(guia.valor.replace(",",".")))
            return {
                "valor": str(guia.valor.replace(",",".")).replace(".", ","),
                "valor_juros": str(floor(juros * 100) / 100).replace(".", ","),
                "valor_multa": str(floor(valor_multa * 100) / 100).replace(".", ","),
                "days": str(days)
            }

    def _ajustar_data(self, data: datetime | str) -> dict[str, str]:

        if isinstance(data, datetime):
            pass
        else:
            data = datetime.strptime(str(data), "%d/%m/%Y")

        hoje = datetime.now().date()
        agora = datetime.now()

        if data.date() >= hoje:
            return {"date": data.strftime("%d/%m/%Y"), "days": "0"}

        if agora.hour >= 9:
            proximo_dia = hoje + timedelta(days=1)
            while proximo_dia.weekday() >= 5:  # sábado=5, domingo=6
                proximo_dia += timedelta(days=1)
            nova_data = datetime.combine(proximo_dia, data.time())
        else:
            nova_data = datetime.combine(hoje, data.time())

        diferenca = (nova_data.date() - data.date()).days
        return {"date": nova_data.strftime("%d/%m/%Y"), "days": str(diferenca)}

    def gerar(self, guia: Guia):

        session = requests.Session()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.sefaz.mt.gov.br",
            "Referer": "https://www.google.com/",  # ou outra página inicial
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        # Faz a primeira requisição GET
        response = session.get(self.paths.get("url1"), headers=headers)

        # Verifica se deu certo
        if response.status_code != 200:
            return False

        headers_step2 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.sefaz.mt.gov.br",
            "Referer": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/menudarlivre",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": session.headers.get("User-Agent"),  # reaproveita User-Agent do GET inicial
            "sec-ch-ua": session.headers.get("sec-ch-ua"),
            "sec-ch-ua-mobile": session.headers.get("sec-ch-ua-mobile"),
            "sec-ch-ua-platform": session.headers.get("sec-ch-ua-platform"),
        }

        data = {
            'codgOrgao': '',
            'tipoTributo': '',
            'ipContribuinte': self._get_local_ip(),
            'portaContribuinte': self._get_port(),
            'pjInscrita': 'true',
        }


        response_post = session.post(self.paths.get("url2"), headers=headers_step2, data=data)

        # Verifica se deu certo
        if response_post.status_code != 200:
            return False

        headers_step3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.sefaz.mt.gov.br",
            "Referer": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/pj/gerardar",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": session.headers.get("User-Agent"),
            "sec-ch-ua": session.headers.get("sec-ch-ua"),
            "sec-ch-ua-mobile": session.headers.get("sec-ch-ua-mobile"),
            "sec-ch-ua-platform": session.headers.get("sec-ch-ua-platform"),
        }

        data_post2 = {
            "inscricaoEstadual": self._format_inscEstadual(guia.ie),
            "pagn": "",
            "codgOrgao": "",
            "corona": "",
            "tipoTributo": "",
            "pjInscrita": "true",
            "ipContribuinte": self._get_local_ip,
            "portaContribuinte": self._get_port()
        }

        response_post2 = session.post(self.paths.get("url2"), headers=headers_step3, data=data_post2)

        # Verifica se deu certo
        if response_post2.status_code != 200:
            return False

        data = self._define_data(guia)


        response_post3 = session.post(
            self.paths.get("url2"),
            data=data,
            headers={
                "Content-Type": data.content_type,
                "Referer": "https://www.sefaz.mt.gov.br/arrecadacao/darlivre/pj/gerardar",
                "Origin": "https://www.sefaz.mt.gov.br",
                "User-Agent": headers["User-Agent"]
            }
        )

        if response_post3.status_code != 200:
            return False


        pdf_response = session.get(self.paths.get("url3"))

        try:
            with open(guia.get_full_path, "wb") as f:
                f.write(pdf_response.content)
            
            print("PDF emitido: " + guia.file_name)
            return True
        except Exception as e:
            print("Message: ", e)
            return False


    def _define_data(self, guia: Guia):
        if guia.tipo == "ICMS":
            valores = self._get_valor(guia)

            return MultipartEncoder(
                fields={
                "periodoReferencia": guia.periodo,
                "tipoVenda": "1",
                "tributo": "1112",
                "cnpjBeneficiario": "",
                "cpfPrestador": "",
                "cnpjPrestador": "",
                "codgCNO": "",
                "codgProcesso": "",
                "numrDuimp": "",
                "numrDocumentoDestinatario": "",
                "notas": "1",
                "nfeNota1": "",
                "nfeNota2": "",
                "nfeNota3": "",
                "nfeNota4": "",
                "nfeNota5": "",
                "nfeNota6": "",
                "nfeNota7": "",
                "nfeNota8": "",
                "nfeNota9": "",
                "nfeNota10": "",
                "numrParcela": "",
                "totalParcela": "",
                "numrNai": "",
                "numrTad": "",
                "multaCovid": "",
                "numeroNob": "",
                "codgConvDesc": "",
                "dataVencimento": self._ajustar_data(guia.vencimento).get("date"),
                "qtd": "",
                "qtdUnMedida": "",
                "valorUnitario": "",
                "valorCampo": valores.get("valor"),
                "valorCorrecao": "0",
                "diasAtraso": valores.get("days"),
                "juros": valores.get("valor_juros"),
                "tipoDocumento": "2",
                "nota1": "",
                "nota2": "",
                "nota3": "",
                "nota4": "",
                "nota5": "",
                "nota6": "",
                "nota7": "",
                "nota8": "",
                "nota9": "",
                "nota10": "",
                "informacaoPrevista": ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes),
                "informacaoPrevista2": "",
                "municipio": self._get_mun(guia),
                "numrContribuinte": self._get_numr_contribuinte(guia),
                "pagn": "emitir",
                "numrDocumento": guia.cnpj,
                "numrInscEstadual": guia.ie,
                "tipoContribuinte": "1",
                "codgCnae": "4612500",
                "tipoTributoH": "",
                "ipContribuinte": str(self._get_local_ip()),
                "portaContribuinte": str(self._get_port()),
                "codgOrgao": "",
                "valor": valores.get("valor"),
                "valorPadrao": "0",
                "valorMulta": "",
                "tributoTad": "1112",
                "tipoVendaX": "",
                "tipoUniMedida": "",
                "valorUnit": "",
                "upfmtFethab": ""
            })
        elif guia.tipo == "DIFAL":
            valores = self._get_valor(guia)

            fields = OrderedDict([
                ("periodoReferencia", guia.periodo),
                ("tipoVenda", "1"),
                ("tributo", "1317"),
                ("cnpjBeneficiario", ""),
                ("cpfPrestador", ""),
                ("cnpjPrestador", ""),
                ("codgCNO", ""),
                ("codgProcesso", ""),
                ("numrDuimp", ""),
                ("numrDocumentoDestinatario", guia.cnpj),
                ("txtCaminhoArquivo", "")
            ])

            for i in range(10):
                fields[f"isNFE{i+1}"] = "on"
                fields[f"numrNota{i+1}"] = guia.notas[i] if i < len(guia.notas) else ""

            # Continua com os campos restantes
            fields.update(OrderedDict([
                ("numrPessoaDestinatario", self._get_numr_contribuinte(guia)),
                ("statInscricaoEstadual", "Ativo"),
                ("notas", str(len(guia.notas))),
                ("nfeNota1", ""),
                ("nfeNota2", ""),
                ("nfeNota3", ""),
                ("nfeNota4", ""),
                ("nfeNota5", ""),
                ("nfeNota6", ""),
                ("nfeNota7", ""),
                ("nfeNota8", ""),
                ("nfeNota9", ""),
                ("nfeNota10", ""),
                ("numrParcela", ""),
                ("totalParcela", ""),
                ("numrNai", ""),
                ("numrTad", ""),
                ("multaCovid", ""),
                ("numeroNob", ""),
                ("codgConvDesc", ""),
                ("dataVencimento", self._ajustar_data(guia.vencimento).get("date")),
                ("qtd", ""),
                ("qtdUnMedida", ""),
                ("valorUnitario", ""),
                ("valorCampo", valores.get("valor")),
                ("valorCorrecao", "0"),
                ("diasAtraso", valores.get("days")),
                ("juros", valores.get("valor_juros")),
                ("tipoDocumento", "2"),
                ("nota1", ""),
                ("nota2", ""),
                ("nota3", ""),
                ("nota4", ""),
                ("nota5", ""),
                ("nota6", ""),
                ("nota7", ""),
                ("nota8", ""),
                ("nota9", ""),
                ("nota10", ""),
                ("informacaoPrevista", ObservationOfPaymentSlipService.generate_text(
                    guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes)),
                ("informacaoPrevista2", ""),
                ("municipio", self._get_mun(guia)),
                ("numrContribuinte", self._get_numr_contribuinte(guia)),
                ("pagn", "emitir"),
                ("numrDocumento", guia.cnpj),
                ("numrInscEstadual", guia.ie),
                ("tipoContribuinte", "1"),
                ("codgCnae", "4612500"),
                ("tipoTributoH", ""),
                ("ipContribuinte", str(self._get_local_ip())),
                ("portaContribuinte", str(self._get_port())),
                ("codgOrgao", ""),
                ("valor", valores.get("valor")),
                ("valorPadrao", "0"),
                ("valorMulta", valores.get("valor_multa")),
                ("tributoTad", "1317"),
                ("tipoVendaX", ""),
                ("tipoUniMedida", ""),
                ("valorUnit", ""),
                ("upfmtFethab", "0"),
                ("descSubTributo", "0.0")
                ]))
            return MultipartEncoder(fields=fields)
        elif guia.tipo == "ST":
            valores = self._get_valor(guia)
            
            fields = OrderedDict([
            ("periodoReferencia", guia.periodo),
            ("tipoVenda", "2"),
            ("tributo", "2817"),
            ("cnpjBeneficiario", ""),
            ("cpfPrestador", ""),
            ("cnpjPrestador", ""),
            ("codgCNO", ""),
            ("codgProcesso", ""),
            ("numrDuimp", ""),
            ("numrDocumentoDestinatario", guia.cnpj),
            ("txtCaminhoArquivo", "")
            ])

            for i in range(10):
                fields[f"isNFE{i+1}"] = "on"
                fields[f"numrNota{i+1}"] = guia.notas[i] if i < len(guia.notas) else ""

            # Continua com os campos restantes
            fields.update(OrderedDict([
                ("numrPessoaDestinatario", self._get_numr_contribuinte(guia)),
                ("statInscricaoEstadual", "Ativo"),
                ("notas", str(len(guia.notas))),
                ("nfeNota1", ""),
                ("nfeNota2", ""),
                ("nfeNota3", ""),
                ("nfeNota4", ""),
                ("nfeNota5", ""),
                ("nfeNota6", ""),
                ("nfeNota7", ""),
                ("nfeNota8", ""),
                ("nfeNota9", ""),
                ("nfeNota10", ""),
                ("numrParcela", ""),
                ("totalParcela", ""),
                ("numrNai", ""),
                ("numrTad", ""),
                ("multaCovid", ""),
                ("numeroNob", ""),
                ("codgConvDesc", ""),
                ("dataVencimento", self._ajustar_data(guia.vencimento).get("date")),
                ("qtd", ""),
                ("qtdUnMedida", ""),
                ("valorUnitario", ""),
                ("valorCampo", valores.get("valor")),
                ("valorCorrecao", "0"),
                ("diasAtraso", valores.get("days")),
                ("juros", valores.get("valor_juros")),
                ("tipoDocumento", "2"),
                ("nota1", ""),
                ("nota2", ""),
                ("nota3", ""),
                ("nota4", ""),
                ("nota5", ""),
                ("nota6", ""),
                ("nota7", ""),
                ("nota8", ""),
                ("nota9", ""),
                ("nota10", ""),
                ("informacaoPrevista", ObservationOfPaymentSlipService.generate_text(
                    guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes)),
                ("informacaoPrevista2", ""),
                ("municipio", self._get_mun(guia)),
                ("numrContribuinte", self._get_numr_contribuinte(guia)),
                ("pagn", "emitir"),
                ("numrDocumento", guia.cnpj),
                ("numrInscEstadual", guia.ie),
                ("tipoContribuinte", "1"),
                ("codgCnae", "4612500"),
                ("tipoTributoH", ""),
                ("ipContribuinte", str(self._get_local_ip())),
                ("portaContribuinte", str(self._get_port())),
                ("codgOrgao", ""),
                ("valor", valores.get("valor")),
                ("valorPadrao", "0"),
                ("valorMulta", valores.get("valor_multa")),
                ("tributoTad", "2817"),
                ("tipoVendaX", ""),
                ("tipoUniMedida", ""),
                ("valorUnit", ""),
                ("upfmtFethab", "0.0"),
                ("descSubTributo", "")
            ]))
            return MultipartEncoder(fields=fields)
