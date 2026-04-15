import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import sys
import os

# Configuración de página
st.set_page_config(page_title="Fintech Risk Monitor", layout="wide")

# Conexión a DB
db_url = "postgresql://postgres:TU_PASSWORD@localhost:5432/fintech_monitor"
engine = create_engine(db_url)

st.title("🛡️ Fintech Sentiment & Risk Monitor")
st.markdown("Monitoreo en tiempo real de salud reputacional mediante FinBERT.")

# Sidebar - KPIs de Riesgo
from src.models.risk_detector import RiskDetector
detector = RiskDetector()
metrics = detector.calculate_risk_metrics()

with st.sidebar:
    st.header("Indicadores de Alerta")
    st.metric("Nivel de Riesgo", metrics.get("risk_level", "N/A"))
    st.metric("Ratio de Negatividad", f"{metrics.get('negativity_ratio', 0)}%")
    st.write(f"Última actualización: {metrics.get('timestamp')}")

# Cuerpo Principal - Gráficas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Sentimiento")
    df_sent = pd.read_sql("SELECT sentiment_label, COUNT(*) as cantidad FROM financial_articles GROUP BY sentiment_label", engine)
    if not df_sent.empty:
        fig = px.pie(df_sent, values='cantidad', names='sentiment_label', color='sentiment_label',
                     color_discrete_map={'Positive':'#00CC96','Negative':'#EF553B','Neutral':'#636EFA'})
        st.plotly_chart(fig)

with col2:
    st.subheader("Tendencia Temporal")
    df_trend = pd.read_sql("SELECT published_at::date as fecha, sentiment_label, COUNT(*) as total FROM financial_articles GROUP BY fecha, sentiment_label", engine)
    if not df_trend.empty:
        fig_trend = px.line(df_trend, x='fecha', y='total', color='sentiment_label')
        st.plotly_chart(fig_trend)

# Tabla de últimas noticias
st.subheader("Últimas Noticias Procesadas")
df_news = pd.read_sql("SELECT title, sentiment_label, sentiment_score FROM financial_articles ORDER BY published_at DESC LIMIT 10", engine)
st.table(df_news)