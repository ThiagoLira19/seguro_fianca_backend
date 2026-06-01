from flask import Flask, jsonify, render_template, request, Response, make_response
from flask_cors import CORS
import pandas as pd
import xml.etree.ElementTree as ET
from models.tabela_seguros import TabelaSegurosModel

app = Flask(__name__)

# Configurar CORS para permitir todas as origens
CORS(app)

# Caminho para o banco de dados SQLite
db_path = "database/dados_fianca.db"

# Instanciar o modelo
tabela_seguros = TabelaSegurosModel(db_path)

@app.route('/')
def home():
    return jsonify({'status_api': 'OK'})

@app.route('/nova_cotacao', methods=['POST'])
def new_quote():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    # Dicionário esperado (valores obrigatórios)
    required_fields = [
        "Nome_Locatario", "CPF_Locatario", "Email_Locatario", "Telefone_Locatario",
        "CEP_Locatario", "Logradouro_Locatario", "Numero_Logradouro_Locatario",
        "Complemento_Logradouro_Locatario", "Cidade_Locatario", "Estado_Locatario",
        "Nome_Locador", "CPF_Locador", "Email_Locador", "Telefone_Locador",
        "CEP_Locador", "Logradouro_Locador", "Numero_Logradouro_Locador",
        "Complemento_Logradouro_Locador", "Cidade_Locador", "Estado_Locador",
        "CEP_Risco", "Logradouro_Risco", "Numero_Logradouro_Risco",
        "Complemento_Risco", "Cidade_Risco", "Estado_Risco",
        "Data_Inicio_Vigencia", "Data_Fim_Vigencia", "Periodo",
        "IS_Aluguel", "IS_IPTU", "IS_Condominio", "IS_Agua",
        "IS_Energia_Eletrica", "IS_Gas", "IS_Danos_Imovel",
        "IS_Pintura_Interna", "IS_Pintura_Externa", "IS_Multa_Recisoria",
        "Tipo_Seguro", "tipo_locacao"
    ]

    # Verifica se todos os campos obrigatórios estão presentes
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Campo obrigatório ausente: {field}"}), 400

    # Preenche os valores obrigatórios com os dados recebidos
    dados = {field: data.get(field) for field in required_fields}

    # Adiciona os valores não obrigatórios com valores padrão
    dados.update({
        "Codigo_Mediador": data.get("Codigo_Mediador", ""),
        "Nome_Mediador": data.get("Nome_Mediador", ""),
        "Email_Mediador": data.get("Email_Mediador", ""),
        "Telefone_Mediador": data.get("Telefone_Mediador", ""),
        "Score": data.get("Score", 0),
        "Pendencia_Financeira": data.get("Pendencia_Financeira", 0),
        "Apolice_Anterior": data.get("Apolice_Anterior", None),
        "Numero_Cotacao": data.get("Numero_Cotacao", None),
        "Status": data.get("Status", "Aguardando processamento da cotacao")
    })

    result = tabela_seguros.inserir_dados(dados)

    # Retorna uma resposta
    return result

@app.route('/meus_pedidos_cotacoes', methods=['POST'])
def get_my_requested_quotes():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    cod_mediador = data.get("cod_mediador", "")

    result = tabela_seguros.listar_cotacoes("")

    return result


@app.route('/download_xml', methods=['POST'])
def download_xml():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    numero_cotacao = data.get("cotacao", "")

    result = tabela_seguros.buscar_cotacao(numero_cotacao)

    # Converter JSON para XML
    root = ET.Element("root")  # Elemento raiz

    for item in result:
        rateIn = ET.SubElement(root, "rateIn")  # Cada item será um <rateIn>
        for key, value in item.items():
            # Adiciona cada chave como um subelemento do pedido
            sub_element = ET.SubElement(rateIn, key)
            sub_element.set("value", str(value) if value is not None else "")  # Adicionar o atributo "value"

    # Converte o XML para string
    xml_content = ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

    # Cria uma resposta com o conteúdo XML
    response = make_response(xml_content)
    response.headers['Content-Type'] = 'application/xml'  # Define o tipo de conteúdo como XML
    #response.headers['Content-Disposition'] = 'attachment; filename=meus_pedidos.xml'  # Define o nome do arquivo para download

    return xml_content

if __name__ == '__main__':
    app.run(debug=True)