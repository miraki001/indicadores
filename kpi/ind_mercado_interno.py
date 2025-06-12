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
from streamlit_echarts import Map
from st_keyup import st_keyup
from util import desp_prov
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import locale


#streamlit_style = """
#    <style>
#    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
#   </style>
#    """
#st.markdown(streamlit_style, unsafe_allow_html=True) 

def ind_mercado_interno(dva):

  actual = dt.now().year  
  anterior = dt.now().year -1  
  dva = dva[dva['anio'] == actual ]
  #st.write(dva)
  mes = max(dva['mes'])
  mes2 = max(dva['mes1'])  
  st.write('Periodo : 01 Enero/' + mes2)
  col = st.columns((4.5, 4.5), gap='medium')
  with col[0]:
      dva1 = dva[dva['anio'] == actual ]
      st.write('Participación y evolución de los despachos por color, en HL')

      df_filtered = dva1.groupby(['color'], as_index=False)[['litros']].sum()
      df_anual = df_filtered.rename(columns={'litros': "value", 'color': "name",})

      json_list = json.loads(json.dumps(list(df_anual.T.to_dict().values()))) 
  
      option = {           
        "color": [
            '#dd6b66',
            '#759aa0',
            '#e69d87',
            '#8dc1a9',
            '#ea7e53',
            '#eedd78',
            '#73a373',
            '#73b9bc',
            '#7289ab',
            '#91ca8c',
            '#f49f42'
        ],            
        "tooltip": {
            "trigger": "item"
        },    
        "legend": {
            "top": "1%",
            "left": "center" 
            },
        "label": {
            "alignTo": 'edge',
#            "formatter": '{name|{b}}\n{time|{c} }',
            "formatter": '{name|{b}}\n  ({d}%)  ',
            "minMargin": 5,
            "edgeDistance": 10,
            "lineHeight": 15,
            "rich": {
              "time": {
              "fontSize": 8,
               "color": '#999'
              }
            }
          },    

        "series": [
            {
                "name": "año 2024",
                "type": "pie",
                "radius": ["30%", "50%"],
                "center": ["50%", "50%"],
                "startAngle": 180,
                "endAngle": 360,
                "data":json_list ,
            }
            ],
      }
      st_echarts(
            options=option,key="indica3", height="250px",
      )

  with col[1]:
    dva.loc[dva["subgrupoenvase"] == "Sachet", "subgrupoenvase"] = "Otros"
    dva.loc[dva["subgrupoenvase"] == "Bidon", "subgrupoenvase"] = "Otros"
    dva.loc[dva["subgrupoenvase"] == "Vasija", "subgrupoenvase"] = "Otros"
    dva.loc[dva["subgrupoenvase"] == "Fraccionamiento sin Sub Grupo", "subgrupoenvase"] = "Otros"
    dva.loc[dva["subgrupoenvase"] == "Granel", "subgrupoenvase"] = "Otros"
    df  = dva.groupby(['color','subgrupoenvase'], as_index=False)[['litros']].sum() 
    df_filtered = dva.groupby(['subgrupoenvase'], as_index=False)[['litros']].sum()
    #st.write(df_filtered)
    df_filtered = df_filtered.rename(columns={'litros': "value", 'subgrupoenvase': "name",})
    #st.write(df_anual)

    st.write('Participación de los despachos por tipo de envase , en HL')

    json_list = json.loads(json.dumps(list(df_filtered.T.to_dict().values()))) 
    option = {           
        "color": [
            '#dd6b66',
            '#759aa0',
            '#e69d87',
            '#8dc1a9',
            '#ea7e53',
            '#eedd78',
            '#73a373',
            '#73b9bc',
            '#7289ab',
            '#91ca8c',
            '#f49f42'
        ],            
        "tooltip": {
            "trigger": "item"
        },    
        "legend": {
            "top": "1%",
            "left": "center" 
            },
        "label": {
            "alignTo": 'edge',
#            "formatter": '{name|{b}}\n{time|{c} }',
            "formatter": '{name|{b}}\n  ({d}%)  ',
            "minMargin": 5,
            "edgeDistance": 10,
            "lineHeight": 15,
            "rich": {
              "time": {
              "fontSize": 8,
               "color": '#999'
              }
            }
          },    

        "series": [
            {
                "name": "año 2024",
                "type": "pie",
                "radius": ["30%", "50%"],
                "center": ["50%", "50%"],
                "startAngle": 180,
                "endAngle": 360,
                "data":json_list ,
            }
            ],
    }
    st_echarts(
            options=option,key="indica4", height="250px",
    )
    
  df = df.reset_index().rename_axis(None, axis=1)
  df = df.rename(columns={'litros': "Hl", 'subgrupoenvase': "Envase",'color': "color"})  
  fig = px.sunburst(df, path=['color', 'Envase'], values='Hl',
                      color='Envase', hover_data=['color'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df['index'], weights=df['Hl']))
  st.plotly_chart(fig,key="indica5", theme="streamlit")	
