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

def despachos_prov(df):
      pivot_table_basic = df.pivot_table(
            index='provicnia', 
            columns='anio',  
            values=['lts'],
            aggfunc='sum'
          )
    
      dfg = pivot_table_basic
      dfg.columns = dfg.columns.droplevel(0)
      dfg = dfg.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})
      st.write(dfg) 
