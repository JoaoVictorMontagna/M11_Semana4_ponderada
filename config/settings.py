import os
from dotenv import load_dotenv


# 1) Carrega o arquivo .env
load_dotenv()

# 2) Variáveis de ambiente
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
CLICKHOUSE_SECURE = os.getenv("CLICKHOUSE_SECURE", "False").lower() == "true"
CLICKHOUSE_TABLE = os.getenv("CLICKHOUSE_TABLE", "prata_events")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xxx.supabase.co")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "chave_invalida")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "fila_ingestao")