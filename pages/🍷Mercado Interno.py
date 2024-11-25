import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line


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



conn = st.connection("postgresql", type="sql")
dfd = conn.query('select anio,tintos,blancos,rosados from info_desp_anio_v1;', ttl="0"),

df = dfd[0]
 
st.subheader('Evolución de los despachos por año')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)


#dfd['anio'] = dfd['anio'].astype(str)

#newdf=dfd.set_index('anio',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df['anio'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df['tintos'].to_list(), "type": "line", "name": 'Tintos'},
               {"data": df['blancos'].to_list(), "type": "line", "name": 'Blancos'},
               {"data": df['rosados'].to_list(), "type": "line", "name": 'Rosados'},
               ]
}
st_echarts(
    options=option, height="400px" ,
)


conn = st.connection("postgresql", type="sql")
df1 = conn.query('select anio,tintos,blancos,rosados from info_desp_anio_mes_v1;', ttl="0"),

df2 = df1[0]
 
st.subheader('Evolución de los despachos por Mes')

if st.checkbox('Ver datos como tabla'):
    st.write(df)


#dfd['anio'] = dfd['anio'].astype(str)

#newdf=dfd.set_index('anio',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df2['anio'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df2['tintos'].to_list(), "type": "line", "name": 'Tintos'},
               {"data": df2['blancos'].to_list(), "type": "line", "name": 'Blancos'},
               {"data": df2['rosados'].to_list(), "type": "line", "name": 'Rosados'},
               ]
}
st_echarts(
    options=option, height="400px" ,
)
