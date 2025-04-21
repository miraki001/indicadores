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


conn = st.connection("postgresql", type="sql")

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

def _format_with_thousands_commas(val): 
  return f'{val:.,0f}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}%}' 

@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()


QUERY_V0 = f"""
        SELECT distinct anio,variedad1 as variedad,provincia,departamento,producto
        FROM despachos_m 
        where producto not in ('Mosto','Alcohol')
        

"""

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


df_filtros = cargar_datos(QUERY_V0)

if df_filtros.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

QUERY_V1 = f"""
        SELECT anio, cantidadlitros AS litros,variedad1 as variedad,provincia,departamento,producto
        FROM despachos_m 
        WHERE producto not in ('Mosto','Alcohol')
"""

    # Listas de valores únicos para los filtros
year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
var_list = sorted(df_filtros["variedad"].dropna().unique())
prov_list = sorted(df_filtros["provincia"].dropna().unique())
depto_list = sorted(df_filtros["departamento"].dropna().unique())
producto_list = sorted(df_filtros["producto"].dropna().unique())
#pais_list = sorted(df_filtros["pais"].dropna().unique())
if "filtroseee" not in st.session_state:
        st.session_state.filtrosee = {
            "anio": "Todos",
            "var": "Todas",
            "prov": "Todas",
            "depto": "Todos",
            "producto": "Todos",
            "Pais": "Todos",
        }



dv1 = cargar_datos(QUERY_V1)
df_filtered = dv1.copy() 


with st.container(border=True):
    col1, col2, col3,col4= st.columns([1, 1, 1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
    with col1:
        with st.popover("Variedad"):
            st.caption("Selecciona uno o más Variedades de la lista")
            variedad = st.multiselect("Variedad343",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
    with col2:
        with st.popover("Provincia"):
            st.caption("Selecciona uno o más Provincias de la lista")
            provincia = st.multiselect("Proncias33",  ["Todas"] + prov_list, default=["Todas"],label_visibility="collapsed")
    with col3:
        with st.popover("Departamento"):
            st.caption("Selecciona uno o más Departamentos de la lista")
            departamento = st.multiselect("dpto",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")                

    with col4:
        with st.popover("Producto"):
            st.caption("Selecciona uno o más Productos de la lista")
            producto = st.multiselect("Coloreo",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed")                


Filtro = 'Filtro = Año = '
Filtro = Filtro +  ' Todos '
  
if variedad:
    if variedad[0] != 'Todas':
        df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
        #st.write(variedad)
    Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
  
if departamento:
    if departamento[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['departamento'].isin(departamento)]
    Filtro = Filtro + ' Departamento = ' +  str(departamento) + ' '
          
if provincia:        
    if provincia[0] != 'Todas':
        df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]          
    Filtro = Filtro + ' Provincia = ' +  str(provincia) + ' '

if producto:
    if producto[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['producto'].isin(producto)]
    Filtro = Filtro + ' Producto = ' +  str(producto) + ' '


tab1, tab2, tab3,tab4,tab5,tab6 = st.tabs(["Evolución", "Por Provincias", "Por Color/Tipo","Por Envase","Por Variedades","Consumo Interno"])

with tab1:

  df_filtered = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()
    
  #st.write(df_filtered)
 
  st.subheader('Evolución de los despachos por año')

  if st.checkbox('Ver datos en forma de tabla'):
      st.write(df_filtered)

  option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df_filtered['anio'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df_filtered['litros'].to_list(), "type": "line", "name": 'Litros'},
               ]
  }
  st_echarts(
    options=option, height="400px" ,
  )

    
