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


streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 1000px;} 
   </style>
    """
st.markdown(streamlit_style, unsafe_allow_html=True) 

def ind_exportaciones(dva):

  streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 1000px;} 
   </style>
    """
  st.markdown(streamlit_style, unsafe_allow_html=True) 

    
  actual = dt.now().year  
  anterior = dt.now().year -1  
  dbg = dva  
  dva = dva[dva['envase'] == 'FRACCIONADO']  
  dvb = dva
  dva = dva[dva['anio'] == actual ]
  dvb = dvb[dvb['anio'] == actual-1 ]
  mes = max(dva['mes'])
  mes2 = max(dva['mes1'])  
  dvb = dvb[dvb['mes'] <= mes ]
  st.write('Periodo : 01 Enero/' + mes2)
  col = st.columns((4.5, 4.5), gap='medium')
  with col[0]:
    dv1 = dva.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()
    dv2 = dvb.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()

    #dv1 = dv1.style.format({"litros": "{:.2f}".format})
    #dv1, column_config={ format=",", ) }
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'fob' : int, 'litros': int } )      
    dv2 = dv2.astype({'fob' : int, 'litros': int } )      
    #st.write(dv1)
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
                "text": 'Fraccionado',
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
                {"data": dv1['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(actual),"yAxisIndex": 1, "color":'#1E8DB6'  },
                {"data": dv2['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(anterior),"yAxisIndex": 1, "color":'#dd6b66'  },
                {"data": dv1['fob'].tolist(), "type": "line", "name": 'u$s ' + str(actual), "yAxisIndex": 2,  "color":'#C92488'},
                {"data": dv2['fob'].tolist(), "type": "line", "name": 'u$s ' + str(anterior), "yAxisIndex": 2,  "color":'#604994'},
                
            ],
    }

    st_echarts(options=option,key="otro33" + str(dt.now()), height="400px")

  
    
  with col[1]:

    dva1 = dbg[dbg['envase'] == 'GRANEL']  
    dvb = dva1
    dva1 = dva1[dva1['anio'] == actual ]
    dvb = dvb[dvb['anio'] == actual-1 ]
    mes = max(dva1['mes'])
    mes2 = max(dva1['mes1'])  
    dvb = dvb[dvb['mes'] <= mes ]
      
    dv1 = dva1.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()
    dv2 = dvb.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()

    #dv1 = dv1.style.format({"litros": "{:.2f}".format})
    #dv1, column_config={ format=",", ) }
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'fob' : int, 'litros': int } )      
    dv2 = dv2.astype({'fob' : int, 'litros': int } )      
    #st.write(dv1)
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
                "text": 'Granel',
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
                {"data": dv1['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(actual),"yAxisIndex": 1, "color":'#1E8DB6'  },
                {"data": dv2['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(anterior),"yAxisIndex": 1, "color":'#dd6b66'  },
                {"data": dv1['fob'].tolist(), "type": "line", "name": 'u$s ' + str(actual), "yAxisIndex": 2,  "color":'#C92488'},
                {"data": dv2['fob'].tolist(), "type": "line", "name": 'u$s ' + str(anterior), "yAxisIndex": 2,  "color":'#604994'},
                
            ],
    }

    st_echarts(options=option,key="otro33" + str(dt.now()), height="400px")
      
  col1 = st.columns((4.5, 4.5), gap='medium')
  with col1[0]:
    dv2 = mosto_registro_mensual(anterior -1)

    dva = dv2[dv2['anio'] == actual ]
    dvb = dv2[dv2['anio'] == actual-1 ]
    mes = max(dva['mes'])
    mes2 = max(dva['mes1'])  
    dvb = dvb[dvb['mes'] <= mes ]
      
      
    dv1 = dva.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()
    dv2 = dvb.groupby(['anio','mes1'], as_index=False)[['fob', 'litros']].sum()

    #dv1 = dv1.style.format({"litros": "{:.2f}".format})
    #dv1, column_config={ format=",", ) }
    dv1.style.format(thousands='.')
    dv1.style.format(precision=0, thousands='.')
    dv1 = dv1.astype({'fob' : int, 'litros': int } )      
    dv2 = dv2.astype({'fob' : int, 'litros': int } )      
    #st.write(dv1)
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
                "text": 'Mosto',
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
                {"data": dv1['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(actual),"yAxisIndex": 1, "color":'#1E8DB6'  },
                {"data": dv2['litros'].tolist(), "type": "bar", "name": 'Lts. ' + str(anterior),"yAxisIndex": 1, "color":'#dd6b66'  },
                {"data": dv1['fob'].tolist(), "type": "line", "name": 'u$s ' + str(actual), "yAxisIndex": 2,  "color":'#C92488'},
                {"data": dv2['fob'].tolist(), "type": "line", "name": 'u$s ' + str(anterior), "yAxisIndex": 2,  "color":'#604994'},
                
            ],
    }

    st_echarts(options=option,key="otro33" + str(dt.now()), height="400px")

  
    
  with col1[1]:
