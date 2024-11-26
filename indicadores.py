import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
import altair as alt



colorPalette = ['#00b04f', '#ffbf00', 'ff0000']

st.set_page_config(
    page_title="Indicadores",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

#alt.themes.enable("dark")

st.title("Indicadores")


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




hide_streamlit_style = """
            <style>
                
                header {visibility: hidden;}
                footer {visibility: hidden;} 
                .streamlit-footer {display: none;}
                
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Exportaciones", "Mercado Interno", "Cosecha y Superficie"])

with tab1:
    st.header("Exportaciones")

    col = st.columns((1.5, 4.5, 2), gap='medium')

    with col[0]:
        st.markdown('Exportaciones')
        st.metric(label='HL', value= 814101 , delta=-0.97)
        st.metric(label='FOB', value= 272923476 , delta=-1.72)
        st.markdown('Mostos')
        st.metric(label='HL', value= 201909 , delta=102.98)
        st.metric(label='FOB', value= 46389836 , delta=85.97)

    
    with col[1]:
        st.markdown('Mercado Interno')
        st.markdown('Despachos por color, en H')
        options = {
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": 62.17, "name": "Tintos"},
                    {"value": 30.12, "name": "Blancos"},
                    {"value": 7.71, "name": "Rosados"},
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(10, 0, 0, 0.5)",
                    }
                },
            }
            ],
        }
        st_echarts(
            options=options, height="200px",
        )

        st.markdown('Por Envases Tintos')
        options = {
            "color": [
            '#dd6b66',
            '#759aa0',
            '#e69d87',
            '#8dc1a9',
            '#ea7e53',
            '#eedd78',
            '#73a373',
            '#73b9bc',
            '#7289ab',
            '#91ca8c',
            '#f49f42'
             ],
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": 67.34, "name": "Botella"},
                    {"value": 27.67, "name": "Multilaminados"},
                    {"value": 4.99, "name": "Otros"},
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
            ],
        }
        st_echarts(
            options=options, height="200px",
        )
        st.markdown('Por Envases  Blancos')
        options = {
            "color": [
            '#37A2DA',
            '#32C5E9',
            '#67E0E3',
            '#9FE6B8',
            '#FFDB5C',
            '#ff9f7f',
            '#fb7293',
            '#E062AE',
            '#E690D1',
            '#e7bcf3',
            '#9d96f5',
            '#8378EA',
            '#96BFFF'
            ],
            "title": {"text": "", "left": "center"},
            "subtitle":{"text": ""},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
            {
                "name": "Hl",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": 44.65, "name": "Botella"},
                    {"value": 51.55, "name": "Multilaminados"},
                    {"value": 4.10, "name": "Otros"},
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 10, 0, 0.5)",
                    }
                },
            }
            ],
        }
        st_echarts(
            options=options, height="200px",
        )

    with col[2]:
        st.markdown('Mercado Interno')
        st.markdown('Evolucion Mensual')

        conn = st.connection("postgresql", type="sql")
        df1 = conn.query('select anio,tintos,blancos,rosados from info_desp_anio_mes_v1 where anio >= 2022;', ttl="0"),
        df2 = df1[0]
    
        option = {
            "color": [
            '#dd6b66',
            '#759aa0',
            '#e69d87',
            '#8dc1a9',
            '#ea7e53',
            '#eedd78',
            '#73a373',
            '#73b9bc',
            '#7289ab',
            '#91ca8c',
            '#f49f42'
             ],
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": { "type": 'cross' }
            },
            "legend": {},    
            "xAxis": {
                "type": "category",
                "data": df2['anio'].to_list(),
            },
            "yAxis": {"type": "value"},
            "series": [{"data": df2['tintos'].to_list(), "type": "line", "name": 'Tintos'},
                       {"data": df2['blancos'].to_list(), "type": "line", "name": 'Blancos'},
                       {"data": df2['rosados'].to_list(), "type": "line", "name": 'Rosados'},
                   ]
            }
        st_echarts(
            options=option, height="400px" ,
        )    


with tab2:
    st.header("Mercado Interno")

    conn = st.connection("postgresql", type="sql")
    df1 = conn.query('select anioant,anioactual from inv_desp_compa() order by indice;', ttl="0"),
    df2 = df1[0]
    st.write(df2)
    st.write(df2.anioant[14])
    blancoant = df2.anioant[14]
    colorant = df2.anioant[15]
    sinant = df2.anioant[16]


    col1 = st.columns((1.5, 4.5, 2), gap='medium')
    

    
    with col1[0]:
        st.markdown('Despachos Noviembre 2023')


        option = {
        "tooltip": {
            "trigger": "item"
        },    
        "legend": {
            "top": "5%",
            "left": "center" 
            },

        "series": [
            {
                "name": "año 2023",
                "type": "pie",
                "radius": ["40%", "70%"],
                "center": ["50%", "50%"],
                "startAngle": 180,
                "endAngle": 360,
                "data": [
                    {"value": blancoant, "name": "Blanco"},
                    {"value": colorant, "name": "Color"},
                    {"value": sinant, "name": "sin espec."},
                ],
            }
            ],
        }
        st_echarts(
            options=option, height="200px",
        )


    
with tab3:
    st.header("Cosecha y Superficie")
    
