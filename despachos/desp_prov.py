import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode

from datetime import datetime as dt

def despacho_prov(df_filtros,df):




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
            
    @st.cache_data
    def cargar_datos(consulta):
        try:
            df = conn.query(consulta, ttl="0")
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()

  
  
  # Listas de valores únicos para los filtros
    #prov_list = sorted(df_filtros["provincia"].dropna().unique())
    envase_list = sorted(df_filtros["subgrupoenvase"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())
    #pais_list = sorted(df_filtros["pais"].dropna().unique())
    if "filtroseem" not in st.session_state:
        st.session_state.filtrosee = {
            "envase": "Todos",
            "producto": "Todos",
        }

    
    dv1['anio'] = dv1['anio'].astype(str)

    df_filtered = dv1.copy()
    


    with st.container(border=True):
        col1, col2 =  st.columns([1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más Productos de la lista")
                producto = st.multiselect("Producto",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más años")
            
      
        with col2:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                variedad = st.multiselect("Envasev",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")
    
    Filtro = 'Filtro = '    
        
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Productos = ' +  str(producto) + ' '
    
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['subgrupoenvase'].isin(color)]          
        Filtro = Filtro + ' Envases = ' +  str(envase) + ' '
            


    #df_anual = df_filtered.groupby(['anio','prov','depto'], as_index=False)[['peso']].sum()
    #df_anual = pd.pivot_table(df_filtered, values='peso', index=['prov'],
    #                   columns=['destino'], aggfunc="sum")

    df_anual = df_filtered.pivot_table(
          index='prov', 
          columns='destino',  
          values=['peso'],
          aggfunc='sum'
    )
    #st.write(df_anual)

    df_anual.columns = df_anual.columns.droplevel(0)
    df_anual = df_anual.reset_index().rename_axis(None, axis=1)
    df_anual  = df_anual.fillna(0)

    totelab = df_anual['Elaboracion'].sum()
    totecon = df_anual['Consumo'].sum()
    totesec = df_anual['Secado'].sum()
    #st.write(totelab)
    total = []
    totco = []
    totse = []
    totto = []
    #total.append(0)
    for index in range(len(df_anual)):
        total.append((  (df_anual['Elaboracion'].loc[index] / totelab) *100 ))
        totco.append((  (df_anual['Consumo'].loc[index] / totecon) *100 ))
        totse.append((  (df_anual['Secado'].loc[index] / totesec) *100 ))
        totto.append((  (df_anual['Secado'].loc[index]  +  df_anual['Consumo'].loc[index] + df_anual['Elaboracion'].loc[index] ) ))
    df_anual['Part. % Total Elab'] = total
    df_anual['Part. % Total Cons'] = totco
    df_anual['Part. % Total Sec'] = totse
    df_anual['Total'] = totto

    df_anual = df_anual.sort_index(axis = 1)
    df_anual = df_anual.rename(columns={'prov': "Provincia"})
    
    df_sorted = df_anual.sort_values(by='Elaboracion', ascending=False)

    styled_df = df_sorted.style.format(
            {"Elaboracion": lambda x : '{:,.0f}'.format(x), 
            "Consumo": lambda x : '{:,.0f}'.format(x), 
            "Secado": lambda x : '{:,.0f}'.format(x),  
            "Total": lambda x : '{:,.0f}'.format(x),  
            "Part. % Total Elab": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Cons": lambda x : '{:,.2f} %'.format(x),
            "Part. % Total Sec": lambda x : '{:,.2f} %'.format(x), 
            }
            ,
            thousands='.',
            decimal=',',
    )

    column_orders =("Provincia", "Elaboracion","Part. % Total Elab","Consumo","Part. % Total Cons","Secado","Part. % Total Sec","Total")

    if st.checkbox('Ver tabla Cosecha por Provincias'):
        st.dataframe(styled_df,
              column_config={
                'Elaboracion': st.column_config.Column('Elaboracion'),
                'Consumo': st.column_config.Column('Consumo'),
                'Secado': st.column_config.Column('Secado'),
                'Total': st.column_config.Column('Total'),
                'Part. % Total Elab': st.column_config.Column('Part. % Total Elab'),        
                'Part. % Total Cons': st.column_config.Column('Part. % Total Cons'),                          
                'Part. % Total Sec': st.column_config.Column('Part. % Total Sec'),                   
                },
                column_order = column_orders,
                width = 800,   
                height = 400,
                hide_index=True)
    

    dv = df_anual.groupby(['Provincia'], as_index=False)[['Total']].sum()
    dv = dv.rename(columns={'Total': "value", 'Provincia': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    st.subheader('Cosecha por Provincias en Quintales')
    #st.write(json_list)
    st.caption(Filtro)

    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Cosecha: ' + value ].join('')};"
            ).js_code,
        },
        "legend": {"data": ["Qintales","Provincia"]},   
        "series": [
                {
                    "name": "Cosecha",
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
        options=option,key="gauge2" + str(dt.now()), height="600px",
    )



    dv = df_filtered.groupby(['prov','depto'], as_index=False)[['peso']].sum()
    #dv = df_anual1
    #st.write(dv)
    dv = dv.rename(columns={'peso': "value", 'depto': "name",'prov': "id"})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.write(json_list)

    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Cosecha: ' + value ].join('')};"
            ).js_code,
        },
        "legend": {"data": ["Qintales","Provincia"]},   
        "series": [
                {
                    "name": "Cosecha",
                    "type": "treemap",
                    "visibleMin": 100,
                    "label": {"show": True, "formatter": "{b}"},
                    "itemStyle": {"borderColor": "#fff"},
                    "colorMappingBy": 'id',
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
        options=option,key="gauge2" + str(dt.now()), height="600px",
    )    
