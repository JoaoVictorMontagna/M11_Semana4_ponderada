import os
import time
import clickhouse_connect
from dotenv import load_dotenv
from config import settings

# Carrega variáveis do .env
load_dotenv()

# Conexão global ao ClickHouse
def conectar_clickhouse():
    """Conecta ao ClickHouse usando variáveis do .env."""
    try:
        client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            secure=settings.CLICKHOUSE_SECURE
        )
        print("✅ Conectado ao ClickHouse com sucesso!")
        return client
    except Exception as e:
        print(f"❌ Erro ao conectar ao ClickHouse: {e}")
        return None

# Criar a conexão global ao iniciar o módulo
client = conectar_clickhouse()

def get_prata_total_count():
    """ Retorna o total de registros na tabela 'prata_events' e a latência da consulta. """
    try:
        if not client:
            return {"error": "Falha na conexão com ClickHouse"}
        
        start = time.time()
        query = "SELECT COUNT(*) FROM prata_events;"
        result = client.query(query).result_rows
        end = time.time()
        
        latency_ms = round((end - start) * 1000, 2)
        return {"table": "prata_events", "total_count": result[0][0], "latency_ms": latency_ms}
    except Exception as e:
        return {"error": str(e)}

def get_prata_peak_hours():
    """ Retorna a contagem de registros por hora (pico de inserção) e a latência da consulta. """
    try:
        if not client:
            return {"error": "Falha na conexão com ClickHouse"}
        
        start = time.time()
        query = """
            SELECT toStartOfHour(timestamp) AS hora, COUNT(*) AS total
            FROM prata_events 
            GROUP BY hora
            ORDER BY hora
        """  # Removido FORMAT JSON;

        result = client.query(query).result_rows
        end = time.time()
        
        latency_ms = round((end - start) * 1000, 2)
        peak_hours = {str(row[0]): row[1] for row in result}
        return {"table": "prata_events", "peak_hours": peak_hours, "latency_ms": latency_ms}
    except Exception as e:
        return {"error": str(e)}


def get_prata_last_update():
    """ Retorna a data da última atualização na tabela 'prata_events' e a latência da consulta. """
    try:
        if not client:
            return {"error": "Falha na conexão com ClickHouse"}
        
        start = time.time()
        query = "SELECT MAX(timestamp) FROM prata_events;"
        result = client.query(query).result_rows
        end = time.time()
        
        latency_ms = round((end - start) * 1000, 2)
        return {"table": "prata_events", "last_update": result[0][0], "latency_ms": latency_ms}
    except Exception as e:
        return {"error": str(e)}
