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
from datetime import datetime as dt
from exportaciones import exporta_evo
from exportaciones import exporta_pais

def bgcolor_positive_or_negative(value):
    bgcolor = "#EC654A" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

#st.set_page_config(initial_sidebar_state="collapsed",
#                  layout="wide",menu_items=None)


st.markdown(
    """
        <style>
                .stAppHeader {
                    background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
                    background-image: url(http://placekitten.com/200/200);
                    background-position: 80px 80px;
                    visibility: visible;  /* Ensure the header is visible */
                }
               button[data-baseweb="tab"] {
                   font-size: 24px;
                   margin: 0;
                   width: 100%;
               }
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 2rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#st.set_page_config(layout="wide")


tab1, tab2, tab3,tab4,tab5,tab6,tab7 = st.tabs(["Evolución", "Destinos", "Variedades","Envase","Mosto Evolución","Mosto Destinos", "Mosto Productos"])

#tab1, tab2, tab3,tab4 = st.tabs(["Evolución", "Totales", "Filtros","Por Provincias"])
#tabs = st.tabs([s.center(whitespace,"-") for s in listTabs])

with tab1:
    exporta_evo.exporta_evolucion()
    
with tab2:
    exporta_pais.exporta_destino()    
    
