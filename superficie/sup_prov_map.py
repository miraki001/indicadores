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


  df = pd.read_parquet("data/processed/superficievariedad_datos.parquet", engine="pyarrow")

  df['anio'] = df['anio'].astype(str)

  df_anios = pd.read_parquet("data/processed/superficievariedad_anios.parquet", engine="pyarrow")
  year_list = df_anios["anio"].to_numpy()    

  df_variedades = pd.read_parquet("data/processed/superficievariedad_variedades.parquet", engine="pyarrow")
  var_list = df_variedades["variedad"].to_numpy()
  var_list = np.append(var_list, "Todas")

  if "filtros_cose3" not in st.session_state:
        st.session_state.filtros_cose2 = {
            "anio": "2024",          
            "var": "Todas"
        }

  with st.container(border=True):
        col1, col2  =  st.columns([1, 1])  # Ajusta los tamaños de las columnas
      
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año1",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
      
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  var_list, default=["Todas"],label_visibility="collapsed")        


  df['anio'] = df['anio'].astype(str)

  Filtro = 'Filtro = Año = '  
  if año:
        df = df[df['anio'].isin(año)]
        df["anio"] = df["anio"].astype(str)  
        Filtro = Filtro +  ' ' +str(año) + ' '
  #st.write(df)      
  if variedad:
        if variedad[0] != 'Todas':
            df = df[df['variedad'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '      
      


  #df = df.groupby(['provincia',], as_index=False)[['sup']].sum()    
  #df = df.reset_index().rename_axis(None, axis=1)    
    
  df_indexed = df.set_index('provincia')    
    
  #st.write(df)
  #st.write(df_indexed)  
  map = folium.Map(location= [-32,-68.5],zoom_start= 4,tiles='CartoDB positron')
  choropleth = folium.Choropleth(
      geo_data='./data/argentina.json',
      data = df,
      columns=["provincia","sup"],
      key_on='feature.properties.name',
      line_opacity=0.8,
      fill_color="YlGn",
      nan_fill_color="purple",
      legend_name="Hectareas por provincia",
      bins=[1,10000, 150000],
      highlight=True,
  ).add_to(map)

  df1 = df.groupby(['provincia'], as_index=False)[['sup']].sum()    
  #st.write(df1)

  #filtered_df = df1.loc[df1['provincia'] == 'Entre Rios']  
  #filtered_df = filtered_df.reset_index().rename_axis(None, axis=1)
  #df1 = df1.reset_index().rename_axis(None, axis=1)    
  df_indexed = df1.set_index('provincia')     
  df_indexed = df_indexed.reset_index().rename_axis(None, axis=1)        
  #pp = filtered_df['sup'][0]
  #pp = df1.loc["Salta", 'sup']
  #st.write(pp)    
  choropleth.geojson.add_to(map)  
  for feature in choropleth.geojson.data['features']:
      prov1 = feature['properties']['name']
      filtered_df = df1.loc[df1['provincia'] == prov1]
      #st.write(len(df.columns) )
      filtered_df = filtered_df.reset_index().rename_axis(None, axis=1)
      #st.write(prov1)
      pp = 0
      if not filtered_df.empty: 
          pp = round(filtered_df['sup'][0])
          #st.write(pp)
      if not filtered_df.empty: 
          #feature['properties']['superficie'] = 'Superficie: ' +  '{:,}'.format(df_indexed.loc[prov1, 'sup'][0]) if prov1 in list(df_indexed.index) else ''
          feature['properties']['superficie'] = 'Superficie: ' +  str(pp)
      if  filtered_df.empty: 
          feature['properties']['superficie'] = 'Superficie:  0'
  
  choropleth.geojson.add_child(
      folium.features.GeoJsonTooltip(['name','superficie'],labels=False)
  )
  st.map = st_folium(map, width=800, height= 650)


  
