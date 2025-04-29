import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def despachos_consumo():


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

    #st.write(dt.now().year)

    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True) 


    conn = st.connection("postgresql", type="sql")

    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"
            
    @st.cache_data
    def cargar_datos(consulta):
        try:
            df = conn.query(consulta, ttl="0")
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()

    QUERY_V0 = f"""
        SELECT distinct canal
        FROM scentia_res       

    """
    df_filtros = cargar_datos(QUERY_V0)
    
  # Listas de valores únicos para los filtros
    canal_list = sorted(df_filtros["canal"].dropna().unique())
    if "filtroseemv" not in st.session_state:
        st.session_state.filtrosee = {
            "canal": "Todos",
        }

    QUERY_V1 = f"""
        SELECT periodo,canal,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" 
        FROM scentia_res
    """    


    dv1 = cargar_datos(QUERY_V1)
    df_filtered = dv1.copy() 
    #dv1['anio'] = dv1['anio'].astype(str)




    with st.container(border=True):
        col1,col2 =  st.columns([1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Canal"):
                st.caption("Selecciona uno o más Canales de la lista")
                canal = st.multiselect("Canal",  ["Todos"] + canal_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más Canales")
                 
    
    Filtro = 'Filtro = '    
        
    if canal:
        if canal[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['canal'].isin(canal)]
        Filtro = Filtro + ' Canal = ' +  str(canal) 
    
    #df_filtered = dv1.copy()
    actual = dt.now().year -4 
    #df_filtered = df_filtered[df_filtered['anio'] > actual ]   
    #df_filtered = df_filtered.groupby(['periodo'], as_index=False).sum()

    litros = df_filtered.pivot_table(
          index='periodo', 
          values=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS"],
          aggfunc='sum'
    )  
    if st.checkbox('Ver datos en forma de tabla Valores'):
        st.write(litros)

    #litros.columns = litros.columns.droplevel(0)
    st.write(litros['periodo'])
    litros['periodo'] = litros['periodo'].astype(str)    
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": litros['periodo'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": litros['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
                   ,{"data": litros['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
                   ,{"data": litros['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
                   ,{"data": litros['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
                   ,{"data": litros['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
                   ,{"data": litros['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
                   ,{"data": litros['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
                   ,{"data": litros['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
    }
    st_echarts(
        options=option, height="400px",
    )
