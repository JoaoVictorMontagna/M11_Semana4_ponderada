import os
import time
from supabase import create_client
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime

# Carrega as variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Cria o cliente do Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_bronze_total_count():
    """
    Retorna:
      - Total de registros na tabela 'bronze'.
      - Latência da query (em milissegundos).
    """
    try:
        start = time.time()
        response = supabase.table("bronze").select("*").execute()
        end = time.time()
        latency_ms = round((end - start) * 1000, 2)
        total_count = len(response.data) if response.data else 0
        return {
            "table": "bronze",
            "total_count": total_count,
            "latency_ms": latency_ms
        }
    except Exception as e:
        return {"error": str(e)}

def get_bronze_peak_hours():
    """
    Retorna a contagem de registros agrupados por hora (picos de inserção).
    """
    try:
        start = time.time()
        response = supabase.table("bronze").select("created_at").execute()
        end = time.time()
        latency_ms = round((end - start) * 1000, 2)

        if not response.data:
            return {
                "table": "bronze",
                "peak_hours": {},
                "latency_ms": latency_ms
            }

        # Agrupar registros por hora
        timestamps = [datetime.fromisoformat(item["created_at"]) for item in response.data if "created_at" in item]
        peak_hours = Counter(t.strftime("%Y-%m-%d %H:00") for t in timestamps)

        return {
            "table": "bronze",
            "peak_hours": dict(peak_hours),
            "latency_ms": latency_ms
        }

    except Exception as e:
        return {"error": str(e)}
