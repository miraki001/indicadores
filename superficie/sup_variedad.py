import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
import folium
from streamlit_folium import st_folium

from datetime import datetime as dt

def sup_variedad():




    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True)     



    df_anios = pd.read_parquet("data/processed/superficievariedad_anios.parquet", engine="pyarrow")
    year_list = df_anios["anio"].to_numpy()

    df_provincias = pd.read_parquet("data/processed/superficievariedad_provincias.parquet", engine="pyarrow")
    prov_list = df_provincias["provincia"].to_numpy()
    prov_list = np.append("Todas",prov_list )

    df_departamentos = pd.read_parquet("data/processed/cosecha_departamentos.parquet", engine="pyarrow")
    depto_list = df_departamentos["depto"].to_numpy()
    depto_list = np.append( "Todos",depto_list)
  
    
    

    


    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"
            


    

    if "filtros_cose123" not in st.session_state:
        st.session_state.filtros_cose = {
            "anio": "2024",          
            "prov": "Todas",
            "depto": "Todos",
        }




    dv1 = pd.read_parquet("data/processed/superficievariedad_datos.parquet", engine="pyarrow")

 
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2, col3 =  st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año444",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
      
        with col2:
            with st.popover("Provincia"):
                st.caption("Selecciona uno o más Provincia de la lista")
                prov = st.multiselect("Provv1",   prov_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Departamento"):
                st.caption("Selecciona uno o más Departamento de la lista")
                depto = st.multiselect("deptov",  depto_list, default=["Todos"],label_visibility="collapsed")                
    
    
    Filtro = 'Filtro = Año = '    
    if año:
        #st.write(año)
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)  
        Filtro = Filtro +  ' ' +str(año) + ' '
        
    if prov:
        if prov[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['provincia'].isin(prov)]
            #st.write(variedad)
        Filtro = Filtro + ' Provincia = ' +  str(prov) + ' '
    
    if depto:
        if depto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['departamento'].isin(depto)]          
        Filtro = Filtro + ' Departamento = ' +  str(depto) + ' '
        

    df_anual = df_filtered.groupby(['variedad',], as_index=False)[['sup']].sum()  

    df_anual  = df_anual.fillna(0)

    df_anual = df_anual.sort_index(axis = 1)
    df_anual = df_anual.rename(columns={'sup': "Superficie"})
    
    df_sorted = df_anual.sort_values(by='Superficie', ascending=False)

    styled_df = df_sorted.style.format(
            {"Superficie": lambda x : '{:,.0f}'.format(x), 
            }
            ,
            thousands='.',
            decimal=',',
    )

    column_orders =("variedad", "Superficie")

    if st.checkbox('Ver tabla Superficie por Variedades'):
        st.dataframe(styled_df,
              column_config={
                'Superficie': st.column_config.Column('Superficie'),
                },
                column_order = column_orders,
                width = 800,   
                height = 400,
                hide_index=True)

    df_anual = df_anual.rename(columns={'Superficie': "value", 'variedad': "name",})

    json_list = json.loads(json.dumps(list(df_anual.T.to_dict().values()))) 
    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Depachos Acumulados: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
            "text": 'Superficie por Variedad en Hectares',
            "subtext": Filtro,
        },        
        #"subtitle": Filtro,
        "legend": {"data": ["Hectareas","variedad"]},   
        "series": [
                {
                    "name": "Superficie Totales",
                    "type": "treemap",
                    "visibleMin": 100,
                    "label": {"show": True, "formatter": "{b}"},
                    "itemStyle": {"borderColor": "#fff"},
                    "levels": [
                        {"itemStyle": {"borderWidth": 0, "gapWidth": 5}},
                        {"itemStyle": {"gapWidth": 1}},
                        {
                            "colorSaturation": [0.35, 0.5],
                            "itemStyle": {"gapWidth": 1, "borderColorSaturation": 0.6},
                        },
                    ],
                    "data": json_list,
                }
        ]
    }
    st_echarts(
        options=option,key="gauge3322" + str(dt.now()), height="600px",
    )
