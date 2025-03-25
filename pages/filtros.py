import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from sqlalchemy import create_engine

# Configuración de conexión a PostgreSQL
DB_USER = "observa"
DB_PASSWORD = "observa"
DB_HOST = "119.8.155.25"
DB_PORT = "5432"
DB_NAME = "observa"

# Crear la conexión con SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Función para cargar datos desde la base de datos
@st.cache_data
def cargar_datos(consulta):
    try:
        with engine.connect() as conn:
            df = pd.read_sql(consulta, con=engine)
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# Cargar datos iniciales para llenar los filtros
QUERY_INICIAL = "SELECT anio, variedad, provincia FROM superficievariedad_m"
df_filtros = cargar_datos(QUERY_INICIAL)

# Si no hay datos, mostrar error y detener la ejecución
if df_filtros.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

# Listas de valores únicos para los filtros
year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
var_list = sorted(df_filtros["variedad"].dropna().unique())
prov_list = sorted(df_filtros["provincia"].dropna().unique())
color_list = ("Tinta", "Blanca", "Rosada", "Sin Dato", "Todas")

# Estado inicial para filtros
if "filtros" not in st.session_state:
    st.session_state.filtros = {
        "anio": "Todos",
        "var": "Todas",
        "prov": "Todas",
        "vcolor": "Todas"
    }

# Interfaz de filtros
with st.popover("Abrir Filtros"):
    st.markdown("Filtros ??")
    anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
    var = st.multiselect("Variedad:", ["Todas"] + var_list, default=["Todas"])
    prov = st.multiselect("Provincia:", ["Todas"] + prov_list, default=["Todas"])
    vcolor = st.multiselect("Color:", color_list, default=["Todas"])

    if st.button("Aplicar filtros", type="primary"):
        st.session_state.filtros = {"anio": anio, "var": var, "prov": prov, "vcolor": vcolor}
        st.rerun()  # Vuelve a ejecutar la app para aplicar los filtros

# Obtener filtros aplicados
filtros = st.session_state.filtros

# Manejo de 1/múltiples valore/s con IN (...)
condiciones = []

# Filtro por color
if "Todas" in filtros["vcolor"]:
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

# Filtro por provincia
if "Todas" not in filtros["prov"]:
    provincias = "', '".join(filtros["prov"])
    condiciones.append(f"provincia IN ('{provincias}')")

# Unir todas las condiciones con AND
where_clause = " AND ".join(condiciones)

QUERY_V1 = f"""
    SELECT anio, SUM(sup) AS sup, COUNT(*) AS cnt  
    FROM superficievariedad_m 
    WHERE {where_clause}
    GROUP BY anio 
    ORDER BY anio
"""

# Dataframe de datos filtrados
dv1 = cargar_datos(QUERY_V1)


# Construcción del mensaje de filtros aplicados
def formatear_filtro(valor):
    """Si el filtro tiene solo un valor y es 'Todos' o 'Todas', lo muestra sin comas."""
    if isinstance(valor, list):
        if len(valor) == 1 and valor[0] in ["Todos", "Todas"]:
            return valor[0]  # Mostrar sin dividir en caracteres
        return ", ".join(map(str, valor))  # Convertir lista a texto
    return str(valor)  # Convertir valores únicos a string
    
# Mostrar los filtros aplicados con estilo tipo "combo box"
st.subheader("Filtros aplicados")

with st.container():
    col1, col2 = st.columns([1, 3])  # Dividir en columnas (etiqueta - valores)
    
    with col1:
        st.markdown("**Año:**")
    with col2:
        st.markdown(f"<div style='border:1px solid gray; padding:4px; border-radius:4px; display:inline-block;'>{formatear_filtro(st.session_state.filtros['anio'])}</div>", unsafe_allow_html=True)
    
    with col1:
        st.markdown("**Variedad:**")
    with col2:
        st.markdown(f"<div style='border:1px solid gray; padding:4px; border-radius:4px; display:inline-block;'>{formatear_filtro(st.session_state.filtros['var'])}</div>", unsafe_allow_html=True)
    
    with col1:
        st.markdown("**Provincia:**")
    with col2:
        st.markdown(f"<div style='border:1px solid gray; padding:4px; border-radius:4px; display:inline-block;'>{formatear_filtro(st.session_state.filtros['prov'])}</div>", unsafe_allow_html=True)
    
    with col1:
        st.markdown("**Color:**")
    with col2:
        st.markdown(f"<div style='border:1px solid gray; padding:4px; border-radius:4px; display:inline-block;'>{formatear_filtro(st.session_state.filtros['vcolor'])}</div>", unsafe_allow_html=True)

# Verificación de datos
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



