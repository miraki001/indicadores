
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

streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
st.markdown(streamlit_style, unsafe_allow_html=True) 

conn = st.connection("postgresql", type="sql")

@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()


QUERY_V0 = f"""
        SELECT distinct anio,variedad,provincia,departamento
        FROM superficievariedad_m 
        

"""



tab1, tab2, tab3 = st.tabs(["Superficie", "Cosecha", "Rendimientos"])

with tab1:


    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    prov_list = sorted(df_filtros["provincia"].dropna().unique())
    depto_list = sorted(df_filtros["provincia"].dropna().unique())
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "anio": "Todos",
            "var": "Todas",
            "provincia": "Todas",
            "departamento": "Todos"
        }

    st.html(
        '''
            <style>
                div[data-testid="stPopover"]>div>button {
                    min-height: 22.4px;
                    height: 22.4px;
                    background-color: #A9F8FA !important;
                    color: black;
                }
            </style>
        '''
    )
    QUERY_V1 = f"""
        SELECT anio,sup ,variedad,provincia,departamento  from superficievariedad_m
        
        

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    with st.container(border=True):
        col1, col2, col3= st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        with col2:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincias de la lista")
                provincia = st.multiselect("Provincia",  ["Todas"] + prov_list, default=["Todas"],label_visibility="collapsed")
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                departamento = st.multiselect("Departamento",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")                

   
    df_filtered = dv1.copy()



    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad1'].isin(variedad)]
            #st.write(variedad)
    if departamento:
        if departamento[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['departamento'].isin(departamento)]
    if provincia:
        if provincia[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]          
    
    st.header("Cantidad de Viñedos")
    #sql = "select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = '" + vcolor + "' or  '" +vcolor + "'= 'Todas' ) group by anio order by anio"
    #st.write(sql)
    #dv1 = conn.query(sql)
    #dv1 = conn.query('select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = %1 or %1= '-1' group by anio order by anio ;', ttl="0")
    st.write(df_filtered)
    #dv1['anio'] = dv1['anio'].astype(str)

    newdf=df_filtered.set_index('anio',inplace=False).rename_axis(None)
    
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
            },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dv1['anio'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dv1['sup'].to_list(), "type": "line", "name": 'Hectareas'}
                   ,{"data": dv1['cnt'].to_list(), "type": "bar","name":'Cnt Viñedos'}]
    }
    st_echarts(
        options=option, height="400px" ,
    )

    
    
with tab2:
    st.header("En Construcción")
    
with tab3:
    st.header("En Construcción")
