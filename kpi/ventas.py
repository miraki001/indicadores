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
import pages as pg
from sqlalchemy import text
from streamlit import runtime


def ventas():

   dv1 = pd.read_parquet("data/processed/ventas.parquet", engine="pyarrow")
   actual = dt.now().year  
   anterior = dt.now().year -1  
   dva = dv1[dv1['TIPO'] == 'Nuevos' ]
   dva = dva[dva['ANIO'] == actual ]
   st.write(dva)

   dva = dva.reset_index().rename_axis(None, axis=1)
   #df = df.rename(columns={'litros': "Hl", 'subgrupoenvase': "Envase",'color': "color"})  
   #df = df.astype({'Hl': int } )      

   fig = px.sunburst(dva, path=['SUCURSAL_VTA', 'MARCA'], values='CNT',
                      color='MARCA', hover_data=['SUCURSAL_VTA'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(dva['index'], weights=dva['CNT']))
   st.plotly_chart(fig,key="indica5", theme="streamlit")	
