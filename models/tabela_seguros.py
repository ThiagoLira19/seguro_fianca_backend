from flask import json
from database.connection import DatabaseConnection
import uuid

class TabelaSegurosModel:
    def __init__(self, db_path):
        self.db = DatabaseConnection()

    def inserir_dados(self, data):
        """
        Insere dados na tabela Tabela_Seguros.
        :param dados: Dicionário com os dados a serem inseridos.
        """
        # Gerar um UUID
        data['unique_id'] = str(uuid.uuid4())
        data['IS_Aluguel'] = float(data['IS_Aluguel'])
        data['IS_IPTU'] = float(data['IS_IPTU'])
        data['IS_Condominio'] = float(data['IS_Condominio'])
        data['IS_Agua'] = float(data['IS_Agua'])
        data['IS_Energia_Eletrica'] = float(data['IS_Energia_Eletrica'])
        data['IS_Gas'] = float(data['IS_Gas'])
        data['IS_Danos_Imovel'] = float(data['IS_Danos_Imovel'])
        data['IS_Pintura_Interna'] = float(data['IS_Pintura_Interna'])
        data['IS_Pintura_Externa'] = float(data['IS_Pintura_Externa'])
        data['IS_Multa_Recisoria'] = float(data['IS_Multa_Recisoria'])

        query = f"""
        INSERT INTO tb_fianca (
            uuid, Codigo_Mediador, Nome_Mediador, Email_Mediador, Telefone_Mediador,
            Nome_Locatario, CPF_Locatario, Email_Locatario, Telefone_Locatario,
            CEP_Locatario, Logradouro_Locatario, Numero_Logradouro_Locatario,
            Complemento_Logradouro_Locatario, Cidade_Locatario, Estado_Locatario,
            Score, Pendencia_Financeira, Nome_Locador, CPF_Locador, Email_Locador,
            Telefone_Locador, CEP_Locador, Logradouro_Locador, Numero_Logradouro_Locador,
            Complemento_Logradouro_Locador, Cidade_Locador, Estado_Locador, Tipo_Seguro,
            Apolice_Anterior, tipo_locacao, CEP_Risco, Logradouro_Risco,
            Numero_Logradouro_Risco, Complemento_Risco, Cidade_Risco, Estado_Risco,
            Data_Inicio_Vigencia, Data_Fim_Vigencia, Periodo, IS_Aluguel, IS_IPTU,
            IS_Condominio, IS_Agua, IS_Energia_Eletrica, IS_Gas, IS_Danos_Imovel,
            IS_Pintura_Interna, IS_Pintura_Externa, IS_Multa_Recisoria, premio_aluguel, 
            premio_iptu, premio_condominio, premio_agua, premio_energia_eletrica,
            premio_gas, premio_danos_imovel, premio_pintura_interna, premio_pintura_externa, 
            premio_multa_recisoria, premio_total_liquido, Numero_Cotacao, Status
        ) VALUES (
            '{data["unique_id"]}', '{data["Codigo_Mediador"]}', '{data["Nome_Mediador"]}', '{data["Email_Mediador"]}', '{data["Telefone_Mediador"]}',
            '{data["Nome_Locatario"]}', '{data["CPF_Locatario"]}', '{data["Email_Locatario"]}', '{data["Telefone_Locatario"]}',
            '{data["CEP_Locatario"]}', '{data["Logradouro_Locatario"]}', '{data["Numero_Logradouro_Locatario"]}',
            '{data["Complemento_Logradouro_Locatario"]}', '{data["Cidade_Locatario"]}', '{data["Estado_Locatario"]}',
            {data["Score"]}, {data["Pendencia_Financeira"]}, '{data["Nome_Locador"]}', '{data["CPF_Locador"]}', '{data["Email_Locador"]}',
            '{data["Telefone_Locador"]}', '{data["CEP_Locador"]}', '{data["Logradouro_Locador"]}', '{data["Numero_Logradouro_Locador"]}',
            '{data["Complemento_Logradouro_Locador"]}', '{data["Cidade_Locador"]}', '{data["Estado_Locador"]}', '{data["Tipo_Seguro"]}',
            {data["Apolice_Anterior"]}, '{data["tipo_locacao"]}', '{data["CEP_Risco"]}', '{data["Logradouro_Risco"]}',
            '{data["Numero_Logradouro_Risco"]}', '{data["Complemento_Risco"]}', '{data["Cidade_Risco"]}', '{data["Estado_Risco"]}',
            '{data["Data_Inicio_Vigencia"]}', '{data["Data_Fim_Vigencia"]}', '{data["Periodo"]}', '{data["IS_Aluguel"]}', '{data["IS_IPTU"]}',
            '{data["IS_Condominio"]}', '{data["IS_Agua"]}', '{data["IS_Energia_Eletrica"]}', '{data["IS_Gas"]}', '{data["IS_Danos_Imovel"]}',
            '{data["IS_Pintura_Interna"]}', '{data["IS_Pintura_Externa"]}', '{data["IS_Multa_Recisoria"]}', 
            '{data["premio_aluguel"]}', '{data["premio_iptu"]}', '{data["premio_condominio"]}', '{data["premio_agua"]}', 
            '{data["premio_energia_eletrica"]}', '{data["premio_gas"]}', '{data["premio_danos_imovel"]}', 
            '{data["premio_pintura_interna"]}', '{data["premio_pintura_externa"]}', '{data["premio_multa_recisoria"]}', 
            '{data["premio_total_liquido"]}', {data["Numero_Cotacao"]}, '{data["Status"]}'
        ) RETURNING id;
        """
        
        return self.db.execute_write(query)
    

    def listar_cotacoes(self, cod_mediador, status):
        """
        Retorna as cotações do banco de dados com base nos filtros fornecidos em 'dados'.
        :param dados: Dicionário com os filtros para a consulta (exemplo: {"status": "ativo"}).
        :return: Lista de cotações.
        """
        if cod_mediador == "":
            cod_mediador = "%"
        else:
            cod_mediador = cod_mediador

        if status == "":
            status = "%"
        else:
            status = status

        query = f"SELECT * FROM tb_fianca WHERE Codigo_Mediador LIKE '{cod_mediador}' AND status LIKE '{status}';"

        # Executa a consulta com o parâmetro cod_mediador
        resultados = self.db.execute_read(query)

        # Retorna os dados em formato JSON
        return resultados
    

    def buscar_cotacao(self, numero_cotacao):
        """
        Retorna um cotacao do banco de dados com base nos filtros fornecidos em 'dados'.
        :param dados: Dicionário com os filtros para a consulta (exemplo: {"status": "ativo"}).
        :return: Lista de cotações.
        """
        query = f"SELECT * FROM tb_fianca WHERE Numero_Cotacao = {numero_cotacao};"

        # Executa a consulta com o parâmetro cod_mediador
        resultados = self.db.execute_read(query)

        # Retorna os dados em formato JSON
        return resultados