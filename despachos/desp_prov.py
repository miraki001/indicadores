import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def despachos_prov(df_filtros,df):




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

  
  
  # Listas de valores únicos para los filtros
    #prov_list = sorted(df_filtros["provincia"].dropna().unique())
    envase_list = sorted(df_filtros["subgrupoenvase"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())
    #pais_list = sorted(df_filtros["pais"].dropna().unique())
    if "filtroseem" not in st.session_state:
        st.session_state.filtrosee = {
            "envase": "Todos",
            "producto": "Todos",
        }

    
    dv1['anio'] = dv1['anio'].astype(str)




    with st.container(border=True):
        col1, col2 =  st.columns([1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más Productos de la lista")
                producto = st.multiselect("Producto",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más años")
            
      
        with col2:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                variedad = st.multiselect("Envasev",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")
    
    Filtro = 'Filtro = '    
    df_filtered = dv1.copy()    
        
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Productos = ' +  str(producto) + ' '
    
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['subgrupoenvase'].isin(color)]          
        Filtro = Filtro + ' Envases = ' +  str(envase) + ' '
            

    #df_filtered = dv1.copy()
    actual = dt.now().year -4 
    df_filtered = df_filtered[df_filtered['anio'] > actual ]   
    df_filtered = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()
    litros = dv2.pivot_table(
          index='provincia', 
          columns='anio',  
          values=['litros'],
          aggfunc='sum'
    )  
    st.write(litros)


