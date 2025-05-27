import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
#from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"


def prov_color():

  df_anios = pd.read_parquet("data/processed/superficievariedad_anios.parquet", engine="pyarrow")
  year_list = df_anios["anio"].to_numpy()
  #year_list = np.append(year_list, "Todos")    

  df_variedades = pd.read_parquet("data/processed/superficievariedad_variedades.parquet", engine="pyarrow")
  var_list = df_variedades["variedad"].to_numpy()
  #var_list = np.append(var_list, "Todas")
    

  with st.container(border=True):
        col1, col2  =  st.columns([1, 1])  # Ajusta los tamaños de las columnas

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
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    

  df = pd.read_parquet("data/processed/superficievariedad_datos.parquet", engine="pyarrow")
    
  pivot_table_basic = df.pivot_table(
      index='provincia', 
      columns='color',  
      values=['sup'],
      aggfunc='sum'
  )
  #st.write(pivot_table_basic)  
  dfg = pivot_table_basic
  dfg.columns = dfg.columns.droplevel(0)
  dfg = dfg.reset_index().rename_axis(None, axis=1)
  dfg['Blanca'] = dfg['Blanca'].fillna(0)  
  dfg['Rosada'] = dfg['Rosada'].fillna(0)   
  dfg['Tinta'] = dfg['Tinta'].fillna(0)    
  pivot_table_basic['Blanca'] = pivot_table_basic['Blanca'].fillna(0)  
  pivot_table_basic['Rosada'] = pivot_table_basic['Rosada'].fillna(0)   
  pivot_table_basic['Tinta'] = pivot_table_basic['Tinta'].fillna(0)    
    
  #st.write(dfg) 

  total = []
  #total.append(0)
  for index in range(len(dfg)):
      total.append(  dfg['Blanca'].loc[index]  + dfg['Rosada'].loc[index]  + dfg['Tinta'].loc[index] )

  pivot_table_basic['Total Prov.'] = total  

  #st.write(pivot_table_basic)

  pivot_table_basic['Blanca %'] = ((pivot_table_basic['Blanca']/pivot_table_basic['Total Prov.']))*100
  pivot_table_basic['Rosada %'] = ((pivot_table_basic['Rosada']/pivot_table_basic['Total Prov.']))*100
  pivot_table_basic['Tinta %'] = ((pivot_table_basic['Tinta']/pivot_table_basic['Total Prov.']))*100
  #pivot_table_basic = pivot_table_basic.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)
  #st.write(pivot_table_basic)

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)


  styled_df = pivot_table_basic.style.applymap(bgcolor_positive_or_negative, subset=['Blanca %','Rosada %','Tinta %']).format(
        {"Blanca": lambda x : '{:,.0f}'.format(x), 
        "Rosada": lambda x : '{:,.0f}'.format(x),
        "Tinta": lambda x : '{:,.0f}'.format(x),
        "Blanca %": lambda x : '{:,.2f} %'.format(x),
        "Rosada %": lambda x : '{:,.2f} %'.format(x),
        "Tinta %": lambda x : '{:,.2f} %'.format(x), 
        "Total Prov.": lambda x : '{:,.0f}'.format(x),
                                        }
        ,
    thousands='.',
    decimal=',',
  )
  st.dataframe(styled_df,
      column_config={
        'provincia': st.column_config.Column('provincia'),
        'Blanca': st.column_config.Column('Blanca'),
        'Rosada': st.column_config.Column('Rosada'),
        'Tinta': st.column_config.Column('Tinta'),
        'Blanca %': st.column_config.Column('Blanca %'),
        'Rosada %': st.column_config.Column('Rosada %'),
        'Tinta %': st.column_config.Column('Tinta %'),
        'Total Prov.': st.column_config.Column('Total Prov.')  
      },
      width = 600,   
      height = 500,
      hide_index=False
  )
  option = {
        "dataZoom": [
        {
          "show": 'true',
          "realtime": 'true',
          "start": 0,
          "end": 100,
          "xAxisIndex": [0, 1]
        },
        {
          "type": 'inside',
          "realtime": 'true',
          "start": 30,
          "end": 70,
          "xAxisIndex": [0, 1]
        }
        ],
            "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dfg['provincia'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dfg['Blanca'].to_list(), "type": "line", "name": 'Blancas'}
               ,{"data": dfg['Rosada'].to_list(), "type": "line","name":'Rosadas'}
               ,{"data": dfg['Tinta'].to_list(), "type": "line","name":'Tintas'}                   
                  ]
  }
  st_echarts(
        options=option, height="400px" ,
  )
    
