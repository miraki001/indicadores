import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def despachos_color(df_filtros,df):


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

  
  
  # Listas de valores únicos para los filtros
    prov_list = sorted(df_filtros["provincia"].dropna().unique())
    envase_list = sorted(df_filtros["subgrupoenvase"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())
    #pais_list = sorted(df_filtros["pais"].dropna().unique())
    if "filtroseem" not in st.session_state:
        st.session_state.filtrosee = {
            "envase": "Todos",
            "producto": "Todos",
        }

    
    #dv1['anio'] = dv1['anio'].astype(str)




    with st.container(border=True):
        col1, col2,col3 =  st.columns([1, 1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más Productos de la lista")
                producto = st.multiselect("Productorr",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más años")
            
      
        with col2:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envasevr",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")

        with col3:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincias de la lista")
                provincia = st.multiselect("Provincias12",  ["Todas"] + envase_list, default=["Todas"],label_visibility="collapsed")
    
    Filtro = 'Filtro = '    
    df_filtered = df.copy()    
        
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Productos = ' +  str(producto) + ' '
    
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['subgrupoenvase'].isin(color)]          
        Filtro = Filtro + ' Envases = ' +  str(envase) + ' '
        
    if provincia:
        if provincia[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]          
        Filtro = Filtro + ' Provincias = ' +  str(provincia) + ' '
            

    #df_filtered = dv1.copy()
    actual = dt.now().year -4 
    #df_filtered = df_filtered[df_filtered['anio'] > actual ]   
    #df_filtered = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()
    litros = df_filtered.pivot_table(
          index='anio', 
          columns='color',  
          values=['litros'],
          aggfunc='sum'
    )  
    litros  = litros.fillna(0)
    litros.columns = litros.columns.droplevel(0)   
    litros = litros.reset_index()
    #st.write(litros['Rosado'])
    for index in range(len(litros)):
        litros['Rosado'].loc[index] = litros['Rosado'].loc[index] +litros['Sin Dato'].loc[index]  
    tot1 = []
    for index in range(len(litros)):
        tot1.append((  (litros['Rosado'].loc[index]  +  litros['Blanco'].loc[index] + litros['Tinto'].loc[index]  )))
    litros['Total'] = tot1        
    tot1 = []
    tot2 = []
    tot3 = []
    for index in range(len(litros)):
        #if index > 0:
            tot1.append((  (litros['Rosado'].loc[index] / litros['Total'].loc[index]  ) *100 ))
            tot2.append((  (litros['Blanco'].loc[index] / litros['Total'].loc[index]  *100 )))
            tot3.append((  (litros['Tinto'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
    litros['Part. % Rosado'] = tot1
    litros['Part. % Blanco'] = tot2
    litros['Part. % Tinto'] = tot3    
    #st.write(litros)
    litros = litros.rename(columns={'anio': "Año"})

    styled_df = litros.style.format(
            {"Rosado": lambda x : '{:,.0f}'.format(x), 
            "Blanco": lambda x : '{:,.0f}'.format(x),
            "Tinto": lambda x : '{:,.0f}'.format(x),
            "Total": lambda x : '{:,.0f}'.format(x),
            "Part. % Rosado": lambda x : '{:,.2f} %'.format(x),
            "Part. % Blanco": lambda x : '{:,.2f} %'.format(x),
            "Part. % Tinto": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver Depachos por Color en forma de tabla'):
        column_orders =("Año", "Blanco", "Part. % Blanco", "Rosado", "Part. % Rosado", "Tinto" , "Part. % Tinto", "Total" )
       
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),                  
                'Rosado': st.column_config.Column('Rosado'),
                'Blanco': st.column_config.Column('Blanco'),
                'Tinto': st.column_config.Column('Tinto'),
                'Total': st.column_config.Column('Total'),
                'Part. % Rosado': st.column_config.Column('Part. % Rosado'),
                'Part. % Blanco': st.column_config.Column('Part. % Blanco'),
                'Part. % Tinto': st.column_config.Column('Part. % Tinto'),
        
                },
                column_order = column_orders,     
                width = 1000,   
                height = 800,
                hide_index=True)
    option = {
        "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": litros['Año'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": litros['Rosado'].to_list(), "type": "line", "name": 'Rosado',"color":'#C92488', },
                   {"data": litros['Blanco'].to_list(), "type": "line", "name": 'Blanco',"color":'#F49F82',},
                   {"data": litros['Tinto'].to_list(), "type": "line", "name": 'tinto',"color":'#604994',},
               ]
      }
    st_echarts(
         options=option, height="400px" ,
    )
    actual1 = dt.now().year -1
    #st.write(actual1)
    litros = litros[litros['Año'] == actual1 ]  
    blanco = int(litros['Blanco'])
    tinto = int(litros['Tinto'])
    blanco = int(litros['Rosado'])
    st.write(blanco)

    options = {
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": blanco, "name": "Blanco"},
                    {"value": tinto , "name": "Tinto"},
                    {"value": rosado , "name": "Rosado"},
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(10, 0, 0, 0.5)",
                    }
                },
            }
            ],
    }
    st_echarts(
        options=options, height="200px",
    )
