import streamlit as st
import pandas as pd
import plotly.express as px
from Clickhouse.Prata import prata_metrics
from Supabase.bronze import bronze_metrics
from Supabase.logs import logs_metrics

# Configuração inicial do layout
st.set_page_config(
    page_title="Dashboard de Telemetria",
    page_icon="📊",
    layout="wide"
)

# Função para carregar dados
def carregar_dados():
    """Obtém métricas do Supabase e ClickHouse"""
    return {
        "bronze": {
            "total": bronze_metrics.get_bronze_total_count(),
            "picos": bronze_metrics.get_bronze_peak_hours()
        },
        "logs": {
            "total": logs_metrics.get_logs_total_count(),
            "picos": logs_metrics.get_logs_peak_hours()
        },
        "prata_events": {
            "total": prata_metrics.get_prata_total_count(),
            "picos": prata_metrics.get_prata_peak_hours()
        }
    }

# Carregar os dados
dados = carregar_dados()

# Estilização do dashboard
st.markdown("""
    <style>
        .metric-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Criar colunas para KPIs
st.markdown("<div class='header'>📊 Métricas Gerais</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Exibir indicadores de total de registros
col1.metric(label="Total de Registros (Bronze)", value=dados["bronze"]["total"]["total_count"])
col2.metric(label="Total de Registros (Logs)", value=dados["logs"]["total"]["total_count"])
col3.metric(label="Total de Registros (Prata Events)", value=dados["prata_events"]["total"]["total_count"])

st.markdown("---")

# Criar colunas para latência
st.markdown("<div class='header'>⏳ Latência das Consultas</div>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)

# Exibir indicadores de latência
col4.metric(label="Latência (Bronze)", value=f"{dados['bronze']['total']['latency_ms']} ms")
col5.metric(label="Latência (Logs)", value=f"{dados['logs']['total']['latency_ms']} ms")
col6.metric(label="Latência (Prata Events)", value=f"{dados['prata_events']['total']['latency_ms']} ms")

st.markdown("---")

# Função para criar gráfico de picos de inserção
def criar_grafico_picos(dados_picos, titulo):
    """Cria gráfico de picos de inserção por hora"""
    if not dados_picos["peak_hours"]:
        st.warning(f"Sem dados disponíveis para {titulo}.")
        return
    df = pd.DataFrame(list(dados_picos["peak_hours"].items()), columns=["Hora", "Registros"])
    df["Hora"] = pd.to_datetime(df["Hora"])
    fig = px.line(df, x="Hora", y="Registros", title=titulo, markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Criar layout de gráficos
st.markdown("<div class='header'>📈 Picos de Inserção</div>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)

# Exibir gráficos de picos de inserção
with col7:
    criar_grafico_picos(dados["bronze"]["picos"], "Picos de Inserção - Bronze")
with col8:
    criar_grafico_picos(dados["logs"]["picos"], "Picos de Inserção - Logs")
with col9:
    criar_grafico_picos(dados["prata_events"]["picos"], "Picos de Inserção - Prata Events")

st.markdown("---")

# Botão para atualizar dados
if st.button("🔄 Atualizar Dados"):
    dados = carregar_dados()
    st.rerun()
