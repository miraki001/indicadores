import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import locale
from script.exportaciones import mosto_registro_mensual
from streamlit_product_card import product_card 
from despachos import desp_consumo


def handle_card_click(card_name):
    st.session_state.click_message = f"'{card_name}' was clicked!"
    st.toast(f"Clicked: {card_name}")
    #desp_consumo.despachos_consumo() 

def bgcolor_positive_or_negative(value):
    bgcolor = "coral" if value < 0 else "green"
    #st.write(bgcolor)
    #return f"color: {bgcolor};"
    return bgcolor

def _format_with_thousands_commas(val): 
  val = round(val,0)
  return f'{val:.12n}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}f}' 


def indica1(dv1):
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
      product_card(
            product_name=delta1 + "%",
            description='Despachos 2024', 
            price=valoro,       
            product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
            picture_position="left",
            image_aspect_ratio="3/2",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={

                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaoa)},

            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_only"
      )
    with col[1]:
      product_card(
            product_name=delta2 + "%",
            description='Despachos 2025', 
            price=valora,       
            product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
            picture_position="left",
            image_aspect_ratio="3/2",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Slab:wght@400&display=swap",
            styles={
                "card": {"background-color": "#e5a294",}, 
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "#5d4037"},
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "lightgreen"},
                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Slab', serif", "line-height": "1.6", "font-size": "0.9em", "color": "#5d4037"},
                "price": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.9em", "color": "red"},
                "button": {"font-family": "'Roboto Slab', serif", "font-weight": "400", "font-size": "0.8em", "background-color": "#53372E",}
            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_only111"
      )

    col1 = st.columns((4.5, 4.5), gap='small')
    with col1[0]:
      product_card(
            product_name=delta2 + "%",
            description='Despachos 2025', 
            price=valora,       
            product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
            picture_position="left",
            image_aspect_ratio="3/2",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Mono:wght@400&display=swap",
            styles={
                "card": {"background-color": "#e5a294",}, 
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "#5d4037"},
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "lightgreen"},
                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "0.9em", "color": "#5d4037"},
                "price": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.9em", "color": "red"},
                "button": {"font-family": "'Roboto Slab', serif", "font-weight": "400", "font-size": "0.8em", "background-color": "#53372E",}
            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_only133"
      )
    with col1[1]:
      product_card(
            product_name=delta2 + "%",
            description='Despachos 2025', 
            price=valora,       
            product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
            picture_position="left",
            image_aspect_ratio="3/2",
            font_url="https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@400;700&family=Roboto+Mono:wght@400&display=swap",
            styles={
                "card": {"background-color": "#e5a294",}, 
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "#5d4037"},
                #"title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": "lightgreen"},
                "title": {"font-family": "'Old Standard TT', serif", "font-weight": "700", "font-size": "1.8em", "color": bgcolor_positive_or_negative(deltaa)},
                "text": {"font-family": "'Roboto Mono', serif", "line-height": "1.6", "font-size": "0.9em", "color": "#5d4037"},
                "price": {"font-family": "'Roboto Mono', serif", "font-weight": "700", "font-size": "1.9em", "color": "red"},
                "button": {"font-family": "'Roboto Slab', serif", "font-weight": "400", "font-size": "0.8em", "background-color": "#53372E",}
            },
            button_text=None,   
            on_button_click=lambda: handle_card_click("Clickable Card Area"),
            key="core_name_only13443"
      )
