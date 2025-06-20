import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import locale
from despachos import desp_consumo
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def handle_card_click(card_name):
    st.session_state.click_message = f"'{card_name}' was clicked!"
    st.toast(f"Clicked: {card_name}")
    #desp_consumo.despachos_consumo() 

def _format_with_thousands_commas(val): 
  val = round(val,0)
  return f'{val:.12n}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}f}' 


def indica2(dv1):
    actual = dt.now().year  
    anterior = dt.now().year -1 
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
    #st.write(valo)
    deltaoa = valo/valoa
    deltaoa = (deltaoa -1)*100
    #if deltaoa < 1:
    #  deltaoa = (1- deltaoa) * -1
     
    deltao = valo/vala
    if deltao < 1:
        deltao = (1- deltao) * -1
    deltaa = vala/valo
    deltaa = (deltaa - 1)*100
    valoro = str(_format_with_thousands_commas(valo)) 
    valora = str(_format_with_thousands_commas(vala)) 
    delta1 = str(_format_as_percentage(deltaoa,2))
    delta2 = str(_format_as_percentage(deltaa,2))
    mes2 = max(dva['mes1'])
    col = st.columns((4.5, 4.5), gap='small')
    with col[0]:
      fig1 = go.Figure(go.Indicator(
      mode = "number+delta",
      #gauge = {'shape': "bullet"},
      delta = {'reference': valoa},
      value = valo,
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Despachos 2024"}))
      #fig.add_trace(go.Scatter(
      #  x = dv1['anio'],
      #  y = dv1['litros']))
      #fig.add_trace(
      #  go.add_bar(x=dv1.mes1, y=dv1.litros)
      #)    
      fig1.add_bar(x = dvoa.mes1,  y = dvoa.litros)
      #fig.update_layout(paper_bgcolor = "lightgray")
      fig1.show()
      st.plotly_chart(fig1, theme="streamlit", key="desp1")
    with col[1]:
      fig2 = go.Figure(go.Indicator(
      mode = "number+delta",
      #gauge = {'shape': "bullet"},
      delta =  {'reference': valoa},
      value = valo,
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Despachos 2024"}))
      #fig.add_trace(go.Scatter(
      #  x = dv1['anio'],
      #  y = dv1['litros']))
      #fig.add_trace(
      #  go.add_bar(x=dvoa.mes1, y=dvoa.litros)
      #)    
      fig2.add_bar(x = dvoa.mes1,  y = dvoa.litros)
      #fig.update_layout(paper_bgcolor = "lightgray")
      fig2.show()
      st.plotly_chart(fig2, theme="streamlit", key="desp2")
