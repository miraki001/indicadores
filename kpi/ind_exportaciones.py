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
  dvb = dva
  dva = dva[dva['anio'] == actual ]
  dvb = dvb[dvb['anio'] == actual-1 ]
  #st.write(dva)
  mes = max(dva['mes'])
  mes2 = max(dva['mes1'])  
  dvb = dvb[dvb['mes'] <= mes ]
  st.write('Periodo : 01 Enero/' + mes2)
  col = st.columns((4.5, 4.5), gap='medium')
  with col[0]:
    st.write('1')
    dv1 = dva.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()
    dv2 = dvb.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()
    st.write(dv1)

    option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "title": {
                "text": 'Exportaciones ',
                "textStyle": {
                        "fontSize": 14,
                },                  
                "subtext": '',
            },            
            "xAxis": {"type": "category", "data": dv1["mes1"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Litros" ,
                 "axisLine": {
                    "show": 'true',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,
                {"type": "value" , "name" : "",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,
                 "axisLine": {
                    "show": 'false',
                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },
                {"type": "value" , "name" : "u$s",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                },            
            ],            
            #"yAxis": {"type": "value"},
            "series": [
                {"data": dv1['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(actual),"yAxisIndex": 1, "color":'#332D75'  },
                {"data": dv2['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(anterior),"yAxisIndex": 1, "color":'#FCE2D6'  },
                {"data": dv1['fob'].tolist(), "type": "line", "name": 'u$s ' + str(actual), "yAxisIndex": 2,  "color":'#C92488'},
                {"data": dv2['fob'].tolist(), "type": "line", "name": 'u$s ' + str(anterior), "yAxisIndex": 2,  "color":'#604994'},
                
            ],
    }

    st_echarts(options=option,key="otro33" + str(dt.now()), height="600px")

  
    
  with col[1]:
    st.write('2')
