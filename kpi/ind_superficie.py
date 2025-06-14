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
from script.exportaciones import mosto_registro_mensual



def ind_superficie(dva,dvc):

  streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 400px;} 
   </style>
    """
  st.markdown(streamlit_style, unsafe_allow_html=True) 

    
  maxanio = max(dva['anio'])
  anterior = maxanio -1  
  dbg = dva  
  dvb = dva
  dva = dva[dva['anio'] > maxanio -5 ]
  dsv = pd.read_parquet("data/processed/superficievariedad_datos.parquet", engine="pyarrow")  
  dsv = dsv[dsv['anio'] > maxanio -5 ]
  #st.write(dsv)
  #dva = dva.groupby(['anio'], as_index=False)[['sup']].sum()
  dvb = dvb[dvb['anio'] == maxanio-1 ]
  col = st.columns((4.5, 4.5), gap='medium')
  with col[0]:
    dv1 = dva.groupby(['anio'], as_index=False)[['sup']].sum()
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'sup' : int } )      
    #st.write(dva)

    option = {
      "tooltip": {
          "trigger": 'axis',
          "axisPointer": { "type": 'cross' }
      },
      "legend": {},  
      "title": {
                "text": 'Superficie Total',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
      },       
      "xAxis": {
          "type": "category",
          "data": dv1['anio'].to_list(),
      },
      "yAxis": {"type": "value"},
      "series": [{"data": dv1['sup'].to_list(), "type": "bar", "name": 'Ha', "color":'#dd6b66'},
               ]
    }
    #st_echarts(
    #  options=option, height="400px" ,
    #)
    st_echarts(options=option,key="otro333" + str(dt.now()), height="400px")



    
  with col[1]:
    dvb = dsv[dsv['color'] == 'Blanca' ]
    dvt = dsv[dsv['color'] == 'Tinta' ]
    dvr = dsv[dsv['color'] == 'Rosada' ]
    dv1 = dvb.groupby(['anio'], as_index=False)[['sup']].sum()
    dv2 = dvt.groupby(['anio'], as_index=False)[['sup']].sum()
    dv3 = dvr.groupby(['anio'], as_index=False)[['sup']].sum()
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'sup' : int } )      

    dv2.style.format(thousands='.')
    dv2.style.format(precision=0, thousands='.')
    dv2 = dv2.astype({'sup' : int } )      

    dv3.style.format(thousands='.')
    dv3.style.format(precision=0, thousands='.')
    dv3 = dv3.astype({'sup' : int } )      
    
    option = {
      "tooltip": {
          "trigger": 'axis',
          "axisPointer": { "type": 'cross' }
      },
      "legend": {},    
      "title": {
                "text": 'Superficie Por Color',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
      },      
      "xAxis": {
          "type": "category",
          "data": dv1['anio'].to_list(),
      },
      "yAxis": {"type": "value"},
      "series": [{"data": dv1['sup'].to_list(), "type": "bar", "name": 'Blanca', "color":'#1E8DB6'},
                 {"data": dv2['sup'].to_list(), "type": "bar", "name": 'Tinta', "color":'#dd6b66'},
                 {"data": dv3['sup'].to_list(), "type": "bar", "name": 'Rosada', "color":'#C92488'},
               ]
    }
    #st_echarts(
    #  options=option, height="400px" ,
    #)
    st_echarts(options=option,key="otro333" + str(dt.now()), height="400px")

  col1 = st.columns((4.5, 4.5), gap='medium')
  with col1[0]:
      st.write('')
      dva = dvc[dvc['anio'] > maxanio -5 ]
      dv1 = dva.groupby(['anio'], as_index=False)[['peso']].sum()
      dv1.style.format(thousands='.')
      dv1.style.format(precision=0, thousands='.')
      dv1 = dv1.astype({'peso' : int } )      
      #st.write(dva)

      option = {
        "tooltip": {
           "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},  
        "title": {
                  "text": 'Cosecha Total',
                  "textStyle": {
                          "fontSize": 12,
                  },                  
                  "subtext": '',
        },       
        "xAxis": {
            "type": "category",
            "data": dv1['anio'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dv1['peso'].to_list(), "type": "bar", "name": 'Tn', "color":'#dd6b66'},
               ]
      }
      #st_echarts(
      #  options=option, height="400px" ,
      #)
      st_echarts(options=option,key="otro333" + str(dt.now()), height="400px")
    
  
  with col1[1]:
    st.write('')
    dva = dvc[dvc['anio'] > maxanio -5 ]
    #st.write(dva)
    dvb = dva[dva['color'] == 'Blanca' ]
    dvt = dva[dva['color'] == 'Tinta' ]
    dvr = dva[dva['color'] == 'Rosada' ]
    dv1 = dvb.groupby(['anio'], as_index=False)[['peso']].sum()
    dv2 = dvt.groupby(['anio'], as_index=False)[['peso']].sum()
    dv3 = dvr.groupby(['anio'], as_index=False)[['peso']].sum()
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'peso' : int } )      

    dv2.style.format(thousands='.')
    dv2.style.format(precision=0, thousands='.')
    dv2 = dv2.astype({'peso' : int } )      

    dv3.style.format(thousands='.')
    dv3.style.format(precision=0, thousands='.')
    dv3 = dv3.astype({'peso' : int } )      
    
    option = {
      "tooltip": {
          "trigger": 'axis',
          "axisPointer": { "type": 'cross' }
      },
      "legend": {},    
      "title": {
                "text": 'Cosecha Por Color',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
      },      
      "xAxis": {
          "type": "category",
          "data": dv1['anio'].to_list(),
      },
      "yAxis": {"type": "value"},
      "series": [{"data": dv1['peso'].to_list(), "type": "bar", "name": 'Blanca', "color":'#1E8DB6'},
                 {"data": dv2['peso'].to_list(), "type": "bar", "name": 'Tinta', "color":'#dd6b66'},
                 {"data": dv3['peso'].to_list(), "type": "bar", "name": 'Rosada', "color":'#C92488'},
               ]
    }
    #st_echarts(
    #  options=option, height="400px" ,
    #)
    st_echarts(options=option,key="otro333" + str(dt.now()), height="400px")
