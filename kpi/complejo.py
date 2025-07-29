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



def complejo(dvex,dvdes,dvsup,dvcos,dvmosto):

  streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 400px;} 
   </style>
    """
  st.markdown(streamlit_style, unsafe_allow_html=True) 

    
  maxanio = max(dvex['anio'])
  anterior = maxanio -1  
  dres = pd.DataFrame(columns=['tipo','cnt','litros','kg','ha'])
  dvex = dvex[dvex['anio'] == anterior]  
  dvdes = dvdes[dvdes['anio'] == anterior]  
  dvcos = dvcos[dvcos['anio'] == anterior]  
  dvsup = dvsup[dvsup['anio'] == anterior]  
  dvmosto = dvmosto[dvmosto['anio'] == anterior]  
  dvcos1 = dvcos.groupby(['anio'], as_index=False)[['peso']].sum()
  cosecha = max(dvcos1['peso'])
  dvsup1 = dvsup.groupby(['anio'], as_index=False)[['sup']].sum()
  sup = max(dvsup1['sup'])
  rend = float(cosecha/sup)
  rend = rend * 100
  st.write(rend)
  st.write(cosecha)

  dvex1 = dvex.groupby(['anio'], as_index=False)[['litros']].sum()
  litros = max(dvex1['litros'])
  le = litros
  #st.write(dvex1)
  kg = int(litros *1.33)
  kge = kg
  ha = int(kg/rend)
  hae = ha
  ap = pd.DataFrame([{'tipo': 'Exportaciones', 'cnt': litros,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  
  dvdes1 = dvdes.groupby(['anio'], as_index=False)[['litros']].sum()
  litros = max(dvdes1['litros'])
  litros = litros * 100
  ld = litros
  kg = int(litros *1.33)
  kgd = kg
  ha = int(kg/rend)
  had = ha
  ap = pd.DataFrame([{'tipo': 'Despachos', 'cnt': litros,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  
  dvmo = dvmosto.groupby(['anio'], as_index=False)[['cantlitros']].sum()
  litros = max(dvmo['cantlitros'])
  lm = litros
  cnt = float(litros/734.5)
  #st.write(dvex1)
  kg = int(litros *1.33)
  kgm = kg
  ha = int(kg/rend)
  ham = ha
  ap = pd.DataFrame([{'tipo': 'Mosto', 'cnt': cnt,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    

  dvfes = dvcos[dvcos['destino'] == 'Consumo']
  dvfes = dvfes.groupby(['anio'], as_index=False)[['peso']].sum()
  kg = int(max(dvfes['peso']) * 100)
  kgf = kg
  ha = int(kg/rend)
  haf = ha
  ap = pd.DataFrame([{'tipo': 'Consumo en Fresco', 'cnt': kg,'litros': 0 , 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    

  dvsec = dvcos[dvcos['destino'] == 'Secado']
  dvsec = dvsec.groupby(['anio'], as_index=False)[['peso']].sum()
  kg = int(max(dvsec['peso']) * 100)
  kgp = kg
  ha = int(kg/rend)
  hap = ha
  ap = pd.DataFrame([{'tipo': 'Pasas', 'cnt': kg,'litros': 0 , 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  #dres['kg'].astype(int)
  #dres['ha'].astype(int)

  
  st.write(dres)
  dvex1 = dres['litros'] 
  dres1 = dres.drop('cnt', axis=1)
  dex =  dres1[dres1['tipo'] == 'Exportaciones']  
  dex = dex.drop('tipo', axis=1)

  #json_list = json.loads(json.dumps(list(dex.T.to_dict().values()))) 
  #st.write(dex)
  #pp =  dex.to_dict('list')
  #st.write(pp)

  options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": ["Exportaciones", "Despachos", "Mosto", "Consumo en Fresco", "Pasas"]
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": ["Litros", "Kg"],
        },
        "series": [
            {
                "name": "Exportaciones",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [le,kge],
            },
            {
                "name": "Despachos",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [ld,kgd],
            },
            {
                "name": "Mosto",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [lm,kgm],
            },
            {
                "name": "Consumo en Fresco",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [0,kgf],
            },
            {
                "name": "Pasas",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [0,kgp],
            },
        ],
    }
  st_echarts(options=options, height="500px")

  options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": ["Exportaciones", "Despachos", "Mosto", "Consumo en Fresco", "Pasas"]
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {"type": "value"},
        "yAxis": {
            "type": "category",
            "data": ["Ha"],
        },
        "series": [
            {
                "name": "Exportaciones",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [hae],
            },
            {
                "name": "Despachos",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [had],
            },
            {
                "name": "Mosto",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [ham],
            },
            {
                "name": "Consumo en Fresco",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [haf],
            },
            {
                "name": "Pasas",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [hap],
            },
            {
                "name": "Diferencia",
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [sup - (hae+had+haf+ham+hap)],
            },          
            {
                "name": "Superficie total",
                "type": "bar",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": [sup],
            },          
        ],
    }
  st_echarts(options=options, height="500px")


