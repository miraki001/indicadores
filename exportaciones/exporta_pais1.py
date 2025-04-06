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

def exporta_destino():


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
        iframe[title="streamlit_echarts.st_echarts"]{ height: 800px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)     

    conn = st.connection("postgresql", type="sql")

    @st.cache_data
    def cargar_datos(consulta):
        try:
            df = conn.query(consulta, ttl="0")
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()
    QUERY_V0 = f"""
        SELECT distinct anio,variedad1 variedad,tipo_envase,color,producto,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')
        and variedad1 in ('MALBEC','CABERNET FRANC','CABERNET SAUVIGNON','BONARDA')
        and pais in ('ESTADOS UNIDOS','REINO UNIDO','BRASIL','CANADA')
    """

    
    # Cargar datos iniciales para llenar los filtros
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais  from exportaciones2_m where producto not in ('Mosto','Alcohol');"
    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    pais_list = sorted(df_filtros["pais"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    envase_list = sorted(df_filtros["tipo_envase"].dropna().unique())
    color_list = sorted(df_filtros["color"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())



    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')
        and variedad1 in  ('MALBEC','CABERNET FRANC','CABERNET SAUVIGNON','BONARDA')
        and pais in ('ESTADOS UNIDOS','REINO UNIDO','BRASIL','CANADA')
    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    

    df_filtered = dv1.copy()




    df_anual = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_variedad = df_filtered.groupby(['pais','variedad1'], as_index=False)[['fob', 'litros']].sum()


    





    df1 = pd.DataFrame({'name':var_list + pais_list})

    result1 = df1.to_json(orient="records")


    df_variedad.drop(['litros'], axis='columns', inplace=True)
    #st.write(df_variedad)
    df_variedad = df_variedad.rename(columns={'pais': "source",'variedad1': "target",'fob': "value"})

    result3 = df_variedad.to_json(orient="records")

    pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}' 

    data = json.loads(pp)


    with open("./data/producto.json", "r") as f:
        data = json.loads(f.read())



    option = {
        "title": {"text": "Sankey Diagram"},
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "type": "sankey",
                "data": data["nodes"],
                "links": data["links"],
                "emphasis": {"focus": "adjacency"},
                "levels": [
                    {
                        "depth": 0,
                        "itemStyle": {"color": "#fbb4ae"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 1,
                        "itemStyle": {"color": "#b3cde3"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 2,
                        "itemStyle": {"color": "#ccebc5"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 3,
                        "itemStyle": {"color": "#decbe4"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                ],
                "lineStyle": {"curveness": 0.5},
            }
        ],
    }
    st_echarts(option,key="otro333", height="500px")
