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
        col1=  st.columns([1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Canal"):
                st.caption("Selecciona uno o más Canales de la lista")
                canal = st.multiselect("Canal",  ["Todos"] + canal_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más Canales")
                 
    
    Filtro = 'Filtro = '    
    df_filtered = df.copy()    
        
    if canal:
        if canal[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['canal'].isin(canal)]
        Filtro = Filtro + ' Canal = ' +  str(Canal) 
    
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
    rosado = int(litros['Rosado'])
    st.write(blanco)

    options = {
            "color": [
            '#C92488',
            '#F49F82',
            '#604994',

            ],        
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "90%",
                "data": [
                    {"value": rosado, "name": "Rosado"},
                    {"value": blanco , "name": "Blanco"},
                    {"value": tinto , "name": "Tinto"},
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

    #   ahora por producto
    
    tipo = df_filtered.pivot_table(
          index='anio', 
          columns='producto',  
          values=['litros'],
          aggfunc='sum'
    )  
    tipo  = tipo.fillna(0)
    tipo.columns = tipo.columns.droplevel(0)   
    tipo = tipo.reset_index()
    #st.write(tipo)
    for index in range(len(tipo)):
        tipo['Otros Vinos'].loc[index] = tipo['Otros Vinos'].loc[index] +tipo['Otros'].loc[index]  
 
    tot1 = []
    for index in range(len(tipo)):
        tot1.append((  (tipo['Espumantes'].loc[index]  +  tipo['Gasificados'].loc[index] + tipo['Otros Vinos'].loc[index] + tipo['Vino Varietal'].loc[index] + tipo['Vinos sin Mencion'].loc[index]   )))
    tipo['Total'] = tot1        
    tot1 = []
    tot2 = []
    tot3 = []
    tot4 = []
    tot5 = []
    for index in range(len(tipo)):
        #if index > 0:
            tot1.append((  (tipo['Espumantes'].loc[index] / tipo['Total'].loc[index]  ) *100 ))
            tot2.append((  (tipo['Gasificados'].loc[index] / tipo['Total'].loc[index]  *100 )))
            tot3.append((  (tipo['Otros Vinos'].loc[index] / tipo['Total'].loc[index]  * 100 ) ) )
            tot4.append((  (tipo['Vino Varietal'].loc[index] / tipo['Total'].loc[index]  * 100 ) ) )
            tot5.append((  (tipo['Vinos sin Mencion'].loc[index] / tipo['Total'].loc[index]  * 100 ) ) )
    tipo['Part. % Esp.'] = tot1
    tipo['Part. % Gas.'] = tot2
    tipo['Part. % Otros'] = tot3    
    tipo['Part. % Var.'] = tot4    
    tipo['Part. % Sin'] = tot5    
    #st.write(tipo)
    tipo = tipo.rename(columns={'anio': "Año"})

    styled_df = tipo.style.format(
            {"Espumantes": lambda x : '{:,.0f}'.format(x), 
            "Gasificados": lambda x : '{:,.0f}'.format(x),
            "Otros Vinos": lambda x : '{:,.0f}'.format(x),
            "Vino Varietal": lambda x : '{:,.0f}'.format(x),
            "Vinos sin Mencion": lambda x : '{:,.0f}'.format(x),
            "Total": lambda x : '{:,.0f}'.format(x),
            "Part. % Esp.": lambda x : '{:,.2f} %'.format(x),
            "Part. % Gas.": lambda x : '{:,.2f} %'.format(x),
            "Part. % Otros": lambda x : '{:,.2f} %'.format(x),
            "Part. % Var.": lambda x : '{:,.2f} %'.format(x),
            "Part. % Sin": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
    )
    if st.checkbox('Ver Depachos por Producto en forma de tabla'):
        column_orders =("Año", "Espumantes", "Part. % Esp.", "Gasificados", "Part. % Gas.", "Otros Vinos" , "Part. % Otros", "Vino Varietal","Part. % Var.","Vinos sin Mencion","Part. % Sin","Total")
       
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),                  
                'Espumantes': st.column_config.Column('Espumantes'),
                'Gasificados': st.column_config.Column('Gasificados'),
                'Otros Vinos': st.column_config.Column('Otros Vinos'),
                'Vino Varietal': st.column_config.Column('Vino Varietal'),
                'Vinos sin Mencion"': st.column_config.Column('Vinos sin Mencion"'),
                'Total': st.column_config.Column('Total'),
                'Part. % Esp.': st.column_config.Column('Part. % Esp.'),
                'Part. % Gas.': st.column_config.Column('Part. % Gas.'),
                'Part. % Otros': st.column_config.Column('Part. % Otros'),
                'Part. % Var.': st.column_config.Column('Part. % Var.'),
                'Part. % Sin': st.column_config.Column('Part. % Sin'),
        
                },
                column_order = column_orders,     
                width = 1200,   
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
            "data": tipo['Año'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": tipo['Espumantes'].to_list(), "type": "line", "name": 'Espumantes',"color":'#C92488', },
                   {"data": tipo['Gasificados'].to_list(), "type": "line", "name": 'Gasificados',"color":'#F49F82',},
                   {"data": tipo['Otros Vinos'].to_list(), "type": "line", "name": 'Otros Vinos',"color":'#604994',},
                   {"data": tipo['Vino Varietal'].to_list(), "type": "line", "name": 'Vino Varietal',"color":'#07ECFA',},
                   {"data": tipo['Vinos sin Mencion'].to_list(), "type": "line", "name": 'Vinos sin Mencion',"color":'#1E8DB6',},
               ]
      }
    st_echarts(
         options=option, height="400px" ,
    )
    actual1 = dt.now().year -1
    #st.write(actual1)
    tipo = tipo[tipo['Año'] == actual1 ]  
    espumantes = int(tipo['Espumantes'])
    gasificados = int(tipo['Gasificados'])
    otros = int(tipo['Otros Vinos'])
    varietal = int(tipo['Vino Varietal'])
    comunes = int(tipo['Vinos sin Mencion'])
    st.write(blanco)

    options = {
            "color": [
            '#C92488',
            '#F49F82',
            '#604994',
            '#07ECFA',
            '#1E8DB6',

            ],        
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "90%",
                "data": [
                    {"value": espumantes, "name": "Espumantes"},
                    {"value": gasificados , "name": "Gasificados"},
                    {"value": otros , "name": "Otros Vinos"},
                    {"value": varietal , "name": "Vino Varietal"},
                    {"value": comunes , "name": "Vino sin Mencion"},
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
