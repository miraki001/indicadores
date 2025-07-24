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



def complejo(dvex,dvdes,dvsup,dvcos):

  streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 400px;} 
   </style>
    """
  st.markdown(streamlit_style, unsafe_allow_html=True) 

    
  maxanio = max(dva['anio'])
  anterior = maxanio -1  
  dres = pd.DataFrame(columns=['tipo','cnt','litros','kg','ha'])
  dvex = dvex[dvex['anio'] == anterior]  
  dvex1 = dvex.groupby(['anio'], as_index=False)[['litros']].sum()
  st.write(dvex1)
