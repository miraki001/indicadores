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

def exporta_destino():

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
    QUERY_V0 = f"""
        SELECT distinct anio,variedad1 variedad,tipo_envase,color,producto,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """

    
    # Cargar datos iniciales para llenar los filtros
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais  from exportaciones2_m where producto not in ('Mosto','Alcohol');"
    df_filtros = cargar_datos(QUERY_V0)

    if df_filtros.empty:
        st.error("No se encontraron datos en la base de datos.")
        st.stop()

    # Listas de valores únicos para los filtros
    year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)
    pais_list = sorted(df_filtros["pais"].dropna().unique(), reverse=True)
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

    st.html(
        '''
            <style>
                div[data-testid="stPopover"]>div>button {
                    min-height: 22.4px;
                    height: 22.4px;
                    background-color: #A9F8FA !important;
                    color: black;
                }
            </style>
        '''
    )

    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """


    dv1 = cargar_datos(QUERY_V1)
 
    dv1['anio'] = dv1['anio'].astype(str)

    
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envase",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")

    df_filtered = dv1.copy()

    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)

    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad1'].isin(variedad)]
            #st.write(variedad)
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipo_envase'].isin(envase)]


    df_anual = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_variedad = df_filtered.groupby(['pais','variedad1'], as_index=False)[['fob', 'litros']].sum()
    indexes = np.r_[-30:0]
    top_bottom_10 = df_variedad.sort_values("fob", ignore_index=True).iloc[indexes]
    #df_variedad = df_variedad.sort_values('fob').head(10)
    st.write(top_bottom_10)
    pais_list1 = sorted(top_bottom_10["pais"].dropna().unique(), reverse=True)
    var_list1 = sorted(top_bottom_10["variedad1"].dropna().unique())
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
    df_anual = df_anual.rename(columns={'litros': "Litros", 'fob': "Fob",})
    df_anual['Part. % Litros'] = total
    df_anual['Part % Fob '] = tot1
    df_anual['Prec x Litro'] = tot2

    
    df_sorted = df_anual.sort_values(by='Fob', ascending=False)

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
    st.dataframe(styled_df,
              column_config={
                'Pais': st.column_config.Column('Pais'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                width = 800,   
                height = 400,
                hide_index=True)
    
    #st.dataframe(df_sorted)
    #dv.drop('fob', axis=1, inplace=True)
    dv = dv.rename(columns={'litros': "value", 'pais': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    st.subheader('Exportaciones por Pais en Litros')
    #st.write(json_list)


    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
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
        options=option,key="gauge2" + str(dt.now()), height="600px",
    )
    st.subheader('Exportaciones por Pais en Fob')
    
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
    
    #dv1 = dv1.rename(columns={'pais': "name"})
    #df1 = dv1['nodes'].unique()

    df1 = pd.DataFrame({'name':var_list1 + pais_list1})
    #df2 = pd.DataFrame({'name':pais_list})
    #df1 = df1.rename(columns={'pais': "nodes"})
    #st.write(df1)
    result1 = df1.to_json(orient="records")
    #result2 = df2.to_json(orient="records")
    #result = df1.to_json(orient="split")
    #df1 = df1.reset_index().rename_axis(None, axis=1)
    #df1.reset_index(drop=True)
    #result = var_list.to_json(orient="split")
    #json_list = json.loads(json.dumps(list(df1.T.to_dict().values()))) 
    st.write(result1)
    #json_list1 = json.loads(json.dumps(list(df2.T.to_dict().values()))) 
    #st.write(json_list1)
    #tt = result1 + result2
    #st.write(tt)
    top_bottom_10.drop(['litros'], axis='columns', inplace=True)
    #st.write(df_variedad)
    top_bottom_10 = top_bottom_10.rename(columns={'pais': "source",'variedad1': "target",'fob': "value"})
    #json_list1 = json.loads(json.dumps(list(df2.T.to_dict().values()))) 
    #result = json.loads(json.dumps(list(df_variedad.T.to_dict().values()))) 
    result3 = top_bottom_10.to_json(orient="records")
    #st.write(result3)
    pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}' 
    #st.write(pp)
    data1 = json.loads(pp)
    #st.write(pp)
    #df2 = dv1['variedad1']
    #df3 = df1+ df2
    #st.write(data["nodes"])

    with open("./data/producto.json", "r") as f:
        data = json.loads(f.read())



    option = {
        "title": {"text": "Sankey Diagram"},
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "type": "sankey",
                "data":  data1["nodes"],
                "links": data1["links"],
                "emphasis": {"focus": "adjacency"},
                "levels": [
                    {
                        "depth": 0,
                        "itemStyle": {"color": "#fbb4ae"},
                        "lineStyle": {"color": "target", "opacity": 0.6},
                    },
                    {
                        "depth": 1,
                        "itemStyle": {"color": "#b3cde3"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 2,
                        "itemStyle": {"color": "#ccebc5"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 3,
                        "itemStyle": {"color": "#decbe4"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                ],
                "lineStyle": {"curveness": 0.5},
            }
        ],
    }
    st_echarts(option,key="otro", height="500px")
