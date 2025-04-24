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
from sqlalchemy import create_engine, text
import plotly.express as px  # Para crear gráficos interactivos. Instalar con: pip install plotly

st.set_page_config(layout="wide")

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

streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;}
   </style>
    """
st.markdown(streamlit_style, unsafe_allow_html=True)

# Datos de conexión (modifica según tu entorno)
DB_USER = "observa"
DB_PASSWORD = "observa"
DB_HOST = "119.8.155.25"
DB_PORT = "5432"
DB_NAME = "observa"

# Crear conexión
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Función para cargar datos desde SQL
@st.cache_data
def cargar_datos(query):
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(query), conn)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# Cargar datos iniciales para llenar los filtros
QUERY_INICIAL = f"""
    SELECT anio,sup,cnt,provincia,departamento,variedad,color,tipouva FROM superficievariedad_m
"""
df = cargar_datos(QUERY_INICIAL)

if df.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

# Listas de valores únicos para los filtros
year_list = sorted(df["anio"].dropna().unique(), reverse=True)
var_list = sorted(df["variedad"].dropna().unique())
prov_list = sorted(df["provincia"].dropna().unique())
color_list = sorted(df["color"].dropna().unique())
tipouva_list = sorted(df["tipouva"].dropna().unique())

st.html(
    '''
        <style>
            div[data-testid="stPopover"]>div>button {
                min-height: 22.4px;
                height: 22.4px;
                background-color: #A9F8FA !important;
                color: black;
            }
        </style>
    '''
)

with st.container(border=True):
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
    with col1:
        with st.popover("Año"):
            st.caption("Selecciona uno o más años")
            #año = st.multiselect("Año1",  year_list, default=[year_list[0]],label_visibility="collapsed",help="Selecciona uno o más años")
            year_list = ["Todos"] + year_list
            anio = st.multiselect("Año1",  year_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más años")
            anio = [str(a) for a in anio]  # Asegura que la selección sea string también

    # Columna 2: Filtro para Provincia
    with col2:
        with st.popover("Provincia"):
            st.caption("Selecciona uno o más Provincias")
            provincia = st.multiselect("Provincia2",  ["Todas"] + prov_list, default=["Todas"],label_visibility="collapsed", help="Selecciona uno o más Provincias")

    # Columna 3: Filtro por variedad
    with col3:
        with st.popover("Variedad"):
            st.caption("Selecciona uno o más Variedades")
            variedad = st.multiselect("Variedad3",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed", help="Selecciona uno o más Variedades")

    # Columna 4: Filtro por color
    with col4:
        with st.popover("Color"):
            st.caption("Selecciona uno o más colores")
            color = st.multiselect("Color4",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed", help="Selecciona uno o más colores")

    # Columna 5: Filtro por tipo
    with col5:
        with st.popover("Tipo Uva"):
            st.caption("Selecciona uno o más tipos")
            tipouva = st.multiselect("Tipo uva5",  ["Todos"] + tipouva_list, default=["Todos"],label_visibility="collapsed", help="Selecciona uno o más tipos")

# Manejo de 1/múltiples valore/s con IN (...)
condiciones = []

if anio and "Todos" not in anio:
    años_sql = ", ".join([str(a) for a in anio])  # sin comillas porque son enteros
    condiciones.append(f"anio IN ({años_sql})")

if provincia and "Todas" not in provincia:
    provincias_sql = ", ".join([f"'{p}'" for p in provincia])
    condiciones.append(f"provincia IN ({provincias_sql})")

if variedad and "Todas" not in variedad:
    variedades_sql = ", ".join([f"'{v}'" for v in variedad])
    condiciones.append(f"variedad IN ({variedades_sql})")

if color and "Todos" not in color:
    colores_sql = ", ".join([f"'{c}'" for c in color])
    condiciones.append(f"color IN ({colores_sql})")

if tipouva and "Todos" not in tipouva:
    tipos_sql = ", ".join([f"'{t}'" for t in tipouva])
    condiciones.append(f"tipouva IN ({tipos_sql})")

# Construcción del query
where_clause = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

QUERY_V1 = f"""
    SELECT anio,sup,cnt,provincia,departamento,variedad,color,tipouva FROM superficievariedad_m
    {where_clause}
"""

# Dataframe de datos filtrados
df_filtered = cargar_datos(QUERY_V1)
if df_filtered.empty:
    st.error("No se encontraron datos con los filtros seleccionados en la base de datos.")
    st.stop()

# Suma de superficie por año
df_grouped_sup = df_filtered.groupby("anio")["sup"].sum().reset_index()
df_grouped_sup["anio"] = df_grouped_sup["anio"].astype(str)

# Calcular el porcentaje de diferencia respecto al año anterior
df_grouped_sup['diff_percentage'] = df_grouped_sup['sup'].pct_change() * 100
df_grouped_sup['diff_percentage'] = df_grouped_sup['diff_percentage'].fillna(0)  # Rellenar el primer valor con 0

df_grouped_vin = df_filtered.groupby("anio")["cnt"].sum().reset_index()
df_grouped_vin["anio"] = df_grouped_vin["anio"].astype(str)


# Grafico de Barras
figxbar = px.bar(df_grouped_sup, x="anio", y="sup", title="Total de hectáreas", text_auto=True)
figxbar.update_layout(
    xaxis_type='category',
    margin=dict(t=50, b=150, l=30, r=30)  # Ajusta el margen inferior (b) para crear más espacio
)

# Grafico de Lineas por Hectareas
figxline_sup = px.line(
    df_grouped_sup,
    x="anio",
    y="sup",
    title="Total de hectáreas",
    markers=True,
    line_shape="linear",
    line_dash_sequence=["solid"],
)

# Grafico de Lineas por Hectareas
figxline_vin = px.line(
    df_grouped_vin,
    x="anio",
    y="cnt",
    title="Cantidad de Viñedos",
    markers=True,
    line_shape="linear",
    line_dash_sequence=["solid"],
)

# Cambiar el color de la línea a rojo
figxline_sup.update_traces(line_color="red")
figxline_vin.update_traces(line_color="red")



# Personalizar fondo y ejes
figxline_sup.update_layout(
    xaxis_type='category',
    title=dict(
        text="Total de hectáreas"
    ),
    plot_bgcolor="#eee",  # Fondo del gráfico (área interior)
    #paper_bgcolor="#333",  # Fondo total, incluyendo el título
    xaxis=dict(
        showticklabels=True,  # Oculta las etiquetas originales
        showline=True,
        linecolor="black",
        linewidth=1,
        showgrid=True,
        gridcolor="white",
        tickfont=dict(color="black")
    ),
    yaxis=dict(
        showline=False,
        linecolor="white",
        tickfont=dict(color="black")
    ),
    font=dict(color="black"),
    margin=dict(t=80, b=150, l=30, r=30)  # Margen superior ajustado
    
)

# Personalizar fondo y ejes
figxline_vin.update_layout(
    xaxis_type='category',
    title=dict(
        text="Cantidad de Viñedos"
    ),
    plot_bgcolor="#eee",  # Fondo del gráfico (área interior)
    #paper_bgcolor="#333",  # Fondo total, incluyendo el título
    xaxis=dict(
        showticklabels=True,  # Oculta las etiquetas originales
        showline=True,
        linecolor="black",
        linewidth=1,
        showgrid=True,
        gridcolor="white",
        tickfont=dict(color="black")
    ),
    yaxis=dict(
        showline=False,
        linecolor="white",
        tickfont=dict(color="black")
    ),
    font=dict(color="black"),
    margin=dict(t=80, b=150, l=30, r=30)  # Margen superior ajustado
)


# Dividir la página en dos columnas
c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        
        # Mostrar los años seleccionados como texto
        if isinstance(anio, list):
            años_str = ", ".join(map(str, anio))
        else:
            años_str = str(anio)
        
        filtros = [
            ("Año(s) seleccionado(s):", años_str),
            ("Provincia:", ", ".join(map(str, provincia))),
            ("Variedad:", ", ".join(map(str, variedad))),
            ("Color:", ", ".join(map(str, color))),
            ("Tipo de uva:", ", ".join(map(str, tipouva))),
        ]

        for i, (label, valor) in enumerate(filtros):
            y_pos = -0.32 - i * 0.07  # Va bajando cada línea

            # Texto del filtro
            figxbar.add_annotation(
                text=label,
                xref="paper", yref="paper",
                x=0.01, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="white"),
                bgcolor="#333",
                borderpad=4,
                align="left",
                width=200,  # Valor fijo para el ancho del fondo de la etiqueta
                bordercolor="white",  # Borde blanco para la etiqueta
                borderwidth=1  # Ancho del borde (puedes ajustarlo si es necesario)
            )

            # Valor del filtro
            figxbar.add_annotation(
                text=valor,
                xref="paper", yref="paper",
                x=0.20, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="black"),
                bgcolor="#ddd",
                borderpad=4,
                align="left",
                width=300,  # Valor fijo para el ancho del fondo de la etiqueta,
                bordercolor="white",  # Borde blanco para la etiqueta
                borderwidth=1  # Ancho del borde (puedes ajustarlo si es necesario)
            )

        st.plotly_chart(figxbar)

with c2:
    with st.container(border=True):

        if isinstance(anio, list):
            años_str = ", ".join(map(str, anio))
        else:
            años_str = str(anio)

        filtros = [
            ("Año(s) seleccionado(s):", años_str),
            ("Provincia:", ", ".join(map(str, provincia))),
            ("Variedad:", ", ".join(map(str, variedad))),
            ("Color:", ", ".join(map(str, color))),
            ("Tipo de uva:", ", ".join(map(str, tipouva))),
        ]

        for i, (label, valor) in enumerate(filtros):
            y_pos = -0.35 - i * 0.07

            figxline_sup.add_annotation(
                text=label,
                xref="paper", yref="paper",
                x=0.01, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="white"),
                bgcolor="#333",
                borderpad=4,
                align="left",
                width=200,
                bordercolor="white",
                borderwidth=1
            )

            figxline_sup.add_annotation(
                text=valor,
                xref="paper", yref="paper",
                x=0.20, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="black"),
                bgcolor="#ddd",
                borderpad=4,
                align="left",
                width=300,
                bordercolor="white",
                borderwidth=1
            )
        
        st.plotly_chart(figxline_sup, use_container_width=True)
    
# Dividir la página en dos columnas
c1, c2 = st.columns(2)

with c1:
    st.info("Aquí se mostrará otro gráfico, por ejemplo: superficie por provincia.")
    #with st.container(border=True):
    #    st.plotly_chart(figxProducto)

with c2:
    with st.container(border=True):
        if isinstance(anio, list):
            años_str = ", ".join(map(str, anio))
        else:
            años_str = str(anio)

        filtros = [
            ("Año(s) seleccionado(s):", años_str),
            ("Provincia:", ", ".join(map(str, provincia))),
            ("Variedad:", ", ".join(map(str, variedad))),
            ("Color:", ", ".join(map(str, color))),
            ("Tipo de uva:", ", ".join(map(str, tipouva))),
        ]

        for i, (label, valor) in enumerate(filtros):
            y_pos = -0.35 - i * 0.07

            figxline_vin.add_annotation(
                text=label,
                xref="paper", yref="paper",
                x=0.01, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="white"),
                bgcolor="#333",
                borderpad=4,
                align="left",
                width=200,
                bordercolor="white",
                borderwidth=1
            )

            figxline_vin.add_annotation(
                text=valor,
                xref="paper", yref="paper",
                x=0.20, y=y_pos,
                showarrow=False,
                font=dict(size=14, color="black"),
                bgcolor="#ddd",
                borderpad=4,
                align="left",
                width=300,
                bordercolor="white",
                borderwidth=1
            )

        st.plotly_chart(figxline_vin)






