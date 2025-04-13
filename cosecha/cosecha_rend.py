import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def cosecha_rend():




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
        SELECT distinct variedad,provincia,departamento
        FROM rendimiento_m
        

    """

    
    # Cargar datos iniciales para llenar los filtros
    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    #year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    prov_list = sorted(df_filtros["provincia"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    depto_list = sorted(df_filtros["departamento"].dropna().unique())

    if "filtros_cose" not in st.session_state:
        st.session_state.filtros_cose = {
            "provincias": "Todas",
            "var": "Todas",
            "depto": "Todos",

        }



    QUERY_V1 = f"""
        SELECT anio, peso , variedad,provincia,departamento,sup
        FROM rendimiento_m 

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más provincia de la lista")
                provincia = st.multiselect("Provincia",  ["Todas"] +   prov_list, default=["Todas"],label_visibility="collapsed",help="Selecciona uno o más años")           
        # Columna 2: Filtro para Países
      
        with col2:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                depto = st.multiselect("Departamento",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")
   
      
        with col3:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    

    #st.write(df_filtered)
    if provincia:
        if provincia[0] != 'Todas':        
            df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]

    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            #st.write(variedad)
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['departamento'].isin(depto)]
 

    df_anual = df_filtered.groupby(['anio'], as_index=False)[['peso','sup']].sum()
    #st.write(df_anual)
    total = []
    #total.append(0)
    for index in range(len(df_anual)):
      #if index > 0:
        total.append((  (df_anual['peso'].loc[index] / df_anual['sup'].loc[index])  )  )
    df_anual = df_anual.rename(columns={'peso': "Quintales",'anio': "Año",'sup': "Superficie"})
    df_anual['Rendimiento'] = total

    df_anual = df_anual.sort_index(axis = 1)

    
    df_sorted = df_anual.sort_values(by='Año', ascending=True)

    styled_df = df_sorted.style.applymap(bgcolor_positive_or_negative, subset=['Var % Año Ant.']).format(
            {"Quintales": lambda x : '{:,.0f}'.format(x), 
             "Superficie": lambda x : '{:,.0f}'.format(x), 
             "Rendimiento": lambda x : '{:,.2f} %'.format(x),                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver tabla Rendimientos por Año'):
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),
                'Quintales': st.column_config.Column('Quintales'),
                'Superficie': st.column_config.Column('Superficie'),
                'Rendimientoo': st.column_config.Column('Rendimiento'),

        
                },
                width = 600,   
                height = 400,
                hide_index=True)
    

    option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "xAxis": {"type": "category", "data": df_anual["Año"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Quintales" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,           
            ],
            "series": [
                {"data": df_anual["Quintales"].tolist(),"position" : 'rigth', "type": "line", "name": "Quintales" },
            ],
        }

    
    st_echarts(options=option,key="gauge" + str(dt.now()), height="400px")
