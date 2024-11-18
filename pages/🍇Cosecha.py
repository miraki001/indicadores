
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


conn = st.connection("postgresql", type="sql")
df = conn.query('select distinct anio from superficievariedad_m ;', ttl="0")
year_list = list(df.anio.unique())[::-1]

dv = conn.query('select distinct variedad from superficievariedad_m ;', ttl="0")
var_list = list(dv.variedad.unique())[::-1]

dp = conn.query('select distinct provincia from superficievariedad_m ;', ttl="0")
prov_list = list(dp.provincia.unique())[::-1]
color_list =  ("Tinto", "Blanco","Rosado","Sin Dato")
vcolor = '-1'

with st.popover("Abrir Filtros"):
    st.markdown("Filtros 🔎")
    anio = st.selectbox( "Año :", year_list )
    var = st.selectbox( "Variedad :", var_list )
    prov = st.selectbox( "Provincia :", prov_list )
    vcolor = st.selectbox( "Color :", color_list )
    st.button("Ok", type="primary")



tab1, tab2, tab3 = st.tabs(["Superficie", "Cosecha", "Rendimientos"])

with tab1:
    st.header("Cantidad de Viñedos")
    sql = "select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = ? or ?= '-1' group by anio order by anio",('Tinto')
    dv1 = conn.query(sql)
    #dv1 = conn.query('select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = %1 or %1= '-1' group by anio order by anio ;', ttl="0")
    st.write(dv1)
    dv1['anio'] = dv1['anio'].astype(str)

    newdf=dv1.set_index('anio',inplace=False).rename_axis(None)
    
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
            },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dv1['anio'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dv1['sup'].to_list(), "type": "line", "name": 'Hectareas'}
                   ,{"data": dv1['cnt'].to_list(), "type": "bar","name":'Cnt Viñedos'}]
    }
    st_echarts(
        options=option, height="400px" ,
    )

    
    
with tab2:
    st.header("A dog")
    
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
