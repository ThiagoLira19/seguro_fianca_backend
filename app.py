from flask import Flask, json, jsonify, render_template, request, Response, make_response
from flask_cors import CORS
from flasgger import Swagger
from models.tabela_seguros import TabelaSegurosModel
from services.radar_service import RadarService
import subprocess
import hmac
import hashlib

app = Flask(__name__)

# Configuração personalizada do Swagger
swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "API de Seguros Fiança",
        "description": "Documentação da API de Seguros Fiança. Aqui você encontra os endpoints disponíveis e como utilizá-los.",
        "version": "1.0.0",
        "termsOfService": "https://www.Allianz.com/termos",
        "contact": {
            "name": "Equipe de Suporte",
            "url": "https://www.Allianz.com/",
            "email": "suporte@allianz.com"
        },
        "license": {
            "name": "Licença MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "host": "localhost:5000",  # Altere para o domínio ou IP do servidor em produção
    "basePath": "/",  # Caminho base para os endpoints
    "schemes": ["http", "https"],
    "operationId": "getmyData",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Adicione o token no formato: Bearer <seu_token>"
        }
    },
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Todos os endpoints serão incluídos
            "model_filter": lambda tag: True,  # Todos os modelos serão incluídos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",  # Rota onde a documentação Swagger será exibida
    "headers": []  # Lista vazia para evitar o erro
}

swagger = Swagger(app, config=swagger_config)

# Configurar CORS para permitir todas as origens
CORS(app)

# Caminho para o banco de dados SQLite
db_path = "database/dados_fianca.db"

# Instanciar o modelo
tabela_seguros = TabelaSegurosModel(db_path)

@app.route('/health', methods=['GET'])
def home():
    """
    Retorna o status da API
    ---
    tags:
      - Endpoints
    responses:
      200:
        description: Retorna o status da API
        schema:
          type: object
          properties:
            status:
              type: string
              description: Status da API
    """

    return jsonify({
        "status": "API está funcionando v1.0"
    }), 200

@app.route('/nova_cotacao', methods=['POST'])
def nova_cotacao():
    """
    Cria uma nova cotação e chama o Radar para o cálculo.
    ---
    tags:
      - Endpoints
    parameters:
      - name: body
        in: body
        required: true
        description: Dados necessários para criar a cotação
        schema:
          type: object
          properties:
            Nome_Locatario:
                type: string
                description: Nome do locatário
                example: "João da Silva"
            CPF_Locatario:
                type: string
                description: CPF do locatário
                example: "123.456.789-00"
            Email_Locatario:
                type: string
                description: E-mail do locatário
                example: "joao.silva@email.com"
            Telefone_Locatario:
                type: string
                description: Telefone do locatário
                example: "(11) 98765-4321"
            CEP_Locatario:
                type: string
                description: CEP do locatário
                example: "12345-678"
            Logradouro_Locatario:
                type: string
                description: Logradouro do locatário
                example: "Rua das Flores"
            Numero_Logradouro_Locatario:
                type: string
                description: Número do logradouro do locatário
                example: "123"
            Complemento_Logradouro_Locatario:
                type: string
                description: Complemento do logradouro do locatário
                example: "Apto 45"
            Cidade_Locatario:
                type: string
                description: Cidade do locatário
                example: "São Paulo"
            Estado_Locatario:
                type: string
                description: Estado do locatário
                example: "SP"
            Nome_Locador:
                type: string
                description: Nome do locador
                example: "Maria Oliveira"
            CPF_Locador:
                type: string
                description: CPF do locador
                example: "987.654.321-00"
            Email_Locador:
                type: string
                description: E-mail do locador
                example: "maria.oliveira@email.com"
            Telefone_Locador:
                type: string
                description: Telefone do locador
                example: "(21) 99876-5432"
            CEP_Locador:
                type: string
                description: CEP do locador
                example: "54321-987"
            Logradouro_Locador:
                type: string
                description: Logradouro do locador
                example: "Avenida Central"
            Numero_Logradouro_Locador:
                type: string
                description: Número do logradouro do locador
                example: "456"
            Complemento_Logradouro_Locador:
                type: string
                description: Complemento do logradouro do locador
                example: "Casa 2"
            Cidade_Locador:
                type: string
                description: Cidade do locador
                example: "Rio de Janeiro"
            Estado_Locador:
                type: string
                description: Estado do locador
                example: "RJ"
            CEP_Risco:
                type: string
                description: CEP do risco
                example: "67890-123"
            Logradouro_Risco:
                type: string
                description: Logradouro do risco
                example: "Rua do Sol"
            Numero_Logradouro_Risco:
                type: string
                description: Número do logradouro do risco
                example: "789"
            Complemento_Risco:
                type: string
                description: Complemento do logradouro do risco
                example: "Galpão"
            Cidade_Risco:
                type: string
                description: Cidade do risco
                example: "Campinas"
            Estado_Risco:
                type: string
                description: Estado do risco
                example: "SP"
            Data_Inicio_Vigencia:
                type: string
                description: Data de início da vigência
                example: "2026-06-01"
            Data_Fim_Vigencia:
                type: string
                description: Data de fim da vigência
                example: "2027-06-01"
            Periodo:
                type: string
                description: Período do seguro
                example: "12"
            IS_Aluguel:
                type: string
                description: Valor do seguro para aluguel
                example: "1500.00"
            IS_IPTU:
                type: string
                description: Valor do seguro para IPTU
                example: "200.00"
            IS_Condominio:
                type: string
                description: Valor do seguro para condomínio
                example: "300.00"
            IS_Agua:
                type: string
                description: Valor do seguro para água
                example: "50.00"
            IS_Energia_Eletrica:
                type: string
                description: Valor do seguro para energia elétrica
                example: "100.00"
            IS_Gas:
                type: string
                description: Valor do seguro para gás
                example: "30.00"
            IS_Danos_Imovel:
                type: string
                description: Valor do seguro para danos ao imóvel
                example: "5000.00"
            IS_Pintura_Interna:
                type: string
                description: Valor do seguro para pintura interna
                example: "1000.00"
            IS_Pintura_Externa:
                type: string
                description: Valor do seguro para pintura externa
                example: "800.00"
            IS_Multa_Recisoria:
                type: string
                description: Valor do seguro para multa rescisória
                example: "3000.00"
            Tipo_Seguro:
                type: string
                description: Tipo do seguro
                example: "Residencial"
            tipo_locacao:
                type: string
                description: Tipo de locação
                example: "Residencial"
    responses:
      200:
        description: Retorna a cotação e o resultado do cálculo do Radar
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Indica se a operação foi bem-sucedida
            data:
              type: object
              description: Dados da cotação gerada
    """

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
        "Apolice_Anterior": data.get("Apolice_Anterior", "NULL"),
        "Numero_Cotacao": data.get("Numero_Cotacao", "NULL"),
        "Status": data.get("Status", "Aguardando processamento da cotacao")
    })

    # Função para converter valores no formato brasileiro para float
    def converter_valor(valor):
        try:
            return float(valor.replace(".", "").replace(",", "."))
        except AttributeError:
            # Caso o valor não seja uma string, retorna o valor original
            return valor
        except ValueError:
            # Caso o valor não seja convertível, lança uma exceção ou retorna um valor padrão
            raise ValueError(f"Erro ao converter o valor: {valor}")

    dados.update({
            "IS_Aluguel": converter_valor(data.get("IS_Aluguel", "0")),
            "IS_IPTU": converter_valor(data.get("IS_IPTU", "0")),
            "IS_Condominio": converter_valor(data.get("IS_Condominio", "0")),
            "IS_Agua": converter_valor(data.get("IS_Agua", "0")),
            "IS_Energia_Eletrica": converter_valor(data.get("IS_Energia_Eletrica", "0")),
            "IS_Gas": converter_valor(data.get("IS_Gas", "0")),
            "IS_Danos_Imovel": converter_valor(data.get("IS_Danos_Imovel", "0")),
            "IS_Pintura_Interna": converter_valor(data.get("IS_Pintura_Interna", "0")),
            "IS_Pintura_Externa": converter_valor(data.get("IS_Pintura_Externa", "0")),
            "IS_Multa_Recisoria": converter_valor(data.get("IS_Multa_Recisoria", "0")),
        })

    result = RadarService.radar_calculator(dados)

    # Dicionário para mapear coverageId aos campos correspondentes
    coverage_mapping = {
        "1": "premio_danos_imovel",  # Danos ao Imóvel
        "2": "premio_iptu",           # IPTU
        "3": "premio_condominio",     # Condomínio
        "4": "premio_agua",           # Água
        "5": "premio_energia_eletrica",  # Energia Elétrica
        "6": "premio_gas",            # Gás
        "7": "premio_pintura_interna",  # Pintura Interna
        "8": "premio_pintura_externa",  # Pintura Externa
        "9": "premio_multa_recisoria",  # Multa Rescisória
        "10": "premio_aluguel",       # Aluguel
    }

    # Inicializa os valores das coberturas
    coberturas = {
        "premio_danos_imovel": 0.0,
        "premio_iptu": 0.0,
        "premio_condominio": 0.0,
        "premio_agua": 0.0,
        "premio_energia_eletrica": 0.0,
        "premio_gas": 0.0,
        "premio_pintura_interna": 0.0,
        "premio_pintura_externa": 0.0,
        "premio_multa_recisoria": 0.0,
        "premio_aluguel": 0.0,
    }

    # Navega até as coberturas no resultado do RadarService
    quotes = result.get("root", {}).get("rateOut", {}).get("quotes", {}).get("quoteOut", [])

    # Função para garantir que o valor seja um número válido
    def obter_valor_comercial(coverage):
        valor = coverage.get("commercialPremiumCov", 0)
        try:
            # Verifica se o valor é uma string numérica ou um número
            if isinstance(valor, (int, float)):
                return float(valor)
            elif isinstance(valor, str) and valor.replace(".", "").isdigit():
                return float(valor)
            else:
                # Retorna 0.0 caso o valor não seja válido
                return 0.0
        except (ValueError, TypeError):
            # Retorna 0.0 em caso de erro
            return 0.0

    # Função para obter as coverages do bundleId 1
    def obter_coverages_bundle1(result):
        try:
            # Navega até os quotes no resultado
            quotes = result.get("root", {}).get("rateOut", {}).get("quotes", {}).get("quoteOut", [])
            
            # Filtra o quote com bundleId igual a "1"
            for quote in quotes:
                if quote.get("bundleId") == "1":
                    # Retorna as coverages do bundleId 1
                    return quote.get("coverages", {}).get("coverageOut", [])
            
            # Retorna uma lista vazia se o bundleId 1 não for encontrado
            return []
        except Exception as e:
            raise ValueError(f"Erro ao obter coverages do bundleId 1: {e}")
        
    # Obtém as coverages do bundleId 1
    coverages_bundle1 = obter_coverages_bundle1(result)

    # Itera sobre as coberturas do primeiro bundle (ou outro bundle, conforme necessário)
    if quotes:
        coverages = coverages_bundle1
        for coverage in coverages:
            coverage_id = coverage.get("coverageId")
            if coverage_id in coverage_mapping:
                # Mapeia o valor da cobertura para o campo correspondente
                campo = coverage_mapping[coverage_id]
                coberturas[campo] = obter_valor_comercial(coverage)

    # Calcula o total líquido somando todas as coberturas
    coberturas["premio_total_liquido"] = sum(coberturas.values())

    # Atualiza o dicionário `dados` com os valores das coberturas
    dados.update(coberturas)

    tabela_seguros.inserir_dados(dados)

    # Retorna uma resposta
    return result

@app.route('/listar_por_cod_mediador_e_status', methods=['POST'])
def get_cotacoes_por_mediador_e_status():
    """
    Lista as cotações podendo filtrar por mediador e status.
    ---
    tags:
      - Endpoints
    parameters:
      - name: body
        in: body
        required: true
        description: Lista as cotações
        schema:
          type: object
          properties:
            cod_mediador:
                type: string
                description: Código do Mediador
                example: ""
            status:
                type: string
                description: status da cotação
                example: ""
    responses:
      200:
        description: Retorna os dados das cotações
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Indica se a operação foi bem-sucedida
            data:
              type: object
              description: Indica o status da requisição
    """

    # Recebe os dados do JSON enviado no corpo da requisição
    data = request.get_json()

    cod_mediador = data.get("cod_mediador", "")

    status = data.get("status", "")

    result = tabela_seguros.listar_cotacoes(cod_mediador="", status=status)

    return jsonify(result)

@app.route('/cotacoes/<numero_cotacao>', methods=['GET'])
def consultar_cotacao(numero_cotacao):
    """
    Consulta uma cotação pelo número da cotação.
    ---
    tags:
      - Endpoints
    parameters:
      - name: numero_cotacao
        in: path
        required: true
        description: Número da cotação a ser consultada
        type: string
        example: "12334566"
    responses:
      200:
        description: Retorna os dados da cotação consultada
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Indica se a operação foi bem-sucedida
            data:
              type: object
              description: Dados da cotação consultada
      404:
        description: Cotação não encontrada
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Indica se a operação foi bem-sucedida
            message:
              type: string
              description: Mensagem de erro
    """
    try:
        # Consulta os dados da cotação na tabela de seguros
        result = tabela_seguros.buscar_cotacao(numero_cotacao=numero_cotacao)

        # Verifica se há resultados
        if not result:
            return jsonify({"success": False, "message": f"Cotação {numero_cotacao} não encontrada."}), 404

        # Retorna os dados da cotação
        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        # Retorna uma mensagem de erro em caso de exceção
        return jsonify({"success": False, "message": f"Erro ao consultar a cotação: {str(e)}"}), 500

@app.route("/deploy")
def deploy():

    resultado = subprocess.run(
        """
        cd /root/app/seguro_fianca_backend &&
        git pull &&
        source venv/bin/activate &&
        pip install -r requirements.txt &&
        systemctl restart seguro-fianca
        """,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True
    )

    return jsonify({
        "codigo": resultado.returncode,
        "saida": resultado.stdout,
        "erro": resultado.stderr
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
