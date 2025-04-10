import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def cosecha_evo():




    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)     

  
    

    conn = st.connection("postgresql", type="sql")


    def cargar_datos(consulta):
        try:
            df = conn.query(consulta, ttl="0")
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()
    QUERY_V0 = f"""
        SELECT distinct variedad,provincia_viñatero prov,departamento_viñatero depto,destino_uva destino,tipouva,color
        FROM cosecha2_m 
        

    """

    
    # Cargar datos iniciales para llenar los filtros
    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    #year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    prov_list = sorted(df_filtros["prov"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    depto_list = sorted(df_filtros["depto"].dropna().unique())
    color_list = sorted(df_filtros["color"].dropna().unique())
    destino_list = sorted(df_filtros["destino"].dropna().unique())
    tipo_list = sorted(df_filtros["tipouva"].dropna().unique())



    QUERY_V1 = f"""
        SELECT anio, peso , variedad,provincia_viñatero prov,departamento_viñatero depto,destino_uva destino,tipouva,color
        FROM cosecha2 

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    

    df_filtered = dv1.copy()




    df_anual = df_filtered.groupby(['pais'], as_index=False)[['peso']].sum()
    




