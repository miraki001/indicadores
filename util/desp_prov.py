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

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"


def despachos_prov(df):
      pivot_table_basic = df.pivot_table(
            index='provincia', 
            columns='anio',  
            values=['lts'],
            aggfunc='sum'
          )
    
      dfg = pivot_table_basic
      dfg.columns = dfg.columns.droplevel(0)
      dfg = dfg.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})
      st.write(dfg) 

      pivot_table_basic = pivot_table_basic.reset_index().rename_axis(None, axis=1)
      pivot_table_basic.loc['Total']= pivot_table_basic.sum(numeric_only=True,axis=0)
      pivot_table_basic['2023/2022'] = (1-(pivot_table_basic[2022]/pivot_table_basic[2023]))*100
      pivot_table_basic['2024/2023'] = (1-(pivot_table_basic[2023]/pivot_table_basic[2024]))*100
      pivot_table_basic = pivot_table_basic.rename(columns={2022: "2022", 2023: "2023", 2024: "2024",'mes': " mes"})

      pivot_table_basic = pivot_table_basic.sort_index(axis = 1)


      styled_df = pivot_table_basic.style.applymap(bgcolor_positive_or_negative, subset=['2023/2022','2024/2023']).format(
        {"2022": lambda x : '{:,.0f}'.format(x), 
        "2023": lambda x : '{:,.0f}'.format(x),
        "2024": lambda x : '{:,.0f}'.format(x),
        "2023/2022": lambda x : '{:,.2f} %'.format(x),
        "2024/2023": lambda x : '{:,.2f} %'.format(x),
                                        }
        ,
      thousands='.',
      decimal=',',
      )


    
    
      st.dataframe(styled_df,
      column_config={
        'mes': st.column_config.Column('Key'),
        '2022': st.column_config.Column('2022'),
        '2023': st.column_config.Column('2023'),
        '2024': st.column_config.Column('2024'),
        '2023/2022': st.column_config.Column('2023/2022'),
        '2024/2023': st.column_config.Column('2024/2023')
      },
      width = 600,   
      height = 500,
      hide_index=False)

      dfg = dfg.reset_index().rename_axis(None, axis=1)
      #st.write(dfg)  
    
      #dfg['mes'] = dfg['mes'].astype(str)

      #newdf=dfg.set_index('mes',inplace=False).rename_axis(None)

      option = {
        "dataZoom": [
        {
          "show": 'true',
          "realtime": 'true',
          "start": 0,
          "end": 100,
          "xAxisIndex": [0, 1]
        },
        {
          "type": 'inside',
          "realtime": 'true',
          "start": 30,
          "end": 70,
          "xAxisIndex": [0, 1]
        }
        ],
            "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dfg['mes'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dfg['2022'].to_list(), "type": "line", "name": '2022'}
               ,{"data": dfg['2023'].to_list(), "type": "line","name":'2023'}
               ,{"data": dfg['2024'].to_list(), "type": "line","name":'2024'}                   
                  ]
      }
      st_echarts(
        options=option, height="400px" ,
      )

