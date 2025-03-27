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

def bgcolor_positive_or_negative(value):
    bgcolor = "#EC654A" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

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
QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto  from exportaciones2_m  where producto not in ('Mosto','Alcohol');"
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

st.html(
    '''
        <style>
            div[data-testid="stPopover"]>div>button {
                min-height: 32.4px;
                height: 32.4px;
                background-color: #A9F8FA !important;
                color: black;
            }
        </style>
    '''
)


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
    condiciones.append(f"variedad1 IN ('{variedades}')")

# Filtro por envase
if "Todos" not in filtros["envase"]:
    envase = "', '".join(filtros["envase"])
    condiciones.append(f"tipo_envase IN ('{envase}')")

if "Todos" not in filtros["producto"]:
    producto = "', '".join(filtros["producto"])
    condiciones.append(f"producto IN ('{producto}')")


# Unir todas las condiciones con AND
where_clause = " AND ".join(condiciones)

QUERY_V1 = f"""
    SELECT anio, SUM(cantlitros) AS litros, sum(valorfobsolo) AS fob, sum(valorfobsolo) / sum(cantlitros) AS ppl
    FROM exportaciones2_m 
    WHERE {where_clause}
    and producto not in ('Mosto','Alcohol')
    GROUP BY anio 
    ORDER BY anio 
"""

# Dataframe de datos filtrados
dv1 = cargar_datos(QUERY_V1)
if dv1.empty:
    st.warning("No se encontraron resultados con los filtros seleccionados.")
else:
    # Tabla
    st.subheader("Exportaciones")
    total = []
    tot1 = []
    tot2 = []
    total.append(0)
    tot1.append(0)
    tot2.append(0)
    for index in range(len(dv1)):
      if index > 0:
        total.append((  (dv1['litros'].loc[index] / dv1['litros'].loc[index -1]) -1 ) *100 )
        tot1.append((  (dv1['fob'].loc[index] / dv1['fob'].loc[index -1]) -1 ) *100 )
        tot2.append((  (dv1['ppl'].loc[index] / dv1['ppl'].loc[index -1]) -1 ) *100     )
    #st.write(total)
    dv1 = dv1.rename(columns={'litros': "Litros", 'fob': "Fob",'anio': "Año","ppl": 'ppl'})
    dv1['Litros Var %'] = total
    dv1['Fob Var. %'] = tot1
    dv1['Prec x Litro Var. %'] = tot2

    dv1 = dv1.sort_index(axis = 1)

    styled_df = dv1.style.applymap(bgcolor_positive_or_negative, subset=['Litros Var %','Fob Var. %','Prec x Litro Var. %']).format(
        {"Litros": lambda x : '{:,.0f}'.format(x), 
        "Fob": lambda x : '{:,.0f}'.format(x),
        "ppl": lambda x : '{:,.2f}'.format(x),
        "Litros Var %": lambda x : '{:,.2f} %'.format(x),
        "Fob Var. %": lambda x : '{:,.2f} %'.format(x),
        "Prec x Litro Var. %": lambda x : '{:,.2f} %'.format(x),
                                        }
        ,
        thousands='.',
        decimal=',',
    )


    #st.write(df2)
    if st.checkbox('Ver datos en forma de tabla'):
        st.dataframe(styled_df,
          column_config={
            'Año': st.column_config.Column('Año'),
            'Litros': st.column_config.Column('Litros'),
            'Fob': st.column_config.Column('Fob'),
            'Litros Var %': st.column_config.Column('Litros Var %'),
            'Fob Var. %': st.column_config.Column('Fob Var. %'),
            'ppl': st.column_config.Column('ppl'),
            'Prec x Litro Var. %': st.column_config.Column('Prec x Litro Var. %'),
        
            },
            width = 600,   
            height = 800,
            hide_index=True)

  
    #st.dataframe(dv1)

    # Convertir 'anio' a string para el gráfico
    dv1["Año"] = dv1["Año"].astype(str)

    # Crear gráfico de líneas y barras
    option = {
      "color": [
            '#332D75',
            '#1E8DB6',
            '#604994',
            '#dd6b66',
        ],
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "legend": {},
        "xAxis": {"type": "category", "data": dv1["Año"].tolist()},
        "yAxis": [
            {"type": "value" ,"name" : "Litros" ,
             "axisLabel": {
                "formatter": '{value} '
                  }
            } ,
            {"type": "value" , "name" : "",
             "position" : 'left',
             "alignTicks": 'true',
             "offset": 80,
             "axisLine": {
                "show": 'true',
              },             
             "axisLabel": {
                "formatter": '{value}  '
                  }
            },
            {"type": "value" , "name" : "ppl",
             "position" : 'rigth',
             "alignTicks": 'true',
             "offset": 80,
             "axisLine": {
                "show": 'true',
                "lineStyle": {                                          
                    "color" : '#07ECFA',
                },
              },             
             "axisLabel": {
                "formatter": '{value} $ '
                  }
            },            
        ],
        "series": [
            {"data": dv1["Litros"].tolist(),"position" : 'rigth', "type": "line", "name": "Litros", "yAxisIndex": 1, },
            {"data": dv1["Fob"].tolist(), "type": "bar", "name": "Fob", "yAxisIndex": 1, },
            {"data": dv1["ppl"].tolist(), "type": "line", "name": "ppl", "yAxisIndex": 2, },
        ],
    }

    st_echarts(options=option, height="400px")
