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
  #st.write(dvex1)
  kg = int(litros *1.33)
  ha = int(kg/rend)
  ap = pd.DataFrame([{'tipo': 'Exportaciones', 'cnt': litros,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  
  dvdes1 = dvdes.groupby(['anio'], as_index=False)[['litros']].sum()
  litros = max(dvdes1['litros'])
  litros = litros * 100
  kg = int(litros *1.33)
  ha = int(kg/rend)
  ap = pd.DataFrame([{'tipo': 'Despachos', 'cnt': litros,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  
  dvmo = dvmosto.groupby(['anio'], as_index=False)[['cantlitros']].sum()
  litros = max(dvmo['cantlitros'])
  cnt = float(litros/734.5)
  #st.write(dvex1)
  kg = int(litros *1.33)
  ha = int(kg/rend)
  ap = pd.DataFrame([{'tipo': 'Mosto', 'cnt': cnt,'litros': litros, 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    

  dvfes = dvcos[dvcos['destino'] == 'Consumo']
  dvfes = dvfes.groupby(['anio'], as_index=False)[['peso']].sum()
  kg = int(max(dvfes['peso']))
  ha = int(kg/rend)
  ap = pd.DataFrame([{'tipo': 'Consumo en Fresco', 'cnt': kg,'litros': 0 , 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    

  dvsec = dvcos[dvcos['destino'] == 'Secado']
  dvsec = dvsec.groupby(['anio'], as_index=False)[['peso']].sum()
  kg = int(max(dvsec['peso']))
  ha = int(kg/rend)
  ap = pd.DataFrame([{'tipo': 'Pasas', 'cnt': kg,'litros': 0 , 'kg': kg,'ha': ha}])
  dres = pd.concat([dres,ap])    
  #dres['kg'].astype(int)
  #dres['ha'].astype(int)

  
  st.write(dres)
