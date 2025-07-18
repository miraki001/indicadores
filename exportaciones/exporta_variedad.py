import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from datetime import datetime as dt

def exporta_variedades():

    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"

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

    #st.write(dt.now().year)

    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True) 



    conn = st.connection("postgresql", type="sql")

    @st.cache_data
    def cargar_datos(consulta):
        try:
            df = conn.query(consulta, ttl="0")
            return df
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return pd.DataFrame()

    # Cargar datos iniciales para llenar los filtros
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais  from exportaciones2_m  where producto not in ('Mosto','Alcohol');"
    df_filtros = cargar_datos(QUERY_INICIAL)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    var_list = sorted(df_filtros["variedad"].dropna().unique())
    envase_list = sorted(df_filtros["tipo_envase"].dropna().unique())
    color_list = sorted(df_filtros["color"].dropna().unique())
    producto_list = sorted(df_filtros["producto"].dropna().unique())
    pais_list = sorted(df_filtros["pais"].dropna().unique())
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "anio": "Todos",
            "var": "Todas",
            "envase": "Todos",
            "vcolor": "Todos",
            "producto": "Todos",
            "pais": "Todos",
        }



    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais,producto
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')
    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    
    with st.container(border=True):
        col1, col2, col3,col4 = st.columns([1, 1, 1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año1",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más producto de la lista")
                producto = st.multiselect("Producto1",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envase1",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")
        with col4:
            with st.popover("Paises"):
                st.caption("Selecciona uno o más Paises de la lista")
                pais = st.multiselect("Pais1",  ["Todos"] + pais_list, default=["Todos"],label_visibility="collapsed")                

    df_filtered = dv1.copy()
    Filtro = 'Filtro = Año = '
    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)
        Filtro = Filtro + str(año) + ' '
    #if variedad:
        #if variedad[0] != 'Todas':
            #df_filtered = df_filtered[df_filtered['variedad1'].isin(variedad)]
            #st.write(variedad)
        #Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipo_envase'].isin(envase)]
        Filtro = Filtro + ' Envase = ' +  str(envase) + ' '            
    if pais:
        if pais[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['pais'].isin(pais)]
        Filtro = Filtro + ' Paises = ' +  str(pais) + ' '            
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(producto)]        
        Filtro = Filtro + ' Producto = ' +  str(producto)  + ' '            
    
    df_anual = df_filtered.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
    dv = df_anual.copy()
    #st.write(Filtro)
    total = []
    tot1 = []
    tot2 = []
    #total.append(0)
    #tot1.append(0)
    #tot2.append(0)
    #df_anual.columns = df_anual.columns.droplevel(0)
    #st.write(df_anual['litros'])
    st.write(df_anual)
    df_anual = df_anual.reset_index().rename_axis(None, axis=1)
    totlitros = df_anual['litros'].sum()
    totfob = df_anual['fob'].sum()
    for index in range(len(df_anual)):
        #if index > 0:
            total.append((  (df_anual['litros'].loc[index] / totlitros ) *100 ))
            tot1.append((  (df_anual['fob'].loc[index] / totfob *100 )))
            tot2.append((  (df_anual['fob'].loc[index] / df_anual['litros'].loc[index]) )    )
        #st.write(total)
    df_anual = df_anual.rename(columns={'litros': "Litros", 'fob': "Fob",})
    df_anual['Part. % Litros'] = total
    df_anual['Part % Fob '] = tot1
    df_anual['Prec x Litro'] = tot2
    #df_anual = df_anual.reset_index().rename_axis(None, axis=1)
    st.write(df_anual)

    
    df_sorted = df_anual.sort_values(by='Fob', ascending=False)
    #df_sorted = df_sorted.reset_index().rename_axis(None, axis=1)

    styled_df = df_sorted.style.format(
            {"Litros": lambda x : '{:,.0f}'.format(x), 
            "Fob": lambda x : '{:,.0f}'.format(x),
            "Part. % Litros": lambda x : '{:,.2f} %'.format(x),
            "Part % Fob": lambda x : '{:,.2f} %'.format(x),
            "Prec x Litro": lambda x : '{:,.2f}'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver tabla Exportaciones según la Variedad'):
        st.dataframe(styled_df,
              column_config={
                'Variedad': st.column_config.Column('Variedad'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                width = 800,   
                height = 200,
                hide_index=True)

    
    #st.dataframe(df_sorted)
    #dv.drop('fob', axis=1, inplace=True)
    dv = dv.rename(columns={'litros': "value", 'variedad1': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.subheader('Exportaciones por Variedad en Litros')
    #st.write(Filtro)


    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
            "text": 'Exportaciones por Variedad en Litros',
            "subtext": Filtro,
        },        
        #"subtitle": Filtro,
        "legend": {"data": ["litros","Pais"]},   
        "series": [
                {
                    "name": "Ventas Totales",
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
        options=option,key="gauge22" + str(dt.now()), height="600px",
    )
    #st.subheader('Exportaciones por variedad en Fob')
    
    dv = dv.rename(columns={'value': "litros", 'variedad1': "name",})
    dv = dv.rename(columns={'fob': "value", 'variedad1': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 

    #st.write(json_list)


    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
            "text": 'Exportaciones por Variedad en Fob',
            "subtext": Filtro,
        },        
        "legend": {"data": ["litros","Pais"]},   
        "series": [
                {
                    "name": "Ventas Totales",
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
        options=option,key="gauge44" + str(dt.now()), height="600px",
    )
