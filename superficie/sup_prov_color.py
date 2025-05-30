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
from pyecharts.charts import Line
import folium
from streamlit_folium import st_folium

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"


def prov_color():

  df_anios = pd.read_parquet("data/processed/superficievariedad_anios.parquet", engine="pyarrow")
  year_list = df_anios["anio"].to_numpy()

  #year_list = np.append(year_list, "Todos")    
  df_variedades = pd.read_parquet("data/processed/superficievariedad_variedades.parquet", engine="pyarrow")
  var_list = df_variedades["variedad"].to_numpy()
  var_list = np.append(var_list, "Todas")
    
  if "filtros_cose2" not in st.session_state:
        st.session_state.filtros_cose2 = {
            "anio": "2024",          
            "var": "Todas"
        }
    
    

  with st.container(border=True):
        col1, col2  =  st.columns([1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
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
    

  df = pd.read_parquet("data/processed/superficievariedad_datos.parquet", engine="pyarrow")

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
            st.write(variedad)
        Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '     
  pivot_table_basic = df.pivot_table(
      index='provincia', 
      columns='color',  
      values=['sup'],
      aggfunc='sum'
  )
  #st.write(pivot_table_basic)  
  dfg = pivot_table_basic
  dfg.columns = dfg.columns.droplevel(0)
  dfg = dfg.reset_index().rename_axis(None, axis=1)
  st.write(dfg)  
  if not 'Blanca'  in dfg:
      dfg['Blanca'] = 0 
      pivot_table_basic['Blanca'] = 0 
  if not 'Rosada'  in dfg:
      dfg['Rosada'] = 0 
      pivot_table_basic['Rosada'] = 0
  if not 'Tinta'  in dfg:
      dfg['Tinta'] = 0 
      pivot_table_basic['Tinta'] = 0
    
  if 'Blanca'  in dfg:
      dfg['Blanca'] = dfg['Blanca'].fillna(0)  
      pivot_table_basic['Blanca'] = pivot_table_basic['Blanca'].fillna(0)  
  if 'Rosada' in dfg:
      dfg['Rosada'] = dfg['Rosada'].fillna(0)   
      pivot_table_basic['Rosada'] = pivot_table_basic['Rosada'].fillna(0)   
  if 'Tinta' in dfg:
      dfg['Tinta'] = dfg['Tinta'].fillna(0)    
      pivot_table_basic['Tinta'] = pivot_table_basic['Tinta'].fillna(0)    
    
  #st.write(dfg) 

  total = []
  #total.append(0)
  for index in range(len(dfg)):
      tot1 = 0
      tot2 = 0
      tot3 = 0
      if 'Blanca'  in dfg:
          tot1 = dfg['Blanca'].loc[index]
      if 'Rosada'  in dfg:
          tot2 = dfg['Rosada'].loc[index]
      if 'Tinta'  in dfg:
          tot3 = dfg['Tinta'].loc[index]
          
      total.append(tot1+ tot2+ tot3)

  pivot_table_basic['Total Prov.'] = total  

  #st.write(pivot_table_basic)
  if 'Blanca'  in dfg:
      pivot_table_basic['Blanca %'] = ((pivot_table_basic['Blanca']/pivot_table_basic['Total Prov.']))*100
  if 'Rosada'  in dfg:
      pivot_table_basic['Rosada %'] = ((pivot_table_basic['Rosada']/pivot_table_basic['Total Prov.']))*100
  if 'Tinta'  in dfg:      
      pivot_table_basic['Tinta %'] = ((pivot_table_basic['Tinta']/pivot_table_basic['Total Prov.']))*100

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)

  pivot_table_basic = pivot_table_basic.sort_index(axis = 1)


  styled_df = pivot_table_basic.style.applymap(bgcolor_positive_or_negative, subset=['Blanca %','Rosada %','Tinta %']).format(
        {"Blanca": lambda x : '{:,.0f}'.format(x), 
        "Rosada": lambda x : '{:,.0f}'.format(x),
        "Tinta": lambda x : '{:,.0f}'.format(x),
        "Blanca %": lambda x : '{:,.2f} %'.format(x),
        "Rosada %": lambda x : '{:,.2f} %'.format(x),
        "Tinta %": lambda x : '{:,.2f} %'.format(x), 
        "Total Prov.": lambda x : '{:,.0f}'.format(x),
                                        }
        ,
    thousands='.',
    decimal=',',
  )
  st.dataframe(styled_df,
      column_config={
        'provincia': st.column_config.Column('provincia'),
        'Blanca': st.column_config.Column('Blanca'),
        'Rosada': st.column_config.Column('Rosada'),
        'Tinta': st.column_config.Column('Tinta'),
        'Blanca %': st.column_config.Column('Blanca %'),
        'Rosada %': st.column_config.Column('Rosada %'),
        'Tinta %': st.column_config.Column('Tinta %'),
        'Total Prov.': st.column_config.Column('Total Prov.')  
      },
      width = 900,   
      height = 500,
      hide_index=False
  )
  option = {
        "dataZoom": [
        {
          "show": 'true',
          "realtime": 'true',
          "start": 0,
          "end": 100,
          "xAxisIndex": [0, 1]
        },
        {
          "type": 'inside',
          "realtime": 'true',
          "start": 30,
          "end": 70,
          "xAxisIndex": [0, 1]
        }
        ],
            "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dfg['provincia'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dfg['Blanca'].to_list(), "type": "line", "name": 'Blancas'}
               ,{"data": dfg['Rosada'].to_list(), "type": "line","name":'Rosadas'}
               ,{"data": dfg['Tinta'].to_list(), "type": "line","name":'Tintas'}                   
                  ]
  }
  st_echarts(
        options=option, height="400px" ,
  )
    
  df = df.groupby(['provincia',], as_index=False)[['sup']].sum()    
  df = df.reset_index().rename_axis(None, axis=1)    
    
  df_indexed = df.set_index('provincia')    

    

  df1 = df.groupby(['provincia'], as_index=False)[['sup']].sum()
  #map_dict = df.set_index('provincia')['sup'].to_dict()
  #color_scale = LinearColormap(['yellow','red'], vmin = min(map_dict.values()), vmax = max(map_dict.values()))
    
  #map = folium.Map(location= [-32,-68.5],zoom_start= 4,tiles='CartoDB positron')
  map = folium.Map(location= [-32,-68.5],zoom_start= 4,tiles='OpenStreetMap')

  def get_color(feature):
      value = map_dict.get(feature['properties']['provincia'])
      if value is None:
          return '#8c8c8c' # MISSING -> gray
      else:
          return color_scale(value)


  #stamenterrain
  choropleth = folium.Choropleth(
        geo_data='./data/argentina.json',
        data = df1,
        columns=["provincia","sup"],
        key_on='feature.properties.name',
        line_opacity=0.8,
        fill_color="YlGn",
        #fill_color=
        nan_fill_color="grey",
        legend_name="Hectareas por provincia",
        highlight=True,
  ).add_to(map)

  #df1 = df.groupby(['provincia'], as_index=False)[['sup']].sum()    
  #st.write(df1)

  df_indexed = df1.set_index('provincia')     
  df_indexed = df_indexed.reset_index().rename_axis(None, axis=1)        
  choropleth.geojson.add_to(map)  
  for feature in choropleth.geojson.data['features']:
        prov1 = feature['properties']['name']
        filtered_df = df1.loc[df1['provincia'] == prov1]
        filtered_df = filtered_df.reset_index().rename_axis(None, axis=1)
        pp = 0
        if not filtered_df.empty: 
            pp = round(filtered_df['sup'][0])
        if not filtered_df.empty: 
            feature['properties']['superficie'] = 'Superficie: ' +  str(pp)
        if  filtered_df.empty: 
            feature['properties']['superficie'] = 'Superficie:  0'
  
  choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name','superficie'],labels=False)
  )
  st.map = st_folium(map, width=800, height= 650)
