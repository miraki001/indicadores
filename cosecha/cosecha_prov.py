import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def cosecha_prov():




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
        SELECT distinct anio,variedad,tipouva,color
        FROM cosecha2 
        

    """

    
    # Cargar datos iniciales para llenar los filtros
    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    color_list = sorted(df_filtros["color"].dropna().unique())
    tipo_list = sorted(df_filtros["tipouva"].dropna().unique())
    if "filtros_cose1" not in st.session_state:
        st.session_state.filtros_cose = {
            "anio": "Todos",          
            "var": "Todas",
            "color": "Todos",
            "tipo": "Todos"
        }



    QUERY_V1 = f"""
        SELECT anio, peso , variedad,provincia_viñatero prov,departamento_viñatero depto,tipouva,destinouva destino,color
        FROM cosecha2 

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2, col3,col4 =  st.columns([1, 1, 1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
      
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedadv",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Colorv",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed")                
        with col4:
            with st.popover("Tipo de Uva"):
                st.caption("Selecciona uno o más Tipos de la lista")
                tipo = st.multiselect("tipouva",  ["Todos"] + tipo_list, default=["Todos"],label_visibility="collapsed")      
    
    
    #st.write(df_filtered)
    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)  
    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            #st.write(variedad)
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
    if tipo:
        if tipo[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipouva'].isin(tipo)]      
    

    #df_anual = df_filtered.groupby(['anio','prov','depto'], as_index=False)[['peso']].sum()
    #df_anual = pd.pivot_table(df_filtered, values='peso', index=['prov'],
    #                   columns=['destino'], aggfunc="sum")

    df_anual = df_filtered.pivot_table(
          index='prov', 
          columns='destino',  
          values=['peso'],
          aggfunc='sum'
    )
    st.write(df_anual)

    df_anual.columns = df_anual.columns.droplevel(0)
    df_anual = df_anual.reset_index().rename_axis(None, axis=1)

    totelab = df_anual['Elaboracion'].sum()
    totecon = df_anual['Consumo'].sum()
    totesec = df_anual['Secado'].sum()
    st.write(totelab)
    total = []
    totco = []
    totse = []
    #total.append(0)
    for index in range(len(df_anual)):
        total.append((  (df_anual['Elaboracion'].loc[index] / totelab) *100 ))
        totco.append((  (df_anual['Consumo'].loc[index] / totecon) *100 ))
        totse.append((  (df_anual['Secado'].loc[index] / totesec) *100 ))
    df_anual['Part. % Total Elab'] = total
    df_anual['Part. % Total Cons'] = total
    df_anual['Part. % Total Sec'] = total

    df_anual = df_anual.sort_index(axis = 1)
    df_anual = df_anual.rename(columns={'prov': "Provincia"})
    
    df_sorted = df_anual.sort_values(by='Elaboracion', ascending=False)

    styled_df = df_sorted.style.format(
            {"Elaboracion": lambda x : '{:,.0f}'.format(x), 
            "Consumo": lambda x : '{:,.0f}'.format(x), 
            "Secado": lambda x : '{:,.0f}'.format(x),  
            "Part. % Total Elab": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Cons": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Sec": lambda x : '{:,.2f} %'.format(x), 
            }
            ,
            thousands='.',
            decimal=',',
    )

    column_orders =("Provincia", "Elaboracion","Part. % Total Elab","Consumo","Part. % Total Cons","Secado","Part. % Total Sec")

    if st.checkbox('Ver tabla Cosecha por Provincias'):
        st.dataframe(styled_df,
              column_config={
                'Elaboracion': st.column_config.Column('Elaboracion'),
                'Consumo': st.column_config.Column('Consumo'),
                'Secado': st.column_config.Column('Secado'),
                'Part. % Total Elab': st.column_config.Column('Part. % Total Elab'),        
                'Part. % Total Cons': st.column_config.Column('Part. % Total Cons'),                          
                'Part. % Total Sec': st.column_config.Column('Part. % Total Sec'),                   
                },
                column_order = column_orders,
                width = 600,   
                height = 400,
                hide_index=True)
    

