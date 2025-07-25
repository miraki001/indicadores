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

def exporta_mosto_destino():

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

    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True) 

    
    #st.write(dt.now().year)
    #estado =  st.session_state['vEstado'] 
    #if estado == '0':
        #st.rerun()
        

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
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto  from exportaciones2_m where producto = 'Mosto' and codigoproducto like '%CONCENTRADO%' ; "
#where producto = 'Mosto' and codigoproducto like '%CONCENTRADO%;    
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
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "anio": "Todos",
            "var": "Todas",
            "envase": "Todos",
            "vcolor": "Todos",
            "producto": "Todos"
        }



    QUERY_V1 = f"""
        SELECT anio, (cantlitros/743.5) AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais
        FROM exportaciones2_m 
        where producto = 'Mosto'
        and codigoproducto like '%CONCENTRADO%' 
        
    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)
    dv1 = dv1.astype({'litros' : int, 'fob': int} )    
    
    with st.container(border=True):
        #col1 = st.columns([1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        #with col1:
        with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año4",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            

    df_filtered = dv1.copy()
    Filtro = 'Filtro = Año = '
    
    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)
        Filtro = Filtro + str(año) + ' '


    df_anual = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    dv = df_anual.copy()
    total = []
    tot1 = []
    tot2 = []
    #total.append(0)
    #tot1.append(0)
    #tot2.append(0)
    #df_anual.columns = df_anual.columns.droplevel(0)
    #st.write(df_anual['litros'])
    df_anual = df_anual.reset_index().rename_axis(None, axis=1)
    totlitros = df_anual['litros'].sum()
    totfob = df_anual['fob'].sum()
    for index in range(len(df_anual)):
        #if index > 0:
            total.append((  (df_anual['litros'].loc[index] / totlitros ) *100 ))
            tot1.append((  (df_anual['fob'].loc[index] / totfob *100 )))
            tot2.append((  (df_anual['fob'].loc[index] / df_anual['litros'].loc[index]) )    )
        #st.write(total)
    df_anual = df_anual.rename(columns={'litros': "Toneladas", 'fob': "Fob",})
    df_anual['Part. % Litros'] = total
    df_anual['Part % Fob '] = tot1
    df_anual['Prec x Litro'] = tot2

    
    df_sorted = df_anual.sort_values(by='Fob', ascending=False)

    styled_df = df_sorted.style.format(
            {"Toneladas": lambda x : '{:,.0f}'.format(x), 
            "Fob": lambda x : '{:,.0f}'.format(x),
            "Part. % Litros": lambda x : '{:,.2f} %'.format(x),
            "Part % Fob": lambda x : '{:,.2f} %'.format(x),
            "Prec x Litro": lambda x : '{:,.2f}'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
    )

    if st.checkbox('Ver Exportaciones de Mosto por pais en forma de tabla'):    
        st.dataframe(styled_df,
              column_config={
                'Pais': st.column_config.Column('Pais'),
                'Toneladas': st.column_config.Column('Toneladas'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                width = 800,   
                height = 600,
                hide_index=True)
    
    dv = dv.rename(columns={'litros': "value", 'pais': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.subheader('Exportaciones por Pais en Toneladas')
    #st.write(json_list)
    st.caption(Filtro)

    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
                "text": 'Exportaciones de Mosto por pais en Tn. ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
        },          
        "legend": {"data": ["Toneladas","Pais"]},   
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
        options=option,key="gauge2" + str(dt.now()), height="600px",
    )
    st.subheader('Exportaciones por Pais en Fob')
    st.caption(Filtro)
    
    dv = dv.rename(columns={'value': "litros", 'pais': "name",})
    dv = dv.rename(columns={'fob': "value", 'pais': "name",})
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
                "text": 'Exportaciones de Mosto por pais en Fob ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
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
        options=option,key="gauge4" + str(dt.now()), height="600px",
    )
