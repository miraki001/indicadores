import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line

def sup_prov_color(df):
  pivot_table_basic = df.pivot_table(
      index='provincia', 
      columns='color',  
      values=['sup'],
      aggfunc='sum'
  )
  st.write(pivot_table_basic)  
  dfg = pivot_table_basic
  dfg.columns = dfg.columns.droplevel(0)
  #st.write(dfg) 
    
  #pivot_table_basic.columns = pivot_table_basic.columns.droplevel(0)
  pivot_table_basic = pivot_table_basic.reset_index().rename_axis(None, axis=1)
  pivot_table_basic.loc['Total']= pivot_table_basic.sum(numeric_only=True,axis=0)
  pivot_table_basic['2023/2022'] = (1-(pivot_table_basic[2022]/pivot_table_basic[2023]))*100
  pivot_table_basic['2024/2023'] = (1-(pivot_table_basic[2023]/pivot_table_basic[2024]))*100
  pivot_table_basic = pivot_table_basic.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)
