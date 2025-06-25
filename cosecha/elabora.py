import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def elabora_evo():




    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)     

  
    

    conn = st.connection("postgresql", type="sql")

    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"
            
    df_anios = pd.read_parquet("data/processed/cosecha_anios.parquet", engine="pyarrow")
    year_list = df_anios["anio"].to_numpy()
    #year_list = np.append(year_list, "Todos")   
    actual = dt.now().year -10 
    dv22 = df_anios[df_anios['anio'] > actual ]
    year_filter = dv22["anio"].to_numpy()
    #st.write(year_filter)



    df_provincias = pd.read_parquet("data/processed/cosecha_provincias.parquet", engine="pyarrow")
    prov_list = df_provincias["prov"].to_numpy()
    prov_list = np.append("Todas",prov_list )

    df_departamentos = pd.read_parquet("data/processed/cosecha_departamentos.parquet", engine="pyarrow")
    depto_list = df_departamentos["depto"].to_numpy()
    depto_list = np.append( "Todos",depto_list)
    
    df_colores = pd.read_parquet("data/processed/despachos_color.parquet", engine="pyarrow")
    color_list = df_colores["color"].to_numpy()
    color_list = np.append("Todos",color_list )
    
    


  
    if "filtros_cose" not in st.session_state:
        st.session_state.filtros_cose = {
            "provincias": "Todas",
            "var": "Todas",
            "depto": "Todos",
            "color": "Todos",
            "destino": "Todos",
            "tipo": "Todos"
        }


    dv1 = pd.read_parquet("data/processed/elabora_datos.parquet", engine="pyarrow")
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    st.write(df_filtered)
    


    with st.container(border=True):
        col1, col2, col3,col4 = st.columns([1, 1, 1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año

        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o mÃ¡s aÃ±os de la lista")
                #aÃ±o = st.multiselect("AÃ±oe",  year_list, default= ['Todos'],label_visibility="collapsed",help="Selecciona uno o mÃ¡s aÃ±os")
                año = st.multiselect("Año111e",  year_list, default= year_filter,label_visibility="collapsed",help="Selecciona uno o mÃ¡s años")
                #anio = st.multiselect("AÃ±o:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
        
        with col2:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más provincia de la lista")
                provincia = st.multiselect("Provinciae",   prov_list, default=["Todas"],label_visibility="collapsed",help="Selecciona uno o más años")           
        # Columna 2: Filtro para Países

        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                depto = st.multiselect("Departamentoe",  depto_list, default=["Todos"],label_visibility="collapsed")

        with col4:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Colore",  color_list, default=["Todos"],label_visibility="collapsed")                
    
    
    
    #st.write(df_filtered)
    Filtro = 'Filtro = Año = '
    Filtro = Filtro +  ' Todos '

    if año:
        #st.write(año)
        if añ[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['anio'].isin(año)]
            df_filtered["anio"] = df_filtered["anio"].astype(str)  
        Filtro = Filtro +  ' ' +str(año) + ' '
    
    Filtro = 'Filtro = Provincia = '    
    if provincia:
        if provincia[0] != 'Todas':        
            df_filtered = df_filtered[df_filtered['prov'].isin(provincia)]
        Filtro = Filtro +  ' ' + str(provincia) + ' '
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['depto'].isin(depto)]
        Filtro = Filtro + ' Departamento = ' +  str(depto) + ' '
            
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
        Filtro = Filtro + ' Color = ' +  str(color) + ' '
            
    
    df_filtered = df_filtered[df_filtered['producto'] != 'Alcohol' ]
    df_filtered = df_filtered[df_filtered['producto'] != 'Mosto' ]
    dv2 = df_filtered
    df_anual = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()
    #st.write(df_anual)
    total = []
    total.append(0)
    for index in range(len(df_anual)):
      if index > 0:
        total.append((  (df_anual['litros'].loc[index] / df_anual['litros'].loc[index -1]) -1 ) *100 )
    df_anual = df_anual.rename(columns={'litros': "Hl",'anio': "Año"})
    df_anual['Var % Año Ant.'] = total

    df_anual = df_anual.sort_index(axis = 1)

    
    df_sorted = df_anual.sort_values(by='Año', ascending=True)

    styled_df = df_sorted.style.applymap(bgcolor_positive_or_negative, subset=['Var % Año Ant.']).format(
            {"Hl": lambda x : '{:,.0f}'.format(x), 
            "Var % Año Ant.": lambda x : '{:,.2f} %'.format(x),                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver tabla Elaboración por Año'):
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),
                'Hl': st.column_config.Column('Hl'),
                'Var % Año Ant.': st.column_config.Column('Var % Año Ant.'),
        
                },
                width = 400,   
                height = 400,
                hide_index=True)
    
    st.caption(Filtro)

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
                {"type": "value" ,"name" : "Hl" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,           
            ],
            "series": [
                {"data": df_anual["Hl"].tolist(),"position" : 'rigth', "type": "line", "name": "Hl" },
            ],
        }

    
    st_echarts(options=option,key="gauge" + str(dt.now()), height="400px")
    df = dv2.groupby(['prov','producto'], as_index=False)[['litros']].sum()    
    df = df.reset_index().rename_axis(None, axis=1)
    
    fig = px.sunburst(df, path=['prov', 'producto'], values='litros',
                      color='variedad', hover_data=['prov'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df['index'], weights=df['litros']))
    st.plotly_chart(fig, theme="streamlit")	
    fig = px.treemap(df, path=[px.Constant("Todas"), 'prov', 'producto'], values='litros')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, theme="streamlit")    
