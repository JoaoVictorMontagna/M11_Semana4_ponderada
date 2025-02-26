from Supabase.bronze.bronze_metrics import get_bronze_total_count
from Supabase.bronze.bronze_metrics import get_bronze_peak_hours
from Supabase.logs.logs_metrics import get_logs_total_count
from Supabase.logs.logs_metrics import get_logs_peak_hours
from Clickhouse.Prata import prata_metrics

def main():
    bronze_count = get_bronze_total_count()
    bronze_peak_hours = get_bronze_peak_hours()

    print("Metricas da tabela 'bronze':")
    print(bronze_count)
    print(bronze_peak_hours)



    logs_count = get_logs_total_count()
    logs_peak_count = get_logs_peak_hours()
    print("Métricas da tabela 'logs':")
    print(logs_count)
    print(logs_peak_count)


    prata_count = prata_metrics.get_prata_total_count()
    print("Métricas da tabela 'prata_events':", prata_count)
    # Picos de inserção por hora
    prata_peak = prata_metrics.get_prata_peak_hours()
    print("Picos de inserção na tabela 'prata_events':", prata_peak)
    # Última atualização na tabela 'prata_events'







if __name__ == "__main__":
    main()
