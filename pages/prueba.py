import json
from streamlit_echarts import st_echarts
import streamlit as st

from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from datetime import datetime as dt
from exportaciones import exporta_pais1

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


tab1, tab2, tab3,tab4,tab5,tab6,tab7 = st.tabs(["Evolución", "Destinos", "Variedades","Color/Envase","Mosto Evolución","Mosto Destinos", "Mosto Productos"])
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
st_echarts(option, height="500px")

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
st_echarts(option,key="gauge2", height="500px")

with tab1:
   exporta_pais1.exporta_destino()  
  
