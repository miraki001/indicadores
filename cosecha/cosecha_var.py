import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
import folium
from streamlit_folium import st_folium

from datetime import datetime as dt

def sup_variedad():




    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)     



    df_anios = pd.read_parquet("data/processed/superficievariedad_anios.parquet", engine="pyarrow")
    year_list = df_anios["anio"].to_numpy()

    df_provincias = pd.read_parquet("data/processed/cosecha_provincias.parquet", engine="pyarrow")
    prov_list = df_provincias["prov"].to_numpy()
    prov_list = np.append("Todas",prov_list )

    df_departamentos = pd.read_parquet("data/processed/cosecha_departamentos.parquet", engine="pyarrow")
    depto_list = df_departamentos["depto"].to_numpy()
    depto_list = np.append( "Todos",depto_list)
  
    
    

    


    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"
            


    

    if "filtros_cose123" not in st.session_state:
        st.session_state.filtros_cose = {
            "anio": "2024",          
            "prov": "Todas",
            "depto": "Todos",
        }




    dv1 = pd.read_parquet("data/processed/cosecha_datos.parquet", engine="pyarrow")

 
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2, col3 =  st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año444",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
      
        with col2:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincia de la lista")
                prov = st.multiselect("Provv1",   prov_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamento de la lista")
                depto = st.multiselect("deptov",  depto_list, default=["Todos"],label_visibility="collapsed")                
    
    
    #st.write(df_filtered)
    Filtro = 'Filtro = Año = '    
    if año:
        #st.write(año)
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)  
        Filtro = Filtro +  ' ' +str(año) + ' '
        
    if prov:
        if prov[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['prov'].isin(prov)]
            #st.write(variedad)
        Filtro = Filtro + ' Provincia = ' +  str(prov) + ' '
    
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['depto'].isin(depto)]          
        Filtro = Filtro + ' Departamento = ' +  str(depto) + ' '

    df_anual = df_filtered.pivot_table(
          index='variedad', 
          columns='destino',  
          values=['peso'],
          aggfunc='sum'
    )
    st.write(df_anual)

    df_anual.columns = df_anual.columns.droplevel(0)
    df_anual = df_anual.reset_index().rename_axis(None, axis=1)
    df_anual  = df_anual.fillna(0)

    totelab = df_anual['Elaboracion'].sum()
    totecon = df_anual['Consumo'].sum()
    totesec = df_anual['Secado'].sum()
    #st.write(totelab)
    total = []
    totco = []
    totse = []
    totto = []
    #total.append(0)
    for index in range(len(df_anual)):
        total.append((  (df_anual['Elaboracion'].loc[index] / totelab) *100 ))
        totco.append((  (df_anual['Consumo'].loc[index] / totecon) *100 ))
        totse.append((  (df_anual['Secado'].loc[index] / totesec) *100 ))
        totto.append((  (df_anual['Secado'].loc[index]  +  df_anual['Consumo'].loc[index] + df_anual['Elaboracion'].loc[index] ) ))
    df_anual['Part. % Total Elab'] = total
    df_anual['Part. % Total Cons'] = totco
    df_anual['Part. % Total Sec'] = totse
    df_anual['Total'] = totto

    df_anual = df_anual.sort_index(axis = 1)
    #df_anual = df_anual.rename(columns={'prov': "Provincia"})
    
    df_sorted = df_anual.sort_values(by='Elaboracion', ascending=False)

    styled_df = df_sorted.style.format(
            {"Elaboracion": lambda x : '{:,.0f}'.format(x), 
            "Consumo": lambda x : '{:,.0f}'.format(x), 
            "Secado": lambda x : '{:,.0f}'.format(x),  
            "Total": lambda x : '{:,.0f}'.format(x),  
            "Part. % Total Elab": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Cons": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Sec": lambda x : '{:,.2f} %'.format(x), 
            }
            ,
            thousands='.',
            decimal=',',
    )

    column_orders =("Variedad", "Elaboracion","Part. % Total Elab","Consumo","Part. % Total Cons","Secado","Part. % Total Sec","Total")

    if st.checkbox('Ver tabla Superficie por Variedades'):
        st.dataframe(styled_df,
              column_config={
                'Variedad': st.column_config.Column('Variedad'),
                'Elaboracion': st.column_config.Column('Elaboracion'),
                'Consumo': st.column_config.Column('Consumo'),
                'Secado': st.column_config.Column('Secado'),
                'Total': st.column_config.Column('Total'),
                'Part. % Total Elab': st.column_config.Column('Part. % Total Elab'),        
                'Part. % Total Cons': st.column_config.Column('Part. % Total Cons'),                          
                'Part. % Total Sec': st.column_config.Column('Part. % Total Sec'),                   
                },
                column_order = column_orders,
                width = 800,   
                height = 400,
                hide_index=True)
