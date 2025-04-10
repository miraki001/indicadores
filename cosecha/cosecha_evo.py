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
        SELECT distinct variedad,provincia_viñatero prov,departamento_viñatero depto,destinouva destino,tipouva,color
        FROM cosecha2 
        

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
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "provincias": "Todas",
            "var": "Todas",
            "depto": "Todos",
            "color": "Todos",
            "destino": "Todos",
            "tipo": "Todos"
        }



    QUERY_V1 = f"""
        SELECT anio, peso , variedad,provincia_viñatero prov,departamento_viñatero depto,destinouva destino,tipouva,color
        FROM cosecha2 

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más provincia de la lista")
                provincia = st.multiselect("Provincia",  ["Todas"] +   prov_list, default=["Todas"],label_visibility="collapsed",help="Selecciona uno o más años")           
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                depto = st.multiselect("Departamento",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")
        with col4:
            with st.popover("Destino"):
                st.caption("Selecciona uno o más Destinos de la lista")
                destino = st.multiselect("Destino",  ["Todos"] + destino_list, default=["Todos"],label_visibility="collapsed")                

        with col5:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Color",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed")                
        with col6:
            with st.popover("Tipo de Uva"):
                st.caption("Selecciona uno o más Tipos de la lista")
                tipo = st.multiselect("Gurpo Envase",  ["Todos"] + tipo_list, default=["Todos"],label_visibility="collapsed")      
    
    
    st.write(df_filtered)
    if provincia:
        if provincia[0] != 'Todas':        
            df_filtered = df_filtered[df_filtered['prov'].isin(provincia)]
            #df_filtered["anio"] = df_filtered["anio"].astype(str)

    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            #st.write(variedad)
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['depto'].isin(depto)]
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
    if destino:
        if destino[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['destino'].isin(destino)]               
    if tipo:
        if tipo[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipouva'].isin(tipo)]      
    

    df_anual = df_filtered.groupby(['anio'], as_index=False)[['peso']].sum()
    st.write(df_anual)
    total = []
    total.append(0)
    for index in range(len(df_anual)):
      if index > 0:
        total.append((  (df_anual['peso'].loc[index] / df_anual['peso'].loc[index -1]) -1 ) *100 )
    df_anual = df_anual.rename(columns={'peso': "Quintales",'anio': "Año"})
    df_anual['Var % Año Ant.'] = total

    df_anual = df_anual.sort_index(axis = 1)

    
    df_sorted = df_anual.sort_values(by='Año', ascending=False)

    styled_df = df_sorted.style.format(
            {"Quintales": lambda x : '{:,.0f}'.format(x), 
            "Var % Año Ant.": lambda x : '{:,.2f} %'.format(x),                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver tabla Cosecha por Año'):
        st.dataframe(styled_df,
              column_config={
                'Pais': st.column_config.Column('Pais'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                width = 800,   
                height = 400,
                hide_index=True)
    


