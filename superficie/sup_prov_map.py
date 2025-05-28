import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
#from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import Map
from pyecharts.charts import Line
import geopandas as gpd
import plotly.express as px
import folium
from streamlit_folium import st_folium

def get_center_latlong(df):
    # get the center of my map for plotting
    centerlat = (df['lat'].max() + df['lat'].min()) / 2
    centerlong = (df['long'].max() + df['long'].min()) / 2
    return centerlat, centerlong

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column,
                               #, locationmode="ISO-3",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(input_df['sup'])),
                               #scope="south america",
                               labels={'sup':'sup'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

def prov_map(df):

  formatter = JsCode(
    "function (params) {"
    + "var value = (params.value + '').split('.');"
    + "value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');"
    + "return params.seriesName + '<br/>' + params.name + ': ' + value;}"
  ).js_code

  #st.write(df)
  f = df.to_json(orient="records")

  pivot_table_basic = df.pivot_table(
      index='provincia', 
      #columns='iso_loc',
      values=['sup'],
      aggfunc='sum'
  )

  df1 = df.pivot_table(
      index='iso_loc', 
      #columns='iso_loc',
      values=['sup'],
      aggfunc='sum'
  )  
  df1 = df1.reset_index().rename_axis(None, axis=1)
  #st.write(df1)  
  dftt = pivot_table_basic
  pivot_table_basic = pivot_table_basic.reset_index().rename_axis(None, axis=1)
  pivot_table_basic = pivot_table_basic.rename(columns={'provincia': "name", 'sup': "value"})    
  
  f = pivot_table_basic.to_json(orient="records")
  json_obj = json.loads(f)


  #st.write(json_obj)  
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
            "min": 1,
            "max": 160000,
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
                "name": "Superficie por provincias",
                "type": "map",
                "roam": True,
                "map": "Argentina",
                "emphasis": {"label": {"show": True}},
                "data": raw_data,
            }
        ],
  }
  st_echarts(options, map=map)
  #st.map(pivot_table_basic)
  st.write('otro')
  #st.write(df)

  fig = px.choropleth(df1, locations='iso_loc',locationmode="ISO-3", color='sup')
  #fig = px.choropleth(df1, locations='iso_loc',color='sup')
 
  fig.show()

  choropleth = make_choropleth(df1, 'iso_loc', 'sup', 'blues')  
  st.plotly_chart(choropleth, use_container_width=True)

  boundary_file = "./data/argentina.json"
  with open(boundary_file, 'r') as f:
    zipcode_boundary = json.load(f)

  #center = get_center_latlong(df1)


  # Initialize Folium Map again (same as before)
  m = folium.Map(location=[40.965, -5.664], 
                 tiles='openstreetmap',
                 zoom_start=10,
                 )


  # Use the groupby method to 
  zipcode_data = df1.groupby('iso_loc').aggregate(np.mean)
  zipcode_data.reset_index(inplace = True)
  st.write(df)
  map = folium.Map(location= [38,-96.5],zoom_start= 4,tiles='CartoDB positron')
  choropleth = folium.Choropleth(
      geo_data='./data/argentina.json',
      data = df,
      columns=('provincia','sup'),
      key_on='feature.properties.name',
  )
  choropleth.geojson.add_to(map)  
  st.map = st_folium(map, width=700, height= 450)


  # Create choropleth map  
  folium.Choropleth(
    geo_data='./data/argentina.json',
    name='choropleth',
    data=df,
    columns=['sup'],
    key_on='Feature.properties.name',  
  ).add_to(m)
  m.save('c:\tmp\zipcode_choropleth.html')
