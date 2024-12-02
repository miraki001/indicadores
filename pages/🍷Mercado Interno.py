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
df1 = conn.query('select anio||mes anio,tintos,blancos,rosados from info_desp_anio_mes_v1;', ttl="0"),

df2 = df1[0]
 
st.subheader('Evolución de los despachos por Mes')

if st.checkbox('Ver datos como tabla'):
    st.write(df)


#dfd['anio'] = dfd['anio'].astype(str)

#newdf=dfd.set_index('anio',inplace=False).rename_axis(None)

option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 30,
      "end": 70,
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

st.subheader('Evolución de los despachos por Provincias')
 
conn = st.connection("postgresql", type="sql")
dfp = conn.query('select provincia from dimprovincia;', ttl="0"),
dfpv = dfp[0]
new_row = pd.DataFrame({"provincia": ["Todas"]})
dfpv = pd.concat([dfpv, new_row], ignore_index=True)

#st.write(dfpv)
dfe = conn.query('select subgrupoenvase from dimsubgrupoenvase;', ttl="0"),
dfev = dfe[0]
new_row1 = pd.DataFrame({"subgrupoenvase": ["Todos"]})
dfev = pd.concat([dfev, new_row1], ignore_index=True)


col1, col2 = st.columns(2)

with col1:
  prov = st.multiselect(
      "Seleccionar Provincia",dfpv.provincia
  )
  all_options = st.button("Select all options")
  if all_options:
        prov = dfpv.provincia,
    
  #selected_options
with col2:
  envase = st.multiselect(
      "Seleccionar Tipo de Envase",dfev.subgrupoenvase
  )

st.write("You selected:", prov)
#if prov == "Todas":
qu = 'select año anio,sum(cnt) cnt,provincia from inf_desp_prov group by provincia,año ;'  
dfpv1 = conn.query(qu, ttl="0"),
#if prov != "Todas": 
#  qu = 'select cnt,provincia from inf_desp_prov where provincia =  :prov;'
#  dfpv1 = conn.query(qu, ttl="0", params={"prov": prov},),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2010]
dfpv1 = dfpv1[dfpv1['provincia'].isin(prov)]
st.write(dfpv1)

df = dfpv1.pivot_table(index='anio', columns='provincia', values='cnt')
st.write(df)
df = df.reset_index() 
st.write(df)
#st.write(df[2021])

dfpv2 = dfpv1.transpose()
st.write(dfpv2)
st.write(dfpv2.transpose())

#dfpv2['anio'] = dfpv2['anio'].astype(str)

#newdf=dfpv2.set_index('anio',inplace=False).rename_axis(None)

option = {
  "legend": {},
  "tooltip": {},
  "dataset": {
    "source": [
      df['provincia'].to_list(),
    ]
  },
  "xAxis": [
    { "type": 'category', "gridIndex": 0 },
    { "type": 'category', "gridIndex": 1 }
  ],
  "yAxis": [{ "gridIndex": 0 }, { "gridIndex": 1 }],
  "grid": [{ "bottom": '55%' }, { "top": '55%' }],
  "series": [
    { "type": 'bar', "seriesLayoutBy": 'row' },
    { "type": 'bar', "seriesLayoutBy": 'row' },
    { "type": 'bar', "seriesLayoutBy": 'row' },
    { "type": 'bar', "xAxisIndex": 1, "yAxisIndex": 1 },
    { "type": 'bar', "xAxisIndex": 1, "yAxisIndex": 1 },
    { "type": 'bar', "xAxisIndex": 1, "yAxisIndex": 1 },
    { "type": 'bar', "xAxisIndex": 1, "yAxisIndex": 1 }
  ]
};
st_echarts(
    options=option, height="400px" ,
)


option = {
    "dataZoom": [
    {
      "show": 'true',
      "realtime": 'true',
      "start": 30,
      "end": 70,
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
        "data": df['anio'].to_list(),
    },
    "yAxis": [{"type": "value"}],
    "series": [
            {
                "name": "Mendoza",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['MENDOZA'].to_list(),
            },
            {
                "name": "San Juan",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['SAN JUAN'].to_list(),
            },
            {
                "name": "La Rioja",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['LA RIOJA'].to_list(),
            },
            {
                "name": "Cordoba",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['CORDOBA'].to_list(),
            },
            {
                "name": "Catamarca",
                "type": "line",
                "stack": "cnt",
                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['CATAMARCA'].to_list(),
            },
            {
                "name": "Buenos Aires",
                "type": "line",
                "stack": "cnt",
                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":df['BUENOS AIRES'].to_list(),
            },
    ],    
}

st_echarts(
    options=option, height="400px" ,
)


