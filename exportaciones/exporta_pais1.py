import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def exporta_destino():




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
        SELECT distinct anio,variedad1 variedad,tipo_envase,color,producto,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """

    
    # Cargar datos iniciales para llenar los filtros
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais  from exportaciones2_m where producto not in ('Mosto','Alcohol');"
    df_filtros = cargar_datos(QUERY_INICIAL)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    pais_list = sorted(df_filtros["pais"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    envase_list = sorted(df_filtros["tipo_envase"].dropna().unique())
    color_list = sorted(df_filtros["color"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())



    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    

    df_filtered = dv1.copy()




    df_anual = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_variedad = df_filtered.groupby(['pais','variedad1'], as_index=False)[['fob', 'litros']].sum()
    df_variedad = df_variedad.sort_values('fob').head(10)
    st.write(df_variedad)
    pais_list1 = sorted(df_variedad["pais"].dropna().unique(), reverse=True)
    var_list1 = sorted(df_variedad["variedad"].dropna().unique())
    





    df1 = pd.DataFrame({'name':var_list + pais_list})

    result1 = df1.to_json(orient="records")


    df_variedad.drop(['litros'], axis='columns', inplace=True)
    #st.write(df_variedad)
    df_variedad = df_variedad.rename(columns={'pais': "source",'variedad1': "target",'fob': "value"})

    result3 = df_variedad.to_json(orient="records")

    pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}' 

    data = json.loads(pp)


