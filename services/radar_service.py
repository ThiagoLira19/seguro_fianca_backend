import requests
import html
import xml.etree.ElementTree as ET
import xmltodict

class RadarService:
    def radar_calculator(data):
        
        try:
            # URL do endpoint SOAP
            url = "https://calculation-0326.nprod.rl.ec1.aws.aztec.cloud.allianz/calculation/default/DpoService.svc"

            # Cabeçalhos HTTP
            headers = {
                "Content-Type": "application/soap+xml; charset=utf-8",
                "x-apikey-cc": "NEzzclX91hGdb6xlbhZTYt9FzLG2jDR"
            }

            xml_input = f"""
            <root>
                <rateIn>
                    <id value="14"/>
                    <uuid value="4af02b27-ee5e-4242-8d0b-d324e154a197"/>
                    <Numero_Cotacao value="14280900"/>
                    <Data_Hora_Cotacao value="2026-06-01 02:28:20"/>
                    <Codigo_Mediador value=""/>
                    <Nome_Mediador value=""/>
                    <Email_Mediador value=""/>
                    <Telefone_Mediador value=""/>
                    <Nome_Locatario value="Thiago Lira da Silva"/>
                    <CPF_Locatario value="10442856725"/>
                    <Email_Locatario value="thiago.silva1@allianz.com.br"/>
                    <Telefone_Locatario value="21967488394"/>
                    <CEP_Locatario value="23012220"/>
                    <Logradouro_Locatario value="Rua Robert Reid Kalley, Santíssimo"/>
                    <Numero_Logradouro_Locatario value="11"/>
                    <Complemento_Logradouro_Locatario value=""/>
                    <Cidade_Locatario value="Rio de Janeiro"/>
                    <Estado_Locatario value="RJ"/>
                    <Score value="0.0"/>
                    <Pendencia_Financeira value="0.0"/>
                    <Nome_Locador value="Thiago Lira da Silva"/>
                    <CPF_Locador value="10442856725"/>
                    <Email_Locador value="thiago.silva1@allianz.com.br"/>
                    <Telefone_Locador value="21967488394"/>
                    <CEP_Locador value="23012220"/>
                    <Logradouro_Locador value="Rua Robert Reid Kalley, Santíssimo"/>
                    <Numero_Logradouro_Locador value="11"/>
                    <Complemento_Logradouro_Locador value=""/>
                    <Cidade_Locador value="Rio de Janeiro"/>
                    <Estado_Locador value="RJ"/>
                    <Tipo_Seguro value="NB"/>
                    <Apolice_Anterior value=""/>
                    <tipo_locacao value="COMERCIAL"/>
                    <CEP_Risco value="21240330"/>
                    <Logradouro_Risco value="Rua Tales de Carvalho, Jardim América"/>
                    <Numero_Logradouro_Risco value="34"/>
                    <Complemento_Risco value=""/>
                    <Cidade_Risco value="Rio de Janeiro"/>
                    <Estado_Risco value="RJ"/>
                    <Data_Inicio_Vigencia value="2026-06-01"/>
                    <Data_Fim_Vigencia value="31/05/2027"/>
                    <Periodo value="12"/>
                    <IS_Aluguel value="{data['IS_Aluguel']}"/>
                    <IS_IPTU value="{data['IS_IPTU']}"/>
                    <IS_Condominio value="{data['IS_Condominio']}"/>
                    <IS_Agua value="{data['IS_Agua']}"/>
                    <IS_Energia_Eletrica value="{data['IS_Energia_Eletrica']}"/>
                    <IS_Gas value="{data['IS_Gas']}"/>
                    <IS_Danos_Imovel value="{data['IS_Danos_Imovel']}"/>
                    <IS_Pintura_Interna value="{data['IS_Pintura_Interna']}"/>
                    <IS_Pintura_Externa value="{data['IS_Pintura_Externa']}"/>
                    <IS_Multa_Recisoria value="{data['IS_Multa_Recisoria']}"/>
                    <Numero_Apolice value=""/>
                    <Data_Hora_Emissao value=""/>
                    <Pacote value=""/>
                    <Tipo_Pagamento value=""/>
                    <Quantidade_Parcelas value=""/>
                    <Juros_Pagamento value=""/>
                    <Taxa_Juros_Pagamento value=""/>
                    <Premio_Total value=""/>
                    <Comissao value=""/>
                    <Desconto_Cap value=""/>
                    <IOF value=""/>
                    <LMG_Aluguel value=""/>
                    <LMG_IPTU value=""/>
                    <LMG_Condominio value=""/>
                    <LMG_Agua value=""/>
                    <LMG_Energia_Eletrica value=""/>
                    <LMG_Gas value=""/>
                    <LMG_Danos_Imovel value=""/>
                    <LMG_Pintura_Interna value=""/>
                    <LMG_Pintura_Externa value=""/>
                    <LMG_Multa_Recisoria value=""/>
                    <Premio_Aluguel value=""/>
                    <Premio_IPTU value=""/>
                    <Premio_Condominio value=""/>
                    <Premio_Agua value=""/>
                    <Premio_Energia_Eletrica value=""/>
                    <Premio_Gas value=""/>
                    <Premio_Danos_Imovel value=""/>
                    <Premio_Pintura_Interna value=""/>
                    <Premio_Pintura_Externa value=""/>
                    <Premio_Multa_Recisoria value=""/>
                    <Premio_Total_Liquido value=""/>
                    <Status value="Aguardando processamento da cotacao"/>
                </rateIn>
            </root>            
            """

            # Corpo da solicitação SOAP
            soap_body = f"""
                <env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
                <env:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
                    <wsa:Action>http://towerswatson.com/rto/dpo/services/2010/01/DpoServiceContract/GetPofWithKey</wsa:Action>
                    <wsa:MessageID>urn:uuid:9e31474c-6072-47df-ae0d-b7dc75cc38d3</wsa:MessageID>
                </env:Header>
                <env:Body>
                    <ns2:PofRequestUsingKey xmlns:ns2="http://towerswatson.com/rto/dpo/services/2010/01" xmlns:ns3="http://towerswatson.com/rto/smf/types/2010/01">
                        <ns2:KeyName>Allianz_Tarifa_fianca_Bra</ns2:KeyName>
                        <ns2:KeyRequestTime>2026-06-11T00:00:00.000</ns2:KeyRequestTime>
                        <ns2:PofrCollection>
                            <ns3:PofrInformationDataContract>
                                <ns3:Pofr>
                                    <![CDATA[
                                    {xml_input}
                                    ]]>
                                </ns3:Pofr>
                            </ns3:PofrInformationDataContract>
                        </ns2:PofrCollection>
                        </ns2:PofRequestUsingKey>
                        </env:Body>
                        </env:Envelope>
                        """
            
            # Enviar a solicitação SOAP
            response = requests.post(url, data=soap_body, headers=headers, verify=False)

            # Verificar a resposta
            if response.status_code == 200:
                try:
                    # Parsear a resposta SOAP como XML
                    root = ET.fromstring(response.text)

                    # Definir os namespaces usados no XML
                    namespaces = {
                        's': 'http://www.w3.org/2003/05/soap-envelope',
                        'b': 'http://towerswatson.com/rto/smf/types/2010/01',
                        '': 'http://towerswatson.com/rto/dpo/services/2010/01'
                    }

                    # Encontrar a tag <b:Pof>
                    pof_tag = root.find(".//b:Pof", namespaces)

                    if pof_tag is not None:
                        # Decodificar o conteúdo da tag <b:Pof>
                        decoded_content = html.unescape(pof_tag.text)

                        # Função para simplificar o dicionário removendo o prefixo '@'
                        def simplify_dict(path, key, value):
                            # Remove o prefixo '@' dos atributos
                            if key.startswith('@'):
                                key = key[1:]  # Remove o '@'
                            return key, value
                        
                        # Função para simplificar o dicionário, transformando "value" em valores simples
                        def flatten_dict(d):
                            if isinstance(d, dict):
                                # Se o dicionário contém apenas a chave "value", retorna o valor
                                if "value" in d and len(d) == 1:
                                    return d["value"]
                                # Caso contrário, processa recursivamente
                                return {k: flatten_dict(v) for k, v in d.items()}
                            elif isinstance(d, list):
                                # Processa cada item da lista recursivamente
                                return [flatten_dict(item) for item in d]
                            else:
                                # Retorna o valor diretamente se não for um dicionário ou lista
                                return d
                        
                        # Converter o XML em um dicionário
                        xml_dict = xmltodict.parse(decoded_content, postprocessor=simplify_dict)

                        # Achatar o dicionário para simplificar os valores
                        flattened_dict = flatten_dict(xml_dict)
                        
                        return flattened_dict
                    else:
                        return {"success": False, "message": f"Xml output do Radar vazio: {e}"}
                except ET.ParseError as e:
                    return {"success": False, "message": f"Erro ao decodificar Xml output do Radar: {e}"}
            else:
                print(f"Erro na chamada do Radar! Código de status: {response.status_code}")
                print("Detalhes do erro:")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return []
        except ValueError as e:
            print(f"Erro ao processar a resposta: {e}")
            return []
