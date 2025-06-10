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
from despachos import desp_prov
from despachos import desp_color
from despachos import desp_envase
from despachos import desp_variedad
from despachos import desp_consumo
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(initial_sidebar_state="collapsed",
                  layout="wide",menu_items=None)



def _format_with_thousands_commas(val): 
  return f'{val:.,0f}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}%}' 


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

dv1 = pd.read_parquet("data/processed/despachos_datos.parquet", engine="pyarrow")

df_filtered = dv1.copy() 
actual = dt.now().year -4 
tab1, tab2, tab3,tab4 = st.tabs(["Indicadores","Exportaciones", "Mercado Interno", "Cosecha y Superficie"])

with tab1:
   st.header("Indicadores")

   col = st.columns((1.5, 4.5, 2), gap='medium')

   with col[0]:
      actual = dt.now().year  
      anterior = dt.now().year -1  
      dva = dv1[dv1['anio'] == actual ]
      dvo = dv1[dv1['anio'] == anterior ]
      st.write(dva)
      st.write(max(dva['mes']))
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      
      mes2 = max(dva['mes1'])
      st.write(mes2)
   with col[1]:
      st.write(dvo)
      st.write(max(dvo['mes']))
               
with tab2:
  st.write('vacio')
  
with tab3:
  st.write('vacio')  
with tab4:
  st.write('vacio')
  
  

