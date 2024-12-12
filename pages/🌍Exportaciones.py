
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
df = conn.query('select anio,litros,fob from inf_expo_anio ;', ttl="0")
#st.write(df)
 
st.subheader('Evolución Exportaciones de vinos por año')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)


df['anio'] = df['anio'].astype(str)

newdf=df.set_index('anio',inplace=False).rename_axis(None)

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
    "yAxis": {"type": "value"},
    "series": [{"data": df['litros'].to_list(), "type": "line", "name": 'Litros'}
               ,{"data": df['fob'].to_list(), "type": "line","name":'Fob'}]
}
st_echarts(
    options=option, height="400px" ,
)


st.write('otro')

conn = st.connection("postgresql", type="sql")
dfp = conn.query('select value as Income, 0 as LifeExpectancy, 0 as Population,pais as country,anio as year from info_expo_anio_paises ;', ttl="0")
dff = conn.query('select pais,value  from info_expo_anio_paises ;', ttl="0")
#dfpe = conn.query('select distinct pais as country from info_expo_anio_paises ;', ttl="0")
#st.write(dfp['pais'])
json_list = json.loads(json.dumps(list(dfp.T.to_dict().values()))) 
tt = '[["Income","Life Expectancy","Population","Country","Year"],['
#st.write(tt)
f = dfp.to_json(orient="values")
f = f.replace("[[" ,tt)
#raw_data = json.load(dfp.to_json(orient="values"))
#st.write(f)  

json_str = dfp.to_json(orient='records')
json_obj = json.loads(f)

json_str1 = dff.to_json(orient='values')
json_obj1 = json.loads(f)


#st.write(json_obj)  
raw_data = json_obj


#with open("./data/life-expectancy-table.json") as f:
#        raw_data1 = json.load(f)
countries = [
        "DINAMARCA",
        "ESTADOS UNIDOS",
        "FRANCIA",
        "IRLANDA",
        "JAPON",
        "MEXICO",
        "NORUEGA",
        "REINO UNIDO",
        "PAISES BAJOS",
  ]
#"id": f"dataset_{country}",

datasetWithFilters = [
        {
            "id": f"dataset_{country}",
            "fromDatasetId": "dataset_raw",
            "transform": {
                "type": "filter",
                "config": {
                    "and": [
                        {"dimension": "Year", "gte": 2011},
                        {"dimension": "Country", "=": country},
                    ]
                },
            },
        }
        for country in countries
]

seriesList = [
        {
            "type": "line",
            "datasetId":f"dataset_{country}",
            "showSymbol": False,
            "name": country,
            "endLabel": {
                "show": True,
                "formatter": JsCode(
                    "function (params) { return params.value[3] + ': ' + params.value[0];}"
                ).js_code,
            },
            "labelLayout": {"moveOverlap": "shiftY"},
            "emphasis": {"focus": "series"},
            "encode": {
                "x": "Year",
                "y": "Income",
                "label": ["Country", "Income"],
                "itemName": "Year",
                "tooltip": ["Income"],
            },
        }
        for country in countries
]

option = {
        "animationDuration": 1000,
        "dataset": [{"id": "dataset_raw", "source": raw_data}] + datasetWithFilters,
        "title": {"text": "Exportaciones por paises"},
        "tooltip": {"order": "valueDesc", "trigger": "axis"},
        "xAxis": {"type": "category", "nameLocation": "middle"},
        "yAxis": {"name": "Income"},
        "grid": {"right": 100},
        "series": seriesList,
}
st_echarts(options=option, height="600px")



df1 = conn.query('select periodo,litros,fob from info_expo_anio_mes ;', ttl="0")
#st.write(df1)
 
st.subheader('Evolución Exportaciones de vinos por Mes')

if st.checkbox('Ver datos en  tabla'):
    st.write(df1)



df1['periodo'] = df1['periodo'].astype(str)

newdf1=df1.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['litros'].to_list(), "type": "line", "name": 'Litros'}
               ,{"data": df1['fob'].to_list(), "type": "line","name":'Fob'}]
}
st_echarts(
    options=option, height="400px" ,
)

df2 = conn.query('select name,value from info_expo_anio_variedad ;', ttl="0")
#st.write(df1)
json_list = json.loads(json.dumps(list(df2.T.to_dict().values()))) 
st.subheader('Exportaciones por Variedad')


option = {
    "tooltip": {
        #"trigger": 'axis',
        #"axisPointer": { "type": 'cross' },
        "formatter": JsCode(
            "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
        ).js_code,
    },
    "legend": {"data": ["litros","variedad1"]},   
    "series": [
            {
                "name": "Ventas Totales",
                "type": "treemap",
                "visibleMin": 100,
                "label": {"show": True, "formatter": "{b}"},
                "itemStyle": {"borderColor": "#fff"},
                "levels": [
                    {"itemStyle": {"borderWidth": 0, "gapWidth": 5}},
                    {"itemStyle": {"gapWidth": 1}},
                    {
                        "colorSaturation": [0.35, 0.5],
                        "itemStyle": {"gapWidth": 1, "borderColorSaturation": 0.6},
                    },
                ],
                "data": json_list,
            }
    ]
}
st_echarts(
    options=option, height="600px",
)




qu = 'select periodo,litros,producto from info_expo_anio_mes_tot ;'  
dfpv1 = conn.query(qu, ttl="0"),
#if prov != "Todas": 
#  qu = 'select cnt,provincia from inf_desp_prov where provincia =  :prov;'
#  dfpv1 = conn.query(qu, ttl="0", params={"prov": prov},),
dfpv1 = dfpv1[0]
#dfpv1 = dfpv1[dfpv1['periodo'] > '2010-12']

st.write(dfpv1)

df = dfpv1.pivot_table(index='periodo', columns='producto', values='litros')
#st.write('df')
#st.write(df)
df = df.reset_index() 
#st.write(df)
#st.write(df[2021])

dfpv2 = dfpv1.transpose()
#st.write(dfpv2)
#st.write('dfpv2')
#st.write(dfpv2.transpose())
ds = dfpv2.transpose(),



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
        "data": df['periodo'].to_list(),
    },
    "yAxis": [{"type": "value"}],
    "series": [
            {
                "name": "Espumantes",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['Espumantes'].to_list(),
            },
            {
                "name": "Gasificados",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['Gasificados'].to_list(),
            },
            {
                "name": "Otros Vinos",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['Otros Vinos'].to_list(),
            },
            {
                "name": "Vinos sin Mencion",
                "type": "line",
                "stack": "cnt",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['Vinos sin Mencion'].to_list(),
            },
            {
                "name": "Vino Varietal",
                "type": "line",
                "stack": "cnt",
                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data":  df['Vino Varietal'].to_list(),
            },
    ],    
}

st_echarts(
    options=option, height="400px" ,
)



st.write('por paises')
#st.write(json_str1)

options = {
        "tooltip": {
          #"trigger": 'axis',
          #"axisPointer": { "type": 'cross' },
          "formatter": JsCode(
              "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
          ).js_code,
        },
        "xAxis": {},
        "yAxis": {},
        "series": [
            {
                "symbolSize": 20,
                "data": json_str1,
                "type": "scatter",
            }
        ],
}
st_echarts(
      options=options, height="500px"
)
