
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# Conectar a PostgreSQL
@st.cache_data
def get_data():
    conn = psycopg2.connect(
        dbname='observa', user='postgres', password='postgres', host='172.16.1.76', port='5433'
    )
    query = """
        SELECT anio, mes, pais, valorfobsolo, cantlitros 
        FROM public.exportaciones_m 
        order by pais,anio,mes
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Obtener datos de la BD
df = get_data()

# Convertir 'mes' a números para facilitar el ordenamiento
def convertir_mes(mes):
    meses = {'01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8,
             '09': 9, '10': 10, '11': 11, '12': 12}
    return meses.get(mes.lower(), 0)

# Convertir mes a int
df['mes_num'] = df['mes'].apply(convertir_mes)
df['anio'] = df['anio'].astype(str)

# Ordenar años unicos del query 
valores_anio_ordenados = sorted(df['anio'].unique(), reverse=True)

# Usar container para el menú superior de filtros
with st.container(border=True):
    col1, col2, col3 = st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
    with col1:
        with st.popover("Año"):
            st.caption("Selecciona uno o más años de la lista")
            año = st.multiselect("Año", valores_anio_ordenados, default=[],label_visibility="collapsed",help="Selecciona uno o más años")
            año = [str(a) for a in año]  # Asegura que la selección sea string también
            
    # Columna 2: Filtro para Países
    with col2:
        with st.popover("País"):
            st.caption("Selecciona uno o más países de la lista")
            país = st.multiselect("Países", df['pais'].unique(), default=[],label_visibility="collapsed")
    
    # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
    with col3:
        st.write("")

# Filtrar datos progresivamente
df_filtered = df.copy()

if año:
    df_filtered = df_filtered[df_filtered['anio'].isin(año)]
    df_filtered["anio"] = df_filtered["anio"].astype(str)

if país:
    df_filtered = df_filtered[df_filtered['pais'].isin(país)]

st.write("Tabla de Datos: ", df_filtered)
         
# Determinar título dinámico
if año:
    titulo = f"Ventas por País ({', '.join(año)})"
else:
    titulo = f"Ventas por País (Todos los años)"
    
# Sumarizar por año
df_anual = df_filtered.groupby('anio', as_index=False)[['valorfobsolo', 'cantlitros']].sum()

# Sumarizar por año y mes para la comparación interanual
df_interanual = df_filtered.groupby(['anio', 'mes_num'], as_index=False).sum()

# Selección del tipo de gráfico
grafico_tipo = st.radio("Seleccione el tipo de gráfico", ('Evolución Anual', 'Comparación Interanual'))

if grafico_tipo == 'Evolución Anual':
    # Mostrar tabla con datos filtrados
    fig = px.line(df_anual, x='anio', y=['valorfobsolo', 'cantlitros'],
                  labels={'value': 'Valor', 'variable': 'Métrica'},
                  title='Evolución Anual de Exportaciones')

if grafico_tipo == 'Comparación Interanual':
    # Selección de variable para el eje Y
    variable_y = st.radio("Seleccione la variable a visualizar", ('cantlitros', 'valorfobsolo'))

    fig = px.line(df_interanual, x='mes_num', y=variable_y, color='anio',
                  labels={'value': 'Valor', 'variable': 'Métrica', 'mes_num': 'Mes'},
                  title=f'Comparación Interanual de {variable_y.capitalize()}')

# Para evitar que Ploty interpole valores
fig.update_xaxes(type='category')

st.plotly_chart(fig)
