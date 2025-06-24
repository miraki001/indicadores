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
            

    df_variedades = pd.read_parquet("data/processed/cosecha_variedades.parquet", engine="pyarrow")
    var_list = df_variedades["variedad"].to_numpy()
    var_list = np.append("Todas", var_list )

    df_provincias = pd.read_parquet("data/processed/cosecha_provincias.parquet", engine="pyarrow")
    prov_list = df_provincias["prov"].to_numpy()
    prov_list = np.append("Todas",prov_list )

    df_departamentos = pd.read_parquet("data/processed/cosecha_departamentos.parquet", engine="pyarrow")
    depto_list = df_departamentos["depto"].to_numpy()
    depto_list = np.append( "Todos",depto_list)
    
    df_colores = pd.read_parquet("data/processed/cosecha_colores.parquet", engine="pyarrow")
    color_list = df_colores["color"].to_numpy()
    color_list = np.append("Todos",color_list )
    
    df_destinos = pd.read_parquet("data/processed/cosecha_destinos.parquet", engine="pyarrow")
    destino_list = df_destinos["destino"].to_numpy()
    destino_list = np.append("Todos",destino_list )
    
    df_tipouvas = pd.read_parquet("data/processed/cosecha_tipouvas.parquet", engine="pyarrow")
    tipo_list = df_tipouvas["tipouva"].to_numpy()
    tipo_list = np.append("Todos",tipo_list )    



  
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
    


    with st.container(border=True):
        col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más provincia de la lista")
                provincia = st.multiselect("Provincia",  ["Todas"] +   prov_list, default=["Todas"],label_visibility="collapsed",help="Selecciona uno o más años")           
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamentos de la lista")
                depto = st.multiselect("Departamento",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")
        with col4:
            with st.popover("Destino"):
                st.caption("Selecciona uno o más Destinos de la lista")
                destino = st.multiselect("Destino",  ["Todos"] + destino_list, default=["Todos"],label_visibility="collapsed")                

        with col5:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Color",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed")                
        with col6:
            with st.popover("Tipo de Uva"):
                st.caption("Selecciona uno o más Tipos de la lista")
                tipo = st.multiselect("Gurpo Envase",  ["Todos"] + tipo_list, default=["Todos"],label_visibility="collapsed")      
    
    
    #st.write(df_filtered)
    Filtro = 'Filtro = Provincia = '    
    if provincia:
        if provincia[0] != 'Todas':        
            df_filtered = df_filtered[df_filtered['prov'].isin(provincia)]
        Filtro = Filtro +  ' ' + str(provincia) + ' '
    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['depto'].isin(depto)]
        Filtro = Filtro + ' Departamento = ' +  str(depto) + ' '
            
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
        Filtro = Filtro + ' Color = ' +  str(color) + ' '
            
    if destino:
        if destino[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['destino'].isin(destino)]               
        Filtro = Filtro + ' Destino = ' +  str(destino) + ' '
    if tipo:
        if tipo[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipouva'].isin(tipo)]      
        Filtro = Filtro + ' Tipo = ' +  str(tipo) + ' '
    

    df_anual = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()
    st.write(df_anual)
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
            {"Quintales": lambda x : '{:,.0f}'.format(x), 
            "Var % Año Ant.": lambda x : '{:,.2f} %'.format(x),                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver tabla Cosecha por Año'):
        st.dataframe(styled_df,
              column_config={
                'Pais': st.column_config.Column('Pais'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
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
                {"type": "value" ,"name" : "Quintales" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,           
            ],
            "series": [
                {"data": df_anual["Quintales"].tolist(),"position" : 'rigth', "type": "line", "name": "Quintales" },
            ],
        }

    
    st_echarts(options=option,key="gauge" + str(dt.now()), height="400px")
