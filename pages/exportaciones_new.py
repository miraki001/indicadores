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




conn = st.connection("postgresql", type="sql")
#df = conn.query('select anio,litros,fob from inf_expo_anio ;', ttl="0")
#st.write(df)

@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# Cargar datos iniciales para llenar los filtros
QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto  from exportaciones2_m;"
df_filtros = cargar_datos(QUERY_INICIAL)

if df_filtros.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

# Listas de valores únicos para los filtros
year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
var_list = sorted(df_filtros["variedad"].dropna().unique())
envase_list = sorted(df_filtros["tipo_envase"].dropna().unique())
color_list = sorted(df_filtros["color"].dropna().unique())
producto_list = sorted(df_filtros["producto"].dropna().unique())
if "filtros" not in st.session_state:
    st.session_state.filtros = {
        "anio": "Todos",
        "var": "Todas",
        "envase": "Todos",
        "vcolor": "Todos",
        "producto": "Todos"
    }

# Interfaz de filtros
with st.popover("Abrir Filtros"):
    st.markdown("Filtros ??")
    anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
    var = st.multiselect("Variedad:", ["Todas"] + var_list, default=["Todas"])
    envase = st.multiselect("Envases:", ["Todos"] + envase_list, default=["Todos"])
    vcolor = st.multiselect("Color:", ["Todos"] +  color_list, default=["Todos"])
    producto = st.multiselect("Producto:",   ["Todos"] +  producto_list, default=["Todos"])

    if st.button("Aplicar filtros", type="primary"):
        st.session_state.filtros = {"anio": anio, "var": var, "envase": envase, "vcolor": vcolor,"producto": producto}
        st.rerun()  # Vuelve a ejecutar la app para aplicar los filtros

# Obtener filtros aplicados
filtros = st.session_state.filtros
condiciones = []

# Filtro por color
if "Todos" in filtros["vcolor"]:
    condiciones.append("1=1")  # No se aplica filtro
else:
    colores = "', '".join(filtros["vcolor"])  # Convierte lista a formato SQL
    condiciones.append(f"color IN ('{colores}')")

# Filtro por año
if "Todos" not in filtros["anio"]:
    años = ", ".join(map(str, filtros["anio"]))
    condiciones.append(f"anio IN ({años})")

# Filtro por variedad
if "Todas" not in filtros["var"]:
    variedades = "', '".join(filtros["var"])
    condiciones.append(f"variedad IN ('{variedades}')")

# Filtro por envase
if "Todos" not in filtros["envase"]:
    envase = "', '".join(filtros["prov"])
    condiciones.append(f"provincia IN ('{provincias}')")

if "Todos" not in filtros["producto"]:
    producto = "', '".join(filtros["producto"])
    condiciones.append(f"producto IN ('{producto}')")


# Unir todas las condiciones con AND
where_clause = " AND ".join(condiciones)

QUERY_V1 = f"""
    SELECT anio, SUM(cntlitros) AS litros, sum(valorfobsolo) AS fob
    FROM exportaciones2_m 
    WHERE {where_clause}
    GROUP BY anio 
    ORDER BY anio
"""

# Dataframe de datos filtrados
dv1 = cargar_datos(QUERY_V1)
if dv1.empty:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
else:
    # Tabla
    st.subheader("Cantidad de Viñedos")
    st.dataframe(dv1)

    # Convertir 'anio' a string para el gráfico
    dv1["anio"] = dv1["anio"].astype(str)

    # Crear gráfico de líneas y barras
    option = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "legend": {},
        "xAxis": {"type": "category", "data": dv1["anio"].tolist()},
        "yAxis": {"type": "value"},
        "series": [
            {"data": dv1["sup"].tolist(), "type": "line", "name": "Hectáreas"},
            {"data": dv1["cnt"].tolist(), "type": "bar", "name": "Cantidad de Viñedos"},
        ],
    }

    st_echarts(options=option, height="400px")
