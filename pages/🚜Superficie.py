import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from superficie import sup_prov_color

conn = st.connection("postgresql", type="sql")
def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

@st.cache_data
def query():
  df3 = conn.query('select año,sum(sup) supeficie,sum(cant) cant_viñedos from superficie_m group by año order by año  ;', ttl="0"),
  return df3
df3 = query()
df2 = df3[0]

@st.cache_data
def query1():
  df4 = conn.query('select s.anio anio,s.sup sup,s.provincia,s.color ,s.variedad,s.departamento,s.tipouva tipoVariedad,s.sistemaconduccion,s.pie from superficieVariedad_m s where s.anio = 2023  ;', ttl="0"),
  return df4
df4 = query1()
df1 = df4[0]

tab1, tab2, tab3,tab4 = st.tabs(["Evolución", "Por Provincia y Color", "Por Provincia y Variedad","Por Variedad"])

with tab1:


    total = []
    tot1 = []
    total.append(0)
    tot1.append(0)
    for index in range(len(df2)):
      if index > 0:
        total.append((  (df2['supeficie'].loc[index] / df2['supeficie'].loc[index -1]) -1 ) *100 )
        tot1.append((  (df2['cant_viñedos'].loc[index] / df2['cant_viñedos'].loc[index -1]) -1 ) *100 )
    #st.write(total)
    df2 = df2.rename(columns={'supeficie': "Superficie", 'cant_viñedos': "Viñedos Cnt.",'año': "Año"})
    df2['Superficie Var %'] = total
    df2['Viñedos Var. %'] = tot1

    df2 = df2.sort_index(axis = 1)

    styled_df = df2.style.applymap(bgcolor_positive_or_negative, subset=['Superficie Var %','Viñedos Var. %']).format(
        {"Superficie": lambda x : '{:,.0f}'.format(x), 
        "Viñedos Cnt.": lambda x : '{:,.0f}'.format(x),
        "Superficie Var %": lambda x : '{:,.2f} %'.format(x),
        "Viñedos Var. %": lambda x : '{:,.2f} %'.format(x),
                                        }
        ,
        thousands='.',
        decimal=',',
    )


    #st.write(df2)

    st.dataframe(styled_df,
      column_config={
        'Año': st.column_config.Column('Año'),
        'Superficie': st.column_config.Column('Superficie'),
        'Viñedos Cnt.': st.column_config.Column('Viñedos Cnt.'),
        'Superficie Var %': st.column_config.Column('Superficie Var %'),
        'Viñedos Var. %': st.column_config.Column('Viñedos Var. %'),
        
        },
        width = 600,   
        height = 800,
        hide_index=True)

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
            "data": df2['Año'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": df2['Superficie'].to_list(), "type": "line", "name": 'Supericie'}
               ,{"data": df2['Viñedos Cnt.'].to_list(), "type": "line","name":'Cnt. de Viñedos'}
                 
                  ]
    }
    st_echarts(
        options=option, height="400px" ,
    )
with tab2:
