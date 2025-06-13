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
from script.exportaciones import registro_mensual
from script.exportaciones import mosto_registro_mensual
from kpi import ind_mercado_interno
from kpi import ind_exportaciones
from streamlit_extras.metric_cards import style_metric_cards 



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




st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #d5b7be;
    text-align: center;
    padding: 10px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)
#locale.setlocale(category=locale.LC_ALL, locale="France", "fr_FR.UTF-8")
locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """
st.markdown(streamlit_style, unsafe_allow_html=True) 

def _format_with_thousands_commas(val): 
  val = round(val,0)
  return f'{val:.12n}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}f}' 

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'


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
actual = dt.now().year  
anterior = dt.now().year -1  
dv2 = registro_mensual(anterior -1)
dva = dv2[dv2['anio'] == actual ]
dvex = dv2
mes = max(dva['mes'])
mes2 = max(dva['mes1'])
#dvm = mosto_registro_mensual(actual)


#dv2 = pd.read_parquet("data/processed/exportaciones.parquet", engine="pyarrow")

def gauge(value):
  option = {
    "tooltip": {
      "formatter": '{a} <br/>{b} : {c}%'
      },
    "series": [
      {
        "name": 'Current',
        "type": 'gauge',
        "progress": {
          "show": False
          },
        "axisLine": {
          "lineStyle": {
            "width": 6,
            "color": [
              [0.2, 'rgb(235, 34, 14)'],
              [0.4, 'rgb(242, 99, 9)'],
              [0.6, 'rgb(250, 197, 21)'],
              [0.8, 'rgb(117, 198, 5)'],
              [1, 'rgb(56, 182, 14)']
              ]
            }
          },
        "detail": {
          "valueAnimation": True,
          "formatter": f'{value}%',
          "color": 'auto'
          },
        "data": [
          {
            "value": value,
            "name": 'Hl'
            },
          ]
        }
      ]
    }
  st_echarts(option, height="400px", key="echarts-1")

df_filtered = dv1.copy() 
#actual = dt.now().year -4 
tab1, tab2, tab3,tab4 = st.tabs(["Indicadores","Exportaciones", "Mercado Interno", "Cosecha y Superficie"])

with tab1:
   st.write('Periodo : 01 Enero/' + mes2)

   col = st.columns((4.5, 4.5, 4.5), gap='medium')

   with col[0]:
      dva = dv1[dv1['anio'] == actual ]
      dvo = dv1[dv1['anio'] == anterior ]
      dvoa = dv1[dv1['anio'] == anterior-1 ]
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      dvo = dvo[dvo['mes']  <= mes]
      dvoa = dvoa[dvoa['mes']  <= mes]
      vala = dva['litros'].sum()
      valo = dvo['litros'].sum()
      valoa = dvoa['litros'].sum()
      #st.write(valoa)
      deltaoa = valo/valoa
      if deltaoa < 1:
        deltaoa = (1- deltaoa) * -1
     
      deltao = valo/vala
      if deltao < 1:
        deltao = (1- deltao) * -1
      deltaa = vala/valo
      if deltaa < 1:
        deltaa = (1- deltaa) * -1
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      st.metric(label='Despachos ' + str(anterior), value=valoro + '  Hl.', delta=_format_as_percentage(deltaoa,2) +'%' )
      st.metric(label='Despachos ' + str(actual), value=valora + '  Hl.', delta=_format_as_percentage(deltaa,2) +'%')
      #gauge(1500)
   with col[1]:
      #st.write(dv2)
      #st.write(max(dvo['mes']))
      #echarts_module.gauge(1500)
      dva = dv2[dv2['anio'] == actual ]
      dvo = dv2[dv2['anio'] == anterior ]
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      dvo = dvo[dvo['mes']  <= mes]
      vala = dva['litros'].sum()/100
      valo = dvo['litros'].sum()/100
      deltao = valo/vala
      if deltao < 1:
        deltao = (1- deltao) * -1
      deltaa = vala/valo
      if deltaa < 1:
        deltaa = (1- deltaa) * -1

      dvoa = dv1[dv1['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['litros'].sum()
      deltaoa = valo/valoa
      if deltaoa < 1:
        deltaoa = (1- deltaoa) * -1     
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      st.metric(label='Exportaciones de Vinos ' + str(anterior), value=valoro + '  Hl.', delta=_format_as_percentage(deltaoa,2) +'%' )
      st.metric(label='Exportaciones de Vinos ' + str(actual), value=valora + '  Hl.', delta=_format_as_percentage(deltaa,2) +'%')

   with col[2]:
      dv2 = registro_mensual(anterior -1)
      #st.write(dv2)
      #st.write(max(dvo['mes']))
      #echarts_module.gauge(1500)
      dva = dv2[dv2['anio'] == actual ]
      dvo = dv2[dv2['anio'] == anterior ]
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      dvo = dvo[dvo['mes']  <= mes]
      vala = dva['fob'].sum()/100
      valo = dvo['fob'].sum()/100
      deltao = valo/vala
      if deltao < 1:
        deltao = (1- deltao) * -1
      deltaa = vala/valo
      if deltaa < 1:
        deltaa = (1- deltaa) * -1
      dvoa = dv1[dv1['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['litros'].sum()
      deltaoa = valo/valoa
      if deltaoa < 1:
        deltaoa = (1- deltaoa) * -1           
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      st.metric(label='Exportaciones de Vinos ' + str(anterior), value=valoro + '  u$s.', delta=_format_as_percentage(deltaoa,2) +'%' )
      st.metric(label='Exportaciones de Vinos ' + str(actual), value=valora + '  u$s.', delta=_format_as_percentage(deltaa,2) +'%')


   colm = st.columns((4.5, 4.5), gap='medium')
   with colm[0]:
      # mosto en toneladas
      dv2 = mosto_registro_mensual(anterior -2)
      #st.write(dv2)
      #st.write(max(dvo['mes']))
      #echarts_module.gauge(1500)
      dva = dv2[dv2['anio'] == actual ]
      dvo = dv2[dv2['anio'] == anterior ]
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      dvo = dvo[dvo['mes']  <= mes]
      vala = dva['litros'].sum()
      #st.write(vala)
      valo = dvo['litros'].sum()
      deltao = valo/vala
      if deltao < 1:
        deltao = (1- deltao) * -1
      deltaa = vala/valo
      if deltaa < 1:
        deltaa = (1- deltaa) * -1
        

      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['litros'].sum()
      st.write(valo)
      st.write(valoa)
      deltaoa = valo/valoa
      if deltaoa < 1:
        deltaoa = (1- deltaoa) * -1        
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      st.metric(label='Exportaciones de Mostos ' + str(anterior), value=valoro + ' Tn. ', delta=_format_as_percentage(deltaoa,2) +'%' )
      st.metric(label='Exportaciones de Mostos ' + str(actual), value=valora + ' Tn. ', delta=_format_as_percentage(deltaa,2) +'%')
   
   with colm[1]:
      dv2 = mosto_registro_mensual(anterior -2)
      #st.write(dv2)
      #st.write(max(dvo['mes']))
      #echarts_module.gauge(1500)
      dva = dv2[dv2['anio'] == actual ]
      dvo = dv2[dv2['anio'] == anterior ]
      mes = max(dva['mes'])
      dvam = dva[dv1['mes'] == mes ]
      dvo = dvo[dvo['mes']  <= mes]
      vala = dva['fob'].sum()
      valo = dvo['fob'].sum()
      deltao = valo/vala
      if deltao < 1:
        deltao = (1- deltao) * -1
      deltaa = vala/valo
      if deltaa < 1:
        deltaa = (1- deltaa) * -1

      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      #st.write(dvoa)
      valoa = dvoa['litros'].sum()
      #st.write(valoa)
      deltaoa = valo/valoa
      if deltaoa < 1:
        deltaoa = (1- deltaoa) * -1        
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      st.metric(label='Exportaciones de Mostos ' + str(anterior), value=valoro + '  u$s.', delta=_format_as_percentage(deltaoa,2) +'%' )
      st.metric(label='Exportaciones de Mostos ' + str(actual), value=valora + '  u$s.', delta=_format_as_percentage(deltaa,2) +'%')

   colo = st.columns((4.5, 4.5), gap='medium')

   with colo[0]:
     st.metric(label='Superficie ' + str(anterior), value= str(1) + '', delta=_format_as_percentage(1,2) +'%' )
     st.metric(label='Superficie ' + str(actual), value= str(1) + ' ', delta=_format_as_percentage(1,2) +'%')
   with colo[1]:
     st.metric(label='Cosecha ' + str(anterior), value= str(1) + '', delta=_format_as_percentage(1,2) +'%' )
     st.metric(label='Cosecha ' + str(actual), value= str(1) + ' ', delta=_format_as_percentage(1,2) +'%')
            
with tab2:
  st.write('vacio')
  ind_exportaciones.ind_exportaciones(dvex)

  
with tab3:
  ind_mercado_interno.ind_mercado_interno(dv1)

with tab4:
  st.write('vacio')
  wch_colour_box = (0,204,102)
  wch_colour_font = (0,0,0)
  fontsize = 18
  valign = "left"
  iconname = "fas fa-asterisk"
  sline = "Observations"
  lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
  i = 123

  htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 14px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

  st.markdown(lnk + htmlstr, unsafe_allow_html=True)
  
  col1, col2, col3 = st.columns(3)

  col1.metric(label="Gain", value=5000, delta=1000)
  col2.metric(label="Loss", value=5000, delta=-1000)
  col3.metric(label="No Change", value=5000, delta=0)

  style_metric_cards()  

