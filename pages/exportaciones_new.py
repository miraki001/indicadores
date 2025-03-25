import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line


hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




conn = st.connection("postgresql", type="sql")
df = conn.query('select anio,litros,fob from inf_expo_anio ;', ttl="0")
#st.write(df)

@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# Cargar datos iniciales para llenar los filtros
QUERY_INICIAL = "select anio,litros,fob from inf_expo_anio"
df_filtros = cargar_datos(QUERY_INICIAL)

if df_filtros.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

# Listas de valores únicos para los filtros
year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
var_list = sorted(df_filtros["variedad"].dropna().unique())
prov_list = sorted(df_filtros["provincia"].dropna().unique())
color_list = ("Tinta", "Blanca", "Rosada", "Sin Dato", "Todas")
