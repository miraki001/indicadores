import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def despachos_envase(df_filtros,df):


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
                producto = st.multiselect("Productoren",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más años")
            
      
        with col2:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envasever",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")

        with col3:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincias de la lista")
                provincia = st.multiselect("Provincias12e",  ["Todas"] + envase_list, default=["Todas"],label_visibility="collapsed")
    
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
          columns='subgrupoenvase',  
          values=['litros'],
          aggfunc='sum'
    )  
    litros  = litros.fillna(0)
    litros.columns = litros.columns.droplevel(0)   
    litros = litros.reset_index()
    #st.write(litros)
    
    #for index in range(len(litros)):
    #    litros['Rosado'].loc[index] = litros['Rosado'].loc[index] +litros['Sin Dato'].loc[index]  
    tot1 = []
    for index in range(len(litros)):
        tot1.append((  (litros['Sachet'].loc[index]  +  litros['Fraccionamiento sin Sub Grupo'].loc[index]   )))
    litros['Otros'] = tot1        

    tot1 = []
    for index in range(len(litros)):
        tot1.append((  (litros['Bidon'].loc[index]  +  litros['Botella'].loc[index]  +  litros['Damajuana'].loc[index]  +  litros['Bag in Box'].loc[index]  +  litros['Granel'].loc[index]  +  litros['Lata'].loc[index]  +  litros['Multilaminado'].loc[index] )))
    litros['Total'] = tot1  
    #st.write(litros)
    
    tot1 = []
    tot2 = []
    tot3 = []
    tot4 = []
    tot5 = []
    tot6 = []
    tot7 = []
    for index in range(len(litros)):
        #if index > 0:
            tot1.append((  (litros['Bidon'].loc[index] / litros['Total'].loc[index]  ) *100 ))
            tot2.append((  (litros['Botella'].loc[index] / litros['Total'].loc[index]  *100 )))
            tot3.append((  (litros['Damajuana'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
            tot4.append((  (litros['Bag in Box'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
            tot5.append((  (litros['Granel'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
            tot6.append((  (litros['Lata'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
            tot7.append((  (litros['Multilaminado'].loc[index] / litros['Total'].loc[index]  * 100 ) ) )
    litros['Part. % Bid'] = tot1
    litros['Part. % Bot'] = tot2
    litros['Part. % Dam'] = tot3    
    litros['Part. % Bag'] = tot4    
    litros['Part. % Gra'] = tot5    
    litros['Part. % Lat'] = tot6    
    litros['Part. % Mul'] = tot7    
    #st.write(litros)
    litros = litros.rename(columns={'anio': "Año"})

    styled_df = litros.style.format(
            {"Bidon": lambda x : '{:,.0f}'.format(x), 
            "Botella": lambda x : '{:,.0f}'.format(x),
            "Damajuana": lambda x : '{:,.0f}'.format(x),
            "Bag in Box": lambda x : '{:,.0f}'.format(x),
            "Granel": lambda x : '{:,.0f}'.format(x),
            "Lata": lambda x : '{:,.0f}'.format(x),
            "Multilaminado": lambda x : '{:,.0f}'.format(x),
            "Total": lambda x : '{:,.0f}'.format(x),
            "Part. % Bid": lambda x : '{:,.2f} %'.format(x),
            "Part. % Bot": lambda x : '{:,.2f} %'.format(x),
            "Part. % Dam": lambda x : '{:,.2f} %'.format(x),
            "Part. % Bag": lambda x : '{:,.2f} %'.format(x),
            "Part. % Gra": lambda x : '{:,.2f} %'.format(x),
            "Part. % Lat": lambda x : '{:,.2f} %'.format(x),
            "Part. % Mul": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver Depachos por Envase en forma de tabla'):
        st.caption(Filtro)    
        
        column_orders =("Año", "Bidon", "Part. % Bid", "Botella", "Part. % Bot", "Damajuana" , "Part. % Dam","Bag in Box","Part. % Bag","Granel","Part. % Gra","Lata","Part. % Lat","Multilaminado","Part. % Mul", "Total" )
       
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),                  
                'Bidon': st.column_config.Column('Bidon'),
                'Botella': st.column_config.Column('Botella'),
                'Damajuana': st.column_config.Column('Damajuana'),
                'Bag in Box"': st.column_config.Column('Bag in Box'),
                'Granel': st.column_config.Column('Granel'),
                'Lata': st.column_config.Column('Lata'),
                'Multilaminado': st.column_config.Column('Multilaminado'),
                'Total': st.column_config.Column('Total'),
                'Part. % Bid': st.column_config.Column('Part. % Bid'),
                'Part. % Bot': st.column_config.Column('Part. % Bot'),
                'Part. % Dam': st.column_config.Column('Part. % Dam'),
                'Part. % Bag': st.column_config.Column('Part. % Bag'),
                'Part. % Gra': st.column_config.Column('Part. % Gra'),
                'Part. % Lat': st.column_config.Column('Part. % Lat'),
                'Part. % Mul': st.column_config.Column('Part. % Mul'),
        
                },
                column_order = column_orders,     
                width = 1200,   
                height = 800,
                hide_index=True)
    st.caption(Filtro)    
        
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
        "series": [{"data": litros['Bidon'].to_list(), "type": "line", "name": 'Bidon',"color":'#C92488', },
                   {"data": litros['Botella'].to_list(), "type": "line", "name": 'Botella',"color":'#F49F82',},
                   {"data": litros['Damajuana'].to_list(), "type": "line", "name": 'Damajuana',"color":'#604994',},
                   {"data": litros['Bag in Box'].to_list(), "type": "line", "name": 'Bag in Box',"color":'#07ECFA',},
                   {"data": litros['Granel'].to_list(), "type": "line", "name": 'Granel',"color":'#1E8DB6',},
                   {"data": litros['Lata'].to_list(), "type": "line", "name": 'Lata',"color":'#C5C6C6',},
                   {"data": litros['Multilaminado'].to_list(), "type": "line", "name": 'Multilaminado',"color":'#A9F8FA',},
               ]
      }
    st_echarts(
         options=option, height="400px" ,
    )
    actual1 = dt.now().year -1
    #st.write(actual1)
    litros = litros[litros['Año'] == actual1 ]  
    Bidon = int(litros['Bidon'])
    Botella = int(litros['Botella'])
    Damajuana = int(litros['Damajuana'])
    Bag = int(litros['Bag in Box'])
    Granel = int(litros['Granel'])
    Lata = int(litros['Lata'])
    Multilaminado = int(litros['Multilaminado'])
    #st.write(blanco)
    st.caption(Filtro)    

    options = {
            "color": [
            '#C92488',
            '#F49F82',
            '#604994',
            '#07ECFA',
            '#1E8DB6',
            '#C5C6C6',
            '#A9F8FA',
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
                    {"value": Bidon, "name": "Bidon"},
                    {"value": Botella , "name": "Botella"},
                    {"value": Damajuana , "name": "Damajuana"},
                    {"value": Bag , "name": "Bag in Box"},
                    {"value": Granel , "name": "Granel"},
                    {"value": Lata , "name": "Lata"},
                    {"value": Multilaminado , "name": "Multilaminado"},
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

