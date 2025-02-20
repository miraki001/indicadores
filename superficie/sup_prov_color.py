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

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

def prov_color(df):
  pivot_table_basic = df.pivot_table(
      index='provincia', 
      columns='color',  
      values=['sup'],
      aggfunc='sum'
  )
  #st.write(pivot_table_basic)  
  dfg = pivot_table_basic
  dfg.columns = dfg.columns.droplevel(0)
  dfg = dfg.reset_index().rename_axis(None, axis=1)
  #st.write(dfg) 

  total = []
  #total.append(0)
  for index in range(len(dfg)):
      total.append(  dfg['Blanca'].loc[index]  + dfg['Rosada'].loc[index]  + dfg['Tinta'].loc[index] )

  pivot_table_basic['Total Prov.'] = total  

  #st.write(pivot_table_basic)

  pivot_table_basic['Blanca %'] = ((pivot_table_basic['Blanca']/pivot_table_basic['Total Prov.']))*100
  pivot_table_basic['Rosada %'] = ((pivot_table_basic['Rosada']/pivot_table_basic['Total Prov.']))*100
  pivot_table_basic['Tinta %'] = ((pivot_table_basic['Tinta']/pivot_table_basic['Total Prov.']))*100
  #pivot_table_basic = pivot_table_basic.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)
  #st.write(pivot_table_basic)

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)


  styled_df = pivot_table_basic.style.applymap(bgcolor_positive_or_negative, subset=['Blanca %','Rosada %','Tinta %']).format(
        {"Blanca": lambda x : '{:,.0f}'.format(x), 
        "Rosada": lambda x : '{:,.0f}'.format(x),
        "Tinta": lambda x : '{:,.0f}'.format(x),
        "Blanca %": lambda x : '{:,.2f} %'.format(x),
        "Rosada %": lambda x : '{:,.2f} %'.format(x),
        "Tinta %": lambda x : '{:,.2f} %'.format(x), 
        "Total Prov.": lambda x : '{:,.0f}'.format(x),
                                        }
        ,
    thousands='.',
    decimal=',',
  )
  st.dataframe(styled_df,
      column_config={
        'provincia': st.column_config.Column('provincia'),
        'Blanca': st.column_config.Column('Blanca'),
        'Rosada': st.column_config.Column('Rosada'),
        'Tinta': st.column_config.Column('Tinta'),
        'Blanca %': st.column_config.Column('Blanca %'),
        'Rosada %': st.column_config.Column('Rosada %'),
        'Tinta %': st.column_config.Column('Tinta %'),
        'Total Prov.': st.column_config.Column('Total Prov.')  
      },
      width = 600,   
      height = 500,
      hide_index=False
  )

    
