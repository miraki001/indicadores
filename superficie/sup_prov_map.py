import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import Map
from pyecharts.charts import Line

def prov_map(df):

  f = df.to_json(orient="records")

  pivot_table_basic = df.pivot_table(
      index='provincia', 
      values=['sup'],
      aggfunc='sum'
  )
  
  #st.write(pivot_table_basic)  
  pivot_table_basic = pivot_table_basic.reset_index().rename_axis(None, axis=1)
  pivot_table_basic = pivot_table_basic.rename(columns={'provincia': "name", 'sup': "value"})    
  
  f = pivot_table_basic.to_json(orient="records")
  json_obj = json.loads(f)


  st.write(json_obj)  
  raw_data = json_obj



  with open("./data/argentina.json", "r") as f:
        map = Map(
            "Argentina",
            json.loads(f.read()),
        )
  #render_usa,

  
  options = {
        "title": {
            "text": "Superficie por Provincias",
#            "subtext": "Data from www.census.gov",
#            "sublink": "http://www.census.gov/popest/data/datasets.html",
            "left": "right",
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
#            "formatter": formatter,
        },
        "visualMap": {
            "left": "right",
            "min": 5000,
            "max": 14000000,
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "series": [
            {
                "name": "Despachos por Provincias",
                "type": "map",
                "roam": True,
                "map": "Argentina",
                "emphasis": {"label": {"show": True}},
                "data": raw_data,
            }
        ],
  }
  st_echarts(options, map=map)
