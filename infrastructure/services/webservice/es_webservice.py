from domain.services.i_guia_generator_service import IGuiaGeneratorService
from domain.entities.guia import Guia

import xml.etree.ElementTree as ET
import requests
import xml.dom.minidom
import base64
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

from domain.services.observation.observation_of_payment_slip import ObservationOfPaymentSlipService

class GuiaGeneratorESWebService(IGuiaGeneratorService):
    
    NS_SOAP = "http://www.w3.org/2003/05/soap-envelope"
    NS_DUAE = "http://www.sefaz.es.gov.br/duae"
    NAMESPACES = {"soap": NS_SOAP, "duae": NS_DUAE, "default": NS_DUAE}

    CODIGO_TIPO = {
        "ICMS": 1210,
        "DIFAL": 1287,
        "ST": 1384,
        "ICAU": 1279
    }

    CODIGO_MUN = {
        "01": 57053,
        "02": 56251,
        "03": 56251,
        "04": 56634,
        "06": 56995,
        "09": 57290
    }

    def __init__(self, cert_file: str = "infrastructure/certs/cert.pem",
                 key_file: str = "infrastructure/certs/chave.pem",
                 homolog: bool = False):
        self.cert_file = cert_file
        self.key_file = key_file
        self.url = (
            "https://homologacao.sefaz.es.gov.br/WsDua/DuaService.asmx"
            if homolog else
            "https://app.sefaz.es.gov.br/WsDua/DuaService.asmx"
        )
        self.headers = {"Content-Type": "application/soap+xml; charset=utf-8",
                        "SOAPAction": ""}

        # Registrar namespaces no ElementTree
        ET.register_namespace("soap", self.NS_SOAP)
        ET.register_namespace("duae", self.NS_DUAE)

    def gerar(self, guia: Guia):
        try:
            dados = self._emitir_dua(guia)
            pdf = self._obter_pdf(**dados)

            if pdf:
                return True
            else:
                return False
        except Exception as e:
            print("Exception message: ", e)
            return False


    def _enviar_requisicao(self, xml: str) -> Optional[requests.Response]:
        """Envia a requisição SOAP ao serviço DUA."""
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                data=xml,
                cert=(self.cert_file, self.key_file),
                verify=True
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print("Erro na requisição:", e)
            return None
    
    @staticmethod
    def _formatar_xml(xml_str: str) -> str:
        """Deixa o XML bonito para leitura/logs."""
        try:
            dom = xml.dom.minidom.parseString(xml_str)
            return dom.toprettyxml(indent="  ")
        except Exception:
            return xml_str
        
    # ==========================
    # Criação dos XMLs
    # ==========================

    def _criar_envelope(self, nome_operacao: str, nome_raiz: str):
        envelope = ET.Element(f"{{{self.NS_SOAP}}}Envelope")

        # Header
        header = ET.SubElement(envelope, f"{{{self.NS_SOAP}}}Header")
        dua_header = ET.SubElement(header, f"{{{self.NS_DUAE}}}DuaServiceHeader")
        ET.SubElement(dua_header, f"{{{self.NS_DUAE}}}versao").text = "1.01"

        # Body
        body = ET.SubElement(envelope, f"{{{self.NS_SOAP}}}Body")
        operacao = ET.SubElement(body, f"{{{self.NS_DUAE}}}{nome_operacao}")
        msg = ET.SubElement(operacao, f"{{{self.NS_DUAE}}}duaDadosMsg")

        raiz = ET.SubElement(msg, nome_raiz, versao="1.01", xmlns=self.NS_DUAE)
        return envelope, raiz

    def _criar_xml_dua(self, **dados) -> bytes:
        envelope, emis_dua = self._criar_envelope("duaEmissao", "emisDua")
        for k, v in dados.items():
            ET.SubElement(emis_dua, k).text = str(v)
        return ET.tostring(envelope, encoding="utf-8", xml_declaration=True)
    
    
    def _criar_xml_obter_pdf_dua(self, tpAmb, nDua, cnpj):
        envelope, obter_pdf_dua = self._criar_envelope("duaObterPdf", "obterPdfDua")
        ET.SubElement(obter_pdf_dua, "tpAmb").text = str(tpAmb)
        ET.SubElement(obter_pdf_dua, "nDua").text = nDua
        ET.SubElement(obter_pdf_dua, "cnpj").text = cnpj
        return ET.tostring(envelope, encoding="utf-8", xml_declaration=True)
    
    def _get_cMun(self, filial: str) -> Optional[int]:
        return self.CODIGO_MUN.get(filial)

    def _get_cServ(self, tipo: str) -> Optional[int]:
        return self.CODIGO_TIPO.get(tipo)


    # ==========================
    # Operações principais
    # ==========================

    def _emitir_dua(self, guia: Guia) -> Optional[Dict]:
        dados_para_gerar_xml_dua = {
            "tpAmb": 1,
            "cnpjEmi": "27080571000130", 
            "cnpjOrg": "27080571000130", 
            "cArea": 2,
            "cServ": self._get_cServ(guia.tipo),
            "cnpjPes": guia.cnpj,
            "dRef": datetime.strptime(guia.periodo, "%m/%Y").strftime("%Y-%m"),
            "dVen": datetime.strptime(guia.vencimento, "%d/%m/%Y").strftime("%Y-%m-%d"),
            "dPag": datetime.strptime(guia.vencimento, "%d/%m/%Y").strftime("%Y-%m-%d"),
            "cMun": self._get_cMun(guia.filial),
            "xInf": ObservationOfPaymentSlipService.generate_text(guia.tipo, guia.periodo, guia.uf, guia.notas, guia.fretes),
            "vRec": float(guia.valor.replace(",",".")),
            "xIde": "Referente a " + guia.tipo,
            "fPix": "true"
        }

        xml = self._criar_xml_dua(**dados_para_gerar_xml_dua).decode("utf-8")
        response = self._enviar_requisicao(xml)

        if not response:
            return None

        try:
            root = ET.fromstring(response.text)
            ret_elem = root.find(".//duae:retEmisDua", self.NAMESPACES)
            if ret_elem is None:
                return None

            nDua_elem = ret_elem.find("duae:dua/duae:nDua", self.NAMESPACES)
            if nDua_elem is None:
                return None

            # Pegar informações do XML enviado
            xml_sent = ET.fromstring(xml)
            tpAmb_elem = xml_sent.find(".//default:tpAmb", self.NAMESPACES)
            cnpj_elem = xml_sent.find(".//default:cnpjPes", self.NAMESPACES)

            return {
                "tpAmb": tpAmb_elem.text if tpAmb_elem is not None else None,
                "nDua": nDua_elem.text,
                "cnpj": cnpj_elem.text if cnpj_elem is not None else None,
                "path": guia.get_full_path
            }
        except Exception as e:
            print("Erro ao processar XML:", e)
            print("Resposta crua:\n", response.text)
            return None
        
    def _obter_pdf(self, tpAmb: str, nDua: str, cnpj: str, path: str):
        xml = self._criar_xml_obter_pdf_dua(tpAmb, nDua, cnpj)
        response = self._enviar_requisicao(xml)
        if not response:
            return False

        root = ET.fromstring(response.text)
        xpdf_elem = root.find(".//duae:xPdf", self.NAMESPACES)

        if xpdf_elem is not None and xpdf_elem.text:
            pdf_bytes = base64.b64decode(xpdf_elem.text)
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            print("PDF emitido: " + path)
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            return True
        else:
            print("Elemento xPdf não encontrado ou vazio.")
            return False

    def _consultar_dua(self, tpAmb, nDua, cnpj):
        """
        Consulta o status de uma DUA já emitida.
        """
        xml = self._criar_xml_consulta_dua(tpAmb, nDua, cnpj)
        response = self._enviar_requisicao(xml)
        if response:
            print("Status Code:", response.status_code)
            print("Resposta formatada:\n", self._formatar_xml(response.text))

    def _consultar_municipio(self, tpAmb):
        """
        Consulta os municípios disponíveis no webservice DUA.
        """
        xml = self._criar_xml_cons_municipio(tpAmb)
        response = self._enviar_requisicao(xml)
        if response:
            print("Status Code:", response.status_code)
            print("Resposta formatada:\n", self._formatar_xml(response.text))

