import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sua_senha")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "iot_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

st.set_page_config(page_title="Dashboard de Temperaturas IoT", layout="wide")

engine = create_engine(DATABASE_URL)


@st.cache_data(ttl=300)
def load_data(view_name: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


st.title("Dashboard de Temperaturas IoT")
st.caption("Pipeline de dados com IoT, Docker e PostgreSQL")

# Grafico 1: Media de temperatura por dispositivo
st.header("Media de Temperatura por Dispositivo")
df_avg_temp = load_data("avg_temp_por_dispositivo")
fig1 = px.bar(
    df_avg_temp,
    x="device_id",
    y="avg_temp",
    labels={"device_id": "Dispositivo", "avg_temp": "Temperatura media (C)"},
)
st.plotly_chart(fig1, use_container_width=True)

# Grafico 2: Contagem de leituras por hora
st.header("Leituras por Hora do Dia")
df_leituras_hora = load_data("leituras_por_hora")
fig2 = px.line(
    df_leituras_hora,
    x="hora",
    y="contagem",
    labels={"hora": "Hora do dia", "contagem": "Numero de leituras"},
)
st.plotly_chart(fig2, use_container_width=True)

# Grafico 3: Temperaturas maximas e minimas por dia
st.header("Temperaturas Maximas e Minimas por Dia")
df_temp_max_min = load_data("temp_max_min_por_dia")
fig3 = px.line(
    df_temp_max_min,
    x="data",
    y=["temp_max", "temp_min"],
    labels={"data": "Data", "value": "Temperatura (C)", "variable": "Metrica"},
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.subheader("Resumo estatistico")
col1, col2, col3 = st.columns(3)
col1.metric("Dispositivos monitorados", df_avg_temp["device_id"].nunique())
col2.metric("Temp. media geral (C)", round(df_avg_temp["avg_temp"].mean(), 1))
col3.metric("Total de leituras (hora)", int(df_leituras_hora["contagem"].sum()))
