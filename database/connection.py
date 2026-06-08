import time
#import sqlite3
import psycopg2

class DatabaseConnection:
    def connect(self):
        """
        Cria e retorna uma conexão com o banco de dados.
        """
        try:
            #conn = sqlite3.connect(self.db_path)
            # conn = psycopg2.connect(
            #     host="data-science-ia.com.br",
            #     port=5432,
            #     database="seguro_fianca",
            #     user="admin",
            #     password="151651asc2026asasdfds@"
            # )
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="seguro_fianca",
                user="postgres",
                password="test"
            )
            return conn
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def execute_write(self, query):
        """
        Executa uma consulta de escrita (INSERT, UPDATE, DELETE).
        :param query: A consulta SQL a ser executada.
        :param params: Parâmetros para a consulta (opcional).
        :return: Dicionário com o status da operação.
        """
        try:
            conn = self.connect()
            if conn:

                cursor = conn.cursor()
                cursor.execute(query)
   
                id_cotacao = cursor.fetchone()[0]  # Supondo que o ID retornado seja a chave primária
                conn.commit()
                # Gerar o valor para Numero_Cotacao
                numero_cotacao = f"{id_cotacao}{str(int(time.time()))[-6:]}"
                # Atualizar a tabela com o Numero_Cotacao
                query_update = """
                    UPDATE tb_fianca
                    SET Numero_Cotacao = %s
                    WHERE id = %s;
                """
                cursor.execute(query_update, (numero_cotacao, id_cotacao))
                conn.commit()

                return {"success": True, "message": "Operação executada com sucesso."}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Erro ao executar a consulta: {e}"}
        finally:
            if conn:
                conn.close()

    def execute_read(self, query):
        """
        Executa uma consulta de leitura (SELECT).
        :param query: A consulta SQL a ser executada.
        :param params: Parâmetros para a consulta (opcional).
        :return: Dicionário com o status da operação e os resultados.
        """
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                
                cursor.execute(query)

                # Obtém os nomes das colunas
                colunas = [desc[0] for desc in cursor.description]

                resultados = cursor.fetchall()

                # Converte os resultados para uma lista de dicionários
                cotacoes = [dict(zip(colunas, row)) for row in resultados]

                return cotacoes
            
        except psycopg2.Error as e:
            return {"success": False, "message": f"Erro ao executar a consulta: {e}"}
        finally:
            if conn:
                conn.close()