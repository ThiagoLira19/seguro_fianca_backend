from flask import Flask, json, jsonify, render_template, request, Response, make_response
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
def nova_cotacao():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    # # Define o caminho e o nome do arquivo onde o JSON será salvo
    # file_path = 'nova_cotacao.json'

    #     # Salva o JSON em um arquivo
    # with open(file_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(data, json_file, ensure_ascii=False, indent=4)

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
        "Apolice_Anterior": data.get("Apolice_Anterior", "NULL"),
        "Numero_Cotacao": data.get("Numero_Cotacao", "NULL"),
        "Status": data.get("Status", "Aguardando processamento da cotacao")
    })

    result = tabela_seguros.inserir_dados(dados)

    # Retorna uma resposta
    return result

@app.route('/list_by_cod_mediador_and_status', methods=['POST'])
def get_cotacoes_por_mediador_e_status():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    cod_mediador = data.get("cod_mediador", "")

    status = data.get("status", "")

    result = tabela_seguros.listar_cotacoes(cod_mediador="", status=status)

    return jsonify(result)

@app.route('/download_json', methods=['POST'])
def download_json():
    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    # Obtém o número da cotação enviado no corpo da requisição
    numero_cotacao = data.get("cotacao", "")

    # Busca os dados da cotação na tabela de seguros
    result = tabela_seguros.buscar_cotacao(numero_cotacao)

    # Verifica se há resultados
    if not result:
        # Retorna uma mensagem de erro caso não encontre a cotação
        return jsonify({"error": f"Cotação {numero_cotacao} não encontrada."}), 404

    # Retorna os dados da cotação como JSON
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)