
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
from cosecha import cosecha_evo

st.set_page_config(initial_sidebar_state="collapsed",
                  layout="wide",menu_items=None)

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

conn = st.connection("postgresql", type="sql")
def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"


@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()


QUERY_V0 = f"""
        SELECT distinct anio,variedad,provincia,departamento
        FROM superficievariedad_m 
        

"""



tab1, tab2, tab3,tab4,tab5,tab6,tab7 = st.tabs(["Superficie Evolución","Superficie por Provincia","Superficie por Variedad", "Cosecha Evolución","Cosecha por Provincias","Cosecha por Variedad",  "Rendimientos"])

with tab1:


    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    prov_list = sorted(df_filtros["provincia"].dropna().unique())
    depto_list = sorted(df_filtros["departamento"].dropna().unique())
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "anio": "Todos",
            "var": "Todas",
            "provincia": "Todas",
            "departamento": "Todos"
        }

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
    QUERY_V1 = f"""
        SELECT anio,sup,cnt ,variedad,provincia,departamento  from superficievariedad_m

    """
    QUERY_V2 = f"""
        SELECT año as anio,sup,cant as cnt ,provincia,departamento  from superficie_m
      

    """


    with st.container(border=True):
        col1, col2, col3= st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        with col2:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincias de la lista")
                provincia = st.multiselect("Provincia",  ["Todas"] + prov_list, default=["Todas"],label_visibility="collapsed")
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                departamento = st.multiselect("Departamento",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")                
    vercnt = 0
    if variedad:
      if variedad[0] != 'Todas':
        dv1 = cargar_datos(QUERY_V1)
        vercnt = 0
      else:
        dv1 = cargar_datos(QUERY_V2)
        vercnt = 1
      dv1['anio'] = dv1['anio'].astype(str)
    else:
      dv1 = cargar_datos(QUERY_V2)  
    df_filtered = dv1.copy()



    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            #st.write(variedad)
    if departamento:
        if departamento[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['departamento'].isin(departamento)]
    if provincia:
        
        if provincia[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]          

    #st.write(provincia)
    #st.write(departamento)
    #st.write(dv1)
  
    st.header("Cantidad de Viñedos")
    #sql = "select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = '" + vcolor + "' or  '" +vcolor + "'= 'Todas' ) group by anio order by anio"
    #st.write(sql)
    #dv1 = conn.query(sql)
    #dv1 = conn.query('select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m where (color = %1 or %1= '-1' group by anio order by anio ;', ttl="0")
    df_anual = df_filtered.groupby(['anio'], as_index=False)[['sup', 'cnt']].sum()
    #st.write(df_anual)

    total = []
    tot1 = []
    total.append(0)
    tot1.append(0)
    for index in range(len(df_anual)):
      if index > 0:
        total.append((  (df_anual['sup'].loc[index] / df_anual['sup'].loc[index -1]) -1 ) *100 )
        tot1.append((  (df_anual['cnt'].loc[index] / df_anual['cnt'].loc[index -1]) -1 ) *100 )
    #st.write(total)
    df_anual = df_anual.rename(columns={'sup': "Superficie", 'cnt': "Viñedos Cnt.",'anio': "Año"})
    df_anual['Superficie Var %'] = total
    df_anual['Viñedos Var. %'] = tot1

    df_anual = df_anual.sort_index(axis = 1)

    styled_df = df_anual.style.applymap(bgcolor_positive_or_negative, subset=['Superficie Var %','Viñedos Var. %']).format(
        {"Superficie": lambda x : '{:,.0f}'.format(x), 
        "Viñedos Cnt.": lambda x : '{:,.0f}'.format(x),
        "Superficie Var %": lambda x : '{:,.2f} %'.format(x),
        "Viñedos Var. %": lambda x : '{:,.2f} %'.format(x),
                                        }
        ,
        thousands='.',
        decimal=',',
    )

    if vercnt == 1:
        column_orders =("Año", "Superficie","Superficie Var %","Viñedos Cnt.","Viñedos Var. %")
    else:
        column_orders =("Año", "Superficie","Superficie Var %")
  
    #st.write(df2)
    if st.checkbox('Ver Cantidad de Viñedos en forma de tabla'):
      st.dataframe(styled_df,
        column_config={
          'Año': st.column_config.Column('Año'),
          'Superficie': st.column_config.Column('Superficie'),
          'Viñedos Cnt.': st.column_config.Column('Viñedos Cnt.'),
          'Superficie Var %': st.column_config.Column('Superficie Var %'),
          'Viñedos Var. %': st.column_config.Column('Viñedos Var. %'),
        
          },
        column_order = column_orders,
#          column_order=[
#                  "tipo_envase",
#                  "producto",
#                  "Fob",
#                  "Part % Fob",
#                  "Litros",
#                  "Part. % Litros",
#                  "Prec x Litro"
#          ],                   
          width = 600,   
          height = 800,
          hide_index=True)


  
    #st.write(df_anual)
    #dv1['anio'] = dv1['anio'].astype(str)

    newdf=df_filtered.set_index('anio',inplace=False).rename_axis(None)
    
    option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "xAxis": {"type": "category", "data": df_anual["Año"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Viñedos" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,
                {"type": "value" , "name" : "",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,
                 "axisLine": {
                    "show": 'false',
                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },
                {"type": "value" , "name" : "Hectareas",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },            
            ],
            "series": [
                
                {"data": df_anual["Viñedos Cnt."].tolist(), "type": "bar", "name": "Viñedos", "yAxisIndex": 1,,"visible": "false",  },
                {"data": df_anual["Superficie"].tolist(), "type": "line", "name": "Hectareas", "yAxisIndex": 2, "color":'#07ECFA' },
            ],
    }

    st_echarts(options=option,key="supe" + str(dt.now()), height="400px")


    
    
with tab2:
    st.header("En Construcción")
    
with tab3:
    st.header("En Construcción")
with tab4:
    cosecha_evo.cosecha_evo()    
with tab5:
    st.header("En Construcción")
with tab6:
    st.header("En Construcción")
with tab7:
    st.header("En Construcción")
