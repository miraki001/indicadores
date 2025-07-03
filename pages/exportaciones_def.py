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
from exportaciones import exporta_variedad
from exportaciones import exporta_color
from exportaciones import mosto_evo
from exportaciones import mosto_pais
from exportaciones import mosto_producto
from exportaciones import espumantes
from exportaciones import expo_misc

def bgcolor_positive_or_negative(value):
    bgcolor = "#EC654A" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

st.set_page_config(initial_sidebar_state="collapsed",
                  layout="wide",menu_items=None)





#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#st.set_page_config(layout="wide")


tab1, tab2, tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs(["Evolución", "Destinos", "Variedades","Color/Envase","Mosto ","Espumantes", "Mercado Mundial","M"])

#tab1, tab2, tab3,tab4 = st.tabs(["Evolución", "Totales", "Filtros","Por Provincias"])
#tabs = st.tabs([s.center(whitespace,"-") for s in listTabs])




#st.session_state['vEstado'] = '0'

with tab1:
    #st.session_state['vEstado'] = '0'
    exporta_evo.exporta_evolucion()
    
with tab2:
    #st.session_state['vEstado'] = '0'
    exporta_pais.exporta_destino()  
    
with tab3:
    #st.session_state['vEstado'] = '0'
    exporta_variedad.exporta_variedades()    
with tab4:
    #st.session_state['vEstado'] = '0'
    exporta_color.exporta_color()    
with tab5:
    #st.session_state['vEstado'] = '0'
    mosto_evo.exporta_mosto_evo()    
    mosto_pais.exporta_mosto_destino()    
    mosto_producto.exporta_mosto_producto()    
    
with tab6:
    #st.session_state['vEstado'] = '0'
    espumantes.espumantes()    
with tab7:
    #st.session_state['vEstado'] = '0'
    st.write('Proximanente')   
with tab8:
    #st.session_state['vEstado'] = '0'
    expo_misc.expo_misc()
    
