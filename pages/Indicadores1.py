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
from kpi import ind_superficie
from kpi import indica1
from kpi import indica2
from streamlit_extras.metric_cards import style_metric_cards 
from streamlit_product_card import product_card 
import pages as pg

st.set_page_config(initial_sidebar_state="collapsed",
                  layout="wide",menu_items=None)


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
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
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

def bgcolor_positive_or_negative(value):
    bgcolor = "#EC2E35" if value < 0 else "#E3E5E9"
    #st.write(bgcolor)
    #return f"color: {bgcolor};"
    return bgcolor
  
def handle_card_click(card_name):
    st.session_state.click_message = f"'{card_name}' was clicked!"
    st.toast(f"Clicked: {card_name}")
    #st.Page(pg.show_exportaciones, title="Exportaciones") 
    #st.switch_page("./pages/🍷Mercado Interno.py")
    st.switch_page("./pages/filtros.py")
  
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
dv2 = registro_mensual(anterior -2)
dva = dv2[dv2['anio'] == actual ]
dvex = dv2
mes = max(dva['mes'])
mes2 = max(dva['mes1'])
#dvm = mosto_registro_mensual(actual)
dfsup = pd.read_parquet("data/processed/superficie_datos.parquet", engine="pyarrow")
maxanio = max(dfsup['anio'])
#st.write(dfsup)
dfcos = pd.read_parquet("data/processed/cosecha_datos.parquet", engine="pyarrow")
style_metric_cards() 

meses_es = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

#mesfin = lambda x: meses_es[x](mes)
dva['mes_int'] = dva['mes'].astype(int)
dva['nombre_mes'] = dva['mes_int'].apply(lambda x: meses_es[x])
mesfin = max(dva[dva['mes'] == mes]['nombre_mes'])
#st.write(dva)

#st.write(mesfin)



#dv2 = pd.read_parquet("data/processed/exportaciones.parquet", engine="pyarrow")

df_filtered = dv1.copy() 
#actual = dt.now().year -4 
tab1, tab2, tab3,tab4,tab5,tab6,tab7 = st.tabs(["Indicadores","Exportaciones", "Mercado Interno", "Cosecha y Superficie","Indica 1","Indica 2","Indica 3"])

with tab1:
   #st.write('Datos acumulados de Enero a  ' + mesfin + ' de cada año' )

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
      #if deltaa < 1:
      #  deltaa = (1- deltaa) * -1
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      delta2 = str(_format_as_percentage(deltaa,2))
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)

      product_card(
            #product_name=delta2 + " %",
            product_name='Despachos ' + mesfin + ' ' + str(actual) ,
            #description='Despachos ' + mesfin + ' ' + str(actual)  , 
            description=valora + 'Hl.', 
            #price=valora,       
            price=delta2 + " %",       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_copa.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Mono:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Roboto Mono', serif", "font-weight": "700", "font-size": "0.8em", "color": "#E31E24" },
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},
                "price": { "background-color": "#E3E5E9","font-family": "'Roboto Regular', serif", "line-height": "1.6", "font-size": "1.1em", "color": bgcolor_positive_or_negative(deltaa)},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlyd"
      )     
      #st.metric(label='Despachos ' + str(anterior), value=valoro + '  Hl.', delta=_format_as_percentage(deltaoa,2) +'%' )
      #st.metric(label='Despachos ' + str(actual), value=valora + '  Hl.', delta=_format_as_percentage(deltaa,2) +'%')
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
      #deltao = valo/vala
      #if deltao < 1:
      #  deltao = (1- deltao) * -1
      deltaa = vala/valo
      deltaa = (deltaa - 1)*100
      #if deltaa < 1:
      #  deltaa = (1- deltaa) * -1

      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['litros'].sum()/100
      deltaoa = valo/valoa
      #st.write(valoa)
      #st.write(valo)
      deltaoa = (deltaoa -1)*100
      #if deltaoa < 1:
      #  deltaoa = (1- deltaoa) * -1     
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      delta2 = str(_format_as_percentage(deltaa,2))
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)

      product_card(
            product_name=delta2 + " %",
            description='Exportaciones '  + mesfin + ' ' + str(actual), 
            price=valora + ' Hl.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_mundo.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Regular:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Regular', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlyeh"
      )              
      #st.metric(label='Exportaciones de Vinos ' + str(anterior), value=valoro + '  Hl.', delta=_format_as_percentage(deltaoa,2) +'%' )
      #st.metric(label='Exportaciones de Vinos ' + str(actual), value=valora + '  Hl.', delta=_format_as_percentage(deltaa,2) +'%')

   with col[2]:
      dv2 = registro_mensual(anterior -2)
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
      deltaa = (deltaa - 1)*100
      #if deltaa < 1:
      #  deltaa = (1- deltaa) * -1
      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['fob'].sum()
      #st.write(valoa)
      #st.write(valo)
      deltaoa = valo/valoa
      deltaoa = (deltaoa -1)*100
      #if deltaoa < 1:
      #  deltaoa = (1- deltaoa) * -1           
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      delta2 = str(_format_as_percentage(deltaa,2))
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      product_card(
            product_name=delta2 + " %",
            description='Exportaciones '  + mesfin + ' ' + str(actual), 
            price=valora + 'Hl.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_mundo.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"background-color": "#17a2b8","font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},
                "price": {"color": "white", "background-color": "#E3E5E9", "padding": "5px 10px", "border-radius": "5px", "text-align": "center", "font-weight": "bold"},
                "product_name": {"color": "white", "background-color": "#17a2b8", "padding": "5px 10px", "border-radius": "5px", "text-align": "center", "font-weight": "bold"},
            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlyep"
      )     
      #st.metric(label='Exportaciones de Vinos ' + str(anterior), value=valoro + '  u$s.', delta=_format_as_percentage(deltaoa,2) +'%' )
      #st.metric(label='Exportaciones de Vinos ' + str(actual), value=valora + '  u$s.', delta=_format_as_percentage(deltaa,2) +'%')


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
      deltaa = (deltaa - 1)*100
      #if deltaa < 1:
      #  deltaa = (1- deltaa) * -1
        

      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      valoa = dvoa['litros'].sum()
      #st.write(valo)
      #st.write(valoa)
      deltaoa = valo/valoa
      #st.write(deltaoa)
      deltaoa = (deltaoa -1)*100
      #if deltaoa < 1:
      #  deltaoa = (deltaoa) * -1        
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      delta2 = str(_format_as_percentage(deltaa,2))
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      product_card(
            product_name=delta2 + " %",
            description='Exportaciones Mosto '  + mesfin + ' ' + str(actual), 
            price=valora + 'Tn.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_mundo.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlyeml"
      )     
      #st.metric(label='Exportaciones de Mostos ' + str(anterior), value=valoro + ' Tn. ', delta=_format_as_percentage(deltaoa,2) +'%' )
      #st.metric(label='Exportaciones de Mostos ' + str(actual), value=valora + ' Tn. ', delta=_format_as_percentage(deltaa,2) +'%')
   
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
      deltaa = (deltaa - 1)*100
      #if deltaa < 1:
      #  deltaa = (1- deltaa) * -1

      dvoa = dv2[dv2['anio'] == anterior-1 ]
      dvoa = dvoa[dvoa['mes']  <= mes]
      #st.write(dvoa)
      valoa = dvoa['fob'].sum()
      #st.write(valo)
      #st.write(valoa)
      deltaoa = valo/valoa
      #st.write(deltaoa)
      deltaoa = (deltaoa -1)*100
      #if deltaoa < 1:
      #  deltaoa = (1- deltaoa) * -1        
      valoro = str(_format_with_thousands_commas(valo)) 
      valora = str(_format_with_thousands_commas(vala)) 
      delta2 = str(_format_as_percentage(deltaa,2))
      mes2 = max(dva['mes1'])
      #st.write('Periodo : 01 Enero/' + mes2)
      product_card(
            product_name=delta2 + " %",
            description='Exportaciones Mosto '  + mesfin + ' ' + str(actual), 
            price=valora + 'u$s.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_mundo.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlyemp"
      )     
      #st.metric(label='Exportaciones de Mostos ' + str(anterior), value=valoro + '  u$s.', delta=_format_as_percentage(deltaoa,2) +'%' )
      #st.metric(label='Exportaciones de Mostos ' + str(actual), value=valora + '  u$s.', delta=_format_as_percentage(deltaa,2) +'%')

   colo = st.columns((4.5, 4.5), gap='medium')

   with colo[0]:

     dva = dfsup[dfsup['anio'] == maxanio ]
     dvo = dfsup[dfsup['anio'] == maxanio-1 ]  
     vala = dva['sup'].sum()
     valo = dvo['sup'].sum()     
     dvoa = dfsup[dfsup['anio'] == maxanio-2 ]
     valoa = dvoa['sup'].sum()
     valoro = str(_format_with_thousands_commas(valo)) 
     valora = str(_format_with_thousands_commas(vala))
     delta2 = str(_format_as_percentage(deltaa,2))
     deltaoa = valo/valoa
     #st.write(deltaoa)
     deltaoa = (deltaoa -1)*100     
     deltaa = vala/valo
     deltaa = (deltaa - 1)*100     
     product_card(
            product_name=delta2 + " %",
            description='Superficie '  + str(maxanio), 
            price=valora + 'Ha.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_superficie.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlysup"
     )       
     
     #st.metric(label='Superficie ' + str(maxanio -1), value= valoro + '', delta=_format_as_percentage(deltaoa,2) +'%' )
     #st.metric(label='Superficie ' + str(maxanio), value= valora + ' ', delta=_format_as_percentage(deltaa,2) +'%')
   with colo[1]:

     dva = dfcos[dfcos['anio'] == maxanio ]
     dvo = dfcos[dfcos['anio'] == maxanio-1 ]  
     vala = dva['peso'].sum()
     valo = dvo['peso'].sum()     
     dvoa = dfcos[dfcos['anio'] == maxanio-2 ]
     valoa = dvoa['peso'].sum()
     valoro = str(_format_with_thousands_commas(valo)) 
     valora = str(_format_with_thousands_commas(vala)) 
     delta2 = str(_format_as_percentage(deltaa,2))
     deltaoa = valo/valoa
     #st.write(deltaoa)
     deltaoa = (deltaoa -1)*100     
     deltaa = vala/valo
     deltaa = (deltaa - 1)*100 
     product_card(
            product_name=delta2 + " %",
            description='Cosecha ' + str(maxanio), 
            price=valora + 'Q.' ,       
            product_image='https://www.observatoriova.com/wp-content/uploads/2023/08/icon_barril.svg', 
            picture_position="left",
            image_aspect_ratio="16/9",
            image_object_fit="contain",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "1.1em", "color": "#5d4037"},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_onlycos"
     )      
     
     #st.metric(label='Cosecha ' + str(maxanio -1), value= valoro + '', delta=_format_as_percentage(deltaoa,2) +'%' )
     #st.metric(label='Cosecha ' + str(maxanio), value= valora + ' ', delta=_format_as_percentage(deltaa,2) +'%')
            
with tab2:
  ind_exportaciones.ind_exportaciones(dvex)

  
with tab3:
  ind_mercado_interno.ind_mercado_interno(dv1)

with tab4:
  ind_superficie.ind_superficie(dfsup,dfcos)
with tab5:
  indica1.indica1(dv1) 
with tab6:
  indica2.indica2(dv1) 
