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

def ind_exportaciones(dva):

  actual = dt.now().year  
  anterior = dt.now().year -1  
  dva = dva[dva['anio'] == actual ]
  st.write(dva)
  mes = max(dva['mes'])
  mes2 = max(dva['mes1'])  
  st.write('Periodo : 01 Enero/' + mes2)
  col = st.columns((4.5, 4.5), gap='medium')
  with col[0]:
    st.write('1')
  with col[1]:
    st.write('2')
