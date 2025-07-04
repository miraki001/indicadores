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
from PIL import Image, ImageDraw, ImageFont


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
    #dvo = dvo.groupby(['anio','mes1'], as_index=False)[['litros']].sum()
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
    dvo = dvo.groupby(['anio','mes1'], as_index=False)[['litros']].sum()
    #st.write(dvo)
    col = st.columns((4.5, 4.5), gap='small')
    with col[0]:
      fig1 = go.Figure(go.Indicator(
      mode = "number+delta",
      #gauge = {'shape': "bullet"},
      delta = {'reference': valoa, 'relative': True, 'valueformat': ".2%"},
      value = valo,
      number = {'valueformat': ".0f"},
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Despachos 2024"}))
      fig1.add_trace(go.Scatter(
        x = dvo['mes1'],
        y = dvo['litros']))
      #fig1.add_trace(
      #  go.line(x=dvo.mes1, y=dvo.litros)
      #)    
        
      #fig1.add_line(x = dvo.mes1,  y = dvo.litros)
      #fig.update_layout(paper_bgcolor = "lightgray")
      fig1.show()
      st.plotly_chart(fig1, theme="streamlit", key="desp1")
    with col[1]:
      fig2 = go.Figure(go.Indicator(
      mode = "number+delta",
      #gauge = {'shape': "bullet"},
      delta =  {'reference': valoa, 'relative': True, 'valueformat': ".2%"},
      value = valo,
      number = {'valueformat': ".0f"},
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Despachos 2024"}))
      #fig.add_trace(go.Scatter(
      #  x = dv1['anio'],
      #  y = dv1['litros']))
      #fig.add_trace(
      #  go.add_bar(x=dvoa.mes1, y=dvoa.litros)
      #)    
      fig2.add_bar(x = dvo.mes1,  y = dvo.litros)
      #fig.update_layout(paper_bgcolor = "lightgray")
      fig2.show()
      st.plotly_chart(fig2, theme="streamlit", key="desp2")


      # Carga las imágenes base y máscara
      botella = Image.open("botella.png").convert("RGBA")
      mascara = Image.open("botella_mascara.png").convert("L")

      # Porcentajes de llenado para cada botella
      porcentajes = [0.15, 0.5, 0.85]

      # Opcional: fuente para las leyendas
      try:
        font = ImageFont.truetype("arial.ttf", 24)
      except:
        font = ImageFont.load_default()

      # Dimensiones para el lienzo final
      espaciado = 30
      ancho_total = len(porcentajes) * botella.width + (len(porcentajes) - 1) * espaciado
      alto_total = botella.height + 40  # espacio para la leyenda

      # Crea el lienzo final
      lienzo = Image.new("RGBA", (ancho_total, alto_total), (255, 255, 255, 0))

      for i, porcentaje_lleno in enumerate(porcentajes):
        altura = int(botella.height * porcentaje_lleno)
        color_verde_botella = (0, 100, 0, 128)  # Verde oscuro semitransparente
        relleno = Image.new("RGBA", botella.size, color_verde_botella)

        relleno_cropped = relleno.crop((0, botella.height - altura, botella.width, botella.height))
        mascara_cropped = mascara.crop((0, botella.height - altura, botella.width, botella.height))
    
        area_relleno = Image.new("RGBA", botella.size, (0, 0, 0, 0))
        area_relleno.paste(relleno_cropped, (0, botella.height - altura), mask=mascara_cropped)
        botella_llena = Image.alpha_composite(botella, area_relleno)
    
        # Pega la botella en la posición correspondiente
        x = i * (botella.width + espaciado)
        lienzo.paste(botella_llena, (x, 0), botella_llena)

        # Crea una capa transparente para el texto
        draw = ImageDraw.Draw(lienzo)
        texto = f"{int(porcentaje_lleno*100)}%"
        bbox = draw.textbbox((0, 0), texto, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        texto_capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
        draw_texto = ImageDraw.Draw(texto_capa)
        draw_texto.text((x + (botella.width - w)//2, botella.height + 5), texto, fill="black", font=font)

        # Combina la capa de texto con la imagen principal
        lienzo = Image.alpha_composite(lienzo, texto_capa)

      # Muestra el resultado en Streamlit
      st.image(lienzo, caption="Botellas con diferentes porcentajes")
