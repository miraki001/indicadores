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
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Sankey
from collections import defaultdict
import plotly.graph_objects as go
import altair as alt
import matplotlib.colors as mcolors

def exporta_destino():

    def append_row(df, row):
        return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)
    
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
        SELECT distinct anio,variedad1 variedad,tipo_envase,color,producto,pais,grupoenvase
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """

    
    # Cargar datos iniciales para llenar los filtros
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais,grupoenvase  from exportaciones2_m where producto not in ('Mosto','Alcohol');"
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
    grupoenvase_list = sorted(df_filtros["grupoenvase"].dropna().unique())
    if "filtros" not in st.session_state:
        st.session_state.filtros = {
            "anio": "Todos",
            "var": "Todas",
            "envase": "Todos",
            "vcolor": "Todos",
            "producto": "Todos",
            "grupoenvase": "Todos"
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
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,pais,color,grupoenvase,producto
        FROM exportaciones2_m 
        where producto not in ('Mosto','Alcohol')

    """


    dv1 = cargar_datos(QUERY_V1)
    dvt = dv1
 
    dv1['anio'] = dv1['anio'].astype(str)

    
    with st.container(border=True):
        col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])  # Ajusta los tamaños de las columnas

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
        with col4:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más Productos de la lista")
                producto = st.multiselect("Producto",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed")                

        with col5:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Color",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed")                
        with col6:
            with st.popover("Grupo Envase"):
                st.caption("Selecciona uno o más grupo de envases de la lista")
                grupoenvase = st.multiselect("Gurpo Envase",  ["Todos"] + grupoenvase_list, default=["Todos"],label_visibility="collapsed")      
    
    df_filtered = dv1.copy()
    Filtro = 'Filtro = Año = '
    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)
        Filtro = Filtro + str(año) + ' '
    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad1'].isin(variedad)]
            #st.write(variedad)
        Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
    
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipo_envase'].isin(envase)]
        Filtro = Filtro + ' Envase = ' +  str(envase) + ' '            
            
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
    if grupoenvase:
        if grupoenvase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['grupoenvase'].isin(grupoenvase)]               
        Filtro = Filtro + ' Grupo envase  = ' +  str(grupoenvase) + ' '            
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(producto)]      
        Filtro = Filtro + ' Producto  = ' +  str(producto) + ' '            
    

    df_anual = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_variedad = df_filtered.groupby(['pais','variedad1'], as_index=False)[['fob', 'litros']].sum()
    df_pais = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_var = df_filtered.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
    indexes = np.r_[-30:0]
    top_bottom_10 = df_variedad.sort_values("fob", ignore_index=True).iloc[indexes]
    pais_list1 = sorted(top_bottom_10["pais"].dropna().unique(), reverse=True)
    indexe1 = np.r_[-10:0]
    top_bottom_10_pais = df_pais.sort_values("fob", ignore_index=True).iloc[indexe1]
    top_bottom_10_var = df_var.sort_values("fob", ignore_index=True).iloc[indexe1]
    pais_list1 = sorted(top_bottom_10_pais["pais"].dropna().unique(), reverse=True)
    var_list1 = sorted(top_bottom_10_var["variedad1"].dropna().unique())
    df_var2= df_variedad[df_variedad['variedad1'].isin(var_list1)]
    df_var2= df_var2[df_var2['pais'].isin(pais_list1)]
    var_list1.append("OTRAS")
    pais_list1.append("OTROS")
    

    df_pais = df_filtered.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_var = df_filtered.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()

    
    top_litros_10_pais = df_pais.sort_values("litros", ignore_index=True).iloc[indexe1]
    top_litros_10_var = df_var.sort_values("litros", ignore_index=True).iloc[indexe1]
    pais_listlts = sorted(top_litros_10_pais["pais"].dropna().unique(), reverse=True)
    var_listlts = sorted(top_litros_10_var["variedad1"].dropna().unique())
    df_varlts= df_variedad[df_variedad['variedad1'].isin(var_listlts)]
    
    df_varlts= df_varlts[df_varlts['pais'].isin(pais_listlts)]
    var_listlts.append("OTRAS")
    var_listp = var_listlts
    var_listlts.append("TOTAL VARIEDAD")
    pais_listlts.append("OTROS")
    pais_listp =pais_listlts
    pais_listlts.append("TOTAL PAISES")
    #st.write(df_varlts)

    

    df_var2 = df_var2.reset_index().rename_axis(None, axis=1)

    df11 = pd.DataFrame({'name':var_list1 + pais_list1})

    df42 = pd.DataFrame({'name':var_listp})
    level = []
    for index in range(len(df42)):
         level.append('3')   
    df42['level'] = level                       
    new_row = pd.Series({'name':'TOTAL VARIEDAD','level': 4})
    df42 = append_row(df42, new_row)    

    
    df43 = pd.DataFrame({'name': pais_listp})
    level = []
    for index in range(len(df43)):
         level.append('2')   
    df43['level'] = level                       
    
    new_row = pd.Series({'name':'TOTAL PAISES','level': 1})
    df43 = append_row(df43, new_row)    


    #df55 = df43.add(df42)
    df55 = pd.concat([df42, df43])
    nodos = df55.to_json(orient="records")
    
    
    result1 = df11.to_json(orient="records")
    
    
    top_bottom_11 = df_variedad.sort_values("litros", ignore_index=True).iloc[indexes]
    pais_list11 = sorted(top_bottom_11["pais"].dropna().unique(), reverse=True)
    var_list11 = sorted(top_bottom_11["variedad1"].dropna().unique())
    dv = df_anual.copy()
    total = []
    tot1 = []
    tot2 = []
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

    if st.checkbox('Ver tabla Exportaciones por Paises'):
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
    
    dv = dv.rename(columns={'litros': "value", 'pais': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.subheader('Exportaciones por Pais en Litros')


    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
            "text": 'Exportaciones por Pais en Litros',
            "subtext": Filtro,
        },        
        #"        
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
    #st.subheader('Exportaciones por Pais en Fob')
    
    dv = dv.rename(columns={'value': "litros", 'pais': "name",})
    dv = dv.rename(columns={'fob': "value", 'pais': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 



    option = {
        "tooltip": {
            #"trigger": 'axis',
            #"axisPointer": { "type": 'cross' },
            "formatter": JsCode(
                "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
            ).js_code,
        },
        "title": {
            "text": 'Exportaciones por  Pais en Fob',
            "subtext": Filtro,
        },         
        "legend": {"data": ["litros","Pais"]},   
        "series": [
                {
                    "name": "Ventas Totales",
                    "type": "treemap",
                    "visibleMin": 100,
                    "visualMin": -100,
                    "visualMax": 100,
                    "visualDimension": 3,
                    "label": {"show": True, "formatter": "{b}"},
                    "itemStyle": {"borderColor": "#fff"},
                    "levels": [
                        #{"itemStyle": {"borderWidth": 0, "gapWidth": 5}},
                        #{"itemStyle": {"gapWidth": 1}},
                      {
                          "itemStyle": {
                          "borderWidth": 3,
                          "borderColor": '#333',
                          "gapWidth": 3,
                        }
                      },
                      
                      {
                            #"color": ['#942e38', '#aaa', '#269f3c'],
                            #"color" :'#942e38',
                            #"colorMappingBy": 'value',
                            "colorSaturation": [0.35, 0.5],
                            "itemStyle": {
                              "gapWidth": 1
                            },
                            #"itemStyle": {"gapWidth": 1, "borderColorSaturation": 0.6},
                      },
                    ],
                    "data": json_list,
                }
        ]
    }
    st_echarts(
        options=option,key="gauge4" + str(dt.now()), height="600px",
    )
    
#agregamos el fob del resto de los paises y el resto de las variedade

    df_var3 = df_var2.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_var4 = df_var2.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
    lista = ''
    for index in range(len(top_bottom_10_pais)) :
        valor = top_bottom_10_pais['fob'].iloc[index]
        pais = top_bottom_10_pais['pais'].iloc[index]
        valor1 = df_var3.loc[df_var3["pais"] == pais, "fob"]
        dif = valor - int(valor1)
        new_row = pd.Series({'fob': dif, 'pais': pais, 'variedad1': 'OTRAS','litros': 1, 'index' : len(df_var2)})
        df_var2 = append_row(df_var2, new_row)    

    for index in range(len(top_bottom_10_var)) :
        valor = top_bottom_10_var['fob'].iloc[index]
        var = top_bottom_10_var['variedad1'].iloc[index]
        valor1 = df_var4.loc[df_var4["variedad1"] == var, "fob"]
        dif = valor - int(valor1)
        new_row = pd.Series({'fob': dif, 'pais': 'OTROS', 'variedad1': var,'litros': 1, 'index' : len(df_var2)})
        df_var2 = append_row(df_var2, new_row)    

    
    df_var2.drop(['litros'], axis='columns', inplace=True)
    df_var2 = df_var2.rename(columns={'pais': "source",'variedad1': "target",'fob': "value"})
    result3 = df_var2.to_json(orient="records")
    pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}' 
    data1 = json.loads(pp)


    option = {
        "title":{
            "top": 0,
            "text": "Top 10 en Valor Fob",
            "subtext": Filtro,
        },
        "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
        "series": [
            {
                "top": 55,
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

    
    #agregamos los litros del resto de los paises y el resto de las variedade
    df_var3 = df_varlts.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
    df_var4 = df_varlts.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
    #st.write(top_litros_10_pais)
    #st.write(top_litros_10_var)
    tot1 = 0
    for index in range(len(top_litros_10_pais)) :
        valor = top_litros_10_pais['litros'].iloc[index]
        pais = top_litros_10_pais['pais'].iloc[index]
        valor1 = df_var3.loc[df_var3["pais"] == pais, "litros"]
        dif = valor - int(valor1)
        tot1 = tot1 + dif
        new_row = pd.Series({'fob': 1, 'pais': pais, 'variedad1': 'OTRAS','litros': dif, 'index' : len(df_varlts)})
        df_varlts = append_row(df_varlts, new_row)    
    #st.write(df_varlts)
    
    for index in range(len(top_litros_10_pais)) :
        valor = top_litros_10_pais['litros'].iloc[index]
        pais = top_litros_10_pais['pais'].iloc[index]
        new_row = pd.Series({'fob': 1, 'pais': 'TOTAL PAISES', 'variedad1': pais,'litros': valor, 'index' : len(df_varlts)})
        df_varlts = append_row(df_varlts, new_row) 



    tot = 0
    for index in range(len(top_litros_10_var)) :
        valor = top_litros_10_var['litros'].iloc[index]
        var = top_litros_10_var['variedad1'].iloc[index]
        valor1 = df_var4.loc[df_var4["variedad1"] == var, "litros"]
        dif = valor - int(valor1)
        tot = tot + dif
        new_row = pd.Series({'fob': 1, 'pais': 'OTROS', 'variedad1': var,'litros': dif, 'index' : len(df_varlts)})
        df_varlts = append_row(df_varlts, new_row)    

    new_row = pd.Series({'fob': 1, 'pais': 'OTROS', 'variedad1': 'OTRAS','litros': 100000, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row)    
    #new_row = pd.Series({'fob': 1, 'pais': 'FRANCIA', 'variedad1': 'MERLOT','litros': 10, 'index' : len(df_varlts)})
    #df_varlts = append_row(df_varlts, new_row)    

   
    


    df5 = df_variedad[~df_variedad['variedad1'].isin(var_listlts)]
    df5 = df5[~df5['pais'].isin(pais_listlts)]
    Total = df5['litros'].sum()
    new_row = pd.Series({'fob': 1, 'pais': 'TOTAL PAISES', 'variedad1': 'OTROS','litros': tot+ Total, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row) 
    
    for index in range(len(top_litros_10_pais)) :
        valor = top_litros_10_var['litros'].iloc[index]
        var = top_litros_10_var['variedad1'].iloc[index]
        new_row = pd.Series({'fob': 1, 'variedad1': 'TOTAL VARIEDAD', 'pais': var,'litros': valor, 'index' : len(df_varlts)})
        df_varlts = append_row(df_varlts, new_row)  
    
    new_row = pd.Series({'fob': 1, 'variedad1': 'TOTAL VARIEDAD', 'pais': 'OTRAS','litros': tot1+ Total, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row) 
   


    df11 = pd.DataFrame({'name':var_listlts + pais_listlts})
    result11 = df11.to_json(orient="records")
    
    df_varlts.drop(['fob'], axis='columns', inplace=True)
    df_varlts = df_varlts.rename(columns={'pais': "source",'variedad1': "target",'litros': "value"})

    #parte para poner los porcentajes

    source_totals = df_varlts.groupby('source')['value'].sum().to_dict()

    # Calculamos porcentaje por fila
    df_varlts['percentage'] = df_varlts.apply(
        lambda row: round((row['value'] / source_totals.get(row['source'], 1)) * 100, 2), axis=1
    ) 

    df_varlts['label'] = df_varlts.apply(
        lambda row: f"{row['source']} <> {row['target']} ({row['percentage']}%)", axis=1
    )

    # Calculamos totales por nivel
    total_source = df_varlts.groupby('source')['value'].sum().sum()
    total_target = df_varlts.groupby('target')['value'].sum().sum()

    # Listado único de nodos
    nodes = list(set(df_varlts['source']).union(set(df_varlts['target'])))

    # Enriquecemos nodos con total y %
    nodes_enriched = []
    for node in nodes:
        is_source = node in df_varlts['source'].values
        is_target = node in df_varlts['target'].values

        node_total = 0
        perc_total = 0
        if is_source:
            node_total = df_varlts[df_varlts['source'] == node]['value'].sum()
            perc_total = round((node_total / total_source) * 100, 2) if total_source else 0
        elif is_target:
            node_total = df_varlts[df_varlts['target'] == node]['value'].sum()
            perc_total = round((node_total / total_target) * 100, 2) if total_target else 0

        label = f"{node} ({node_total:,.0f} UST, {perc_total}%)"
        #nodes_enriched.append({"name": label})
        nodes_enriched.append({"original": node, "name": label, "total": node_total})

    # Ordenamos los nodos por total (descendente)
    nodes_data_sorted = sorted(nodes_enriched, key=lambda x: x["total"], reverse=True)

    # Creamos el mapping original ? enriquecido
    name_mapping = {item["original"]: item["name"] for item in nodes_data_sorted}
    #st.write(name_mapping)

    # Aplicamos el mapping
    df_varlts['source'] = df_varlts['source'].map(name_mapping)
    df_varlts['target'] = df_varlts['target'].map(name_mapping)
    nodes = list(set(df_varlts['source']).union(set(df_varlts['target'])))
    nodes = [n for n in nodes if pd.notna(n)]   

    #st.write(df_varlts)


    result1 = json.dumps(nodes_enriched)
    result3 = df_varlts.to_json(orient="records")    
    pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}'
    data1 = json.loads(pp)    

    #result32 = df_varlts.to_json(orient="records")
    #pp11 = '{ "nodes": ' + result11 + ' , "links": ' + lista + result32   + '}' 
    #data11 = json.loads(pp11)
    #pp12 =  lista + result32 
    #data12 = json.loads(pp12)

    



    
    option = {
        "title": {
            "top": 0,
            "text": "Top 10 en Litros",
            "subtext": Filtro,
            "formatter": "{b} ::::{c}"
        },
        "tooltip": {
            "trigger": "item",
            "triggerOn": "mousemove",
            "formatter": JsCode("function (info) { if (info.dataType === 'edge')     { return info.data.label || (info.data.source + ' > ' + info.data.target + '<br/>FOB: USD ' + info.data.value.toLocaleString()); } else {return info.name}};").js_code,  
                   
                   },
        "series": [
            {
                "top": 55,
                "type": "sankey",
                "data":  data1["nodes"],
                "links": data1["links"],
                "emphasis": {"focus": "adjacency"},
                "levels": [
                    {
                        "depth": 0,
                        "itemStyle": {"color": "#06C2CC"},
                        "lineStyle": {"color": "target", "opacity": 0.6},
                    },
                    {
                        "depth": 1,
                        "itemStyle": {"color": "#1E8DB6"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 2,
                        "itemStyle": {"color": "#A9F8FA"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                    {
                        "depth": 3,
                        "itemStyle": {"color": "#1E8DB6"},
                        "lineStyle": {"color": "source", "opacity": 0.6},
                    },
                ],
                "lineStyle": {"curveness": 0.5},
            }
        ],
    }
    st_echarts(option,key="otro11", height="500px")
    # Pivotear el DataFrame para que cada fila sea una provincia y cada columna un año
    st.write(dv1)
    #melted_df = melted_df[melted_df['litros'] != 0 ]
    #dv1 = dv1.groupby(['pais','anio'], as_index=False)[['litros']].sum()
    dv1 = dv1.groupby(['variedad1','anio'], as_index=False)[['litros']].sum()
    dv1 = dv1[dv1['anio'] > '2014']
    #dv2 = dv1.groupby(['pais'], as_index=False)[['litros']].sum()
    dv2 = dv1.groupby(['variedad1'], as_index=False)[['litros']].sum()
    indexe1 = np.r_[-20:0]
    dv2 = dv2.sort_values("litros", ignore_index=True).iloc[indexe1]
    #pais_list11 = sorted(dv2["pais"].dropna().unique(), reverse=True)
    var_list11 = sorted(dv2["variedad1"].dropna().unique(), reverse=True)
    #indexe1 = np.r_[-20:0]
    #dv1 = dv1.sort_values("litros", ignore_index=True).iloc[indexe1]
    #dv1 = dv1[dv1['anio'] > '2014']
    #dv1= dv1[dv1['pais'].isin(pais_list11)]
    dv1= dv1[dv1['variedad1'].isin(var_list11)]
    #dv1 = dv1[dv1['pais']== pais_list11]
    #indexe1 = np.r_[-20:0]
    #dv1 = dv1.sort_values("litros", ignore_index=True).iloc[indexe1]
    #df_pivot = dv1.pivot(index='pais', columns='anio', values='litros').reset_index()
    df_pivot = dv1.pivot(index='variedad1', columns='anio', values='litros').reset_index()

    # Asegurar que los años estén ordenados correctamente
    #df_pivot = df_pivot[['pais'] + sorted([col for col in df_pivot.columns if col != 'pais'])]
    df_pivot = df_pivot[['variedad1'] + sorted([col for col in df_pivot.columns if col != 'variedad1'])]

    # Identificar las columnas de año, ordenadas de mayor a menor
    #anios = sorted([col for col in df_pivot.columns if col != 'pais'])
    anios = sorted([col for col in df_pivot.columns if col != 'variedad1'])
        
    # Calcular el cambio porcentual entre años (sobre las columnas)
    df_pct = df_pivot[anios].pct_change(axis=1)
    df_pct = df_pct.round(4).fillna(0)  # Redondear y reemplazar NaN por 0

    # Renombrar columnas de porcentaje
    df_pct.columns = [f"{col}_Δ%" for col in df_pct.columns]

    # Insertar las columnas de diferencia al lado de cada año
    #df_resultado = df_pivot[['pais']].copy()
    df_resultado = df_pivot[['variedad1']].copy()
    for año, col_delta in zip(anios, df_pct.columns):
        df_resultado[año] = df_pivot[año]
        df_resultado[col_delta] = df_pct[col_delta]

    # Ordenar columnas: primero 'provincia', luego años descendentes intercaladas con %Δ
    #columnas_ordenadas = ['pais']
    columnas_ordenadas = ['variedad1']
    for año in sorted(anios, reverse=True):
        #columnas_ordenadas.append(año)
        columnas_ordenadas.append(f"{año}_Δ%")

    df_resultado = df_resultado[columnas_ordenadas]
      
    # Ordenar filas por provincia
    #df_resultado = df_resultado.sort_values(by="pais")
    df_resultado = df_resultado.sort_values(by="variedad1")
    #st.write(df_resultado)
                
    #st.markdown("<h4 style='text-align: left;'>Superficie por Provincia y variación interanual (%)</h4>", unsafe_allow_html=True)

    # Obtener columnas de porcentaje
    cols_pct = [col for col in df_resultado.columns if col.endswith('_Δ%')]
    st.write(df_resultado)
    melted_df = df_resultado.melt(id_vars=['variedad1'], 
                    var_name='anio', value_name='litros')
    melted_df = melted_df[melted_df['litros'] != 0 ]
    st.write(melted_df)
    input_color = 'blue'
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    heatmap = alt.Chart(melted_df).mark_rect().encode(
            y=alt.Y(f'{'anio'}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{'variedad1'}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({'litros'}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=selected_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    st.altair_chart(heatmap, use_container_width=True)
        
    # Columnas normalizadas que se usarán solo para aplicar color
    cols_norm = [f"{col}_norm" for col in cols_pct]

    # Obtener todos los valores de % en una sola serie plana, sin NaN
    valores_pct = df_resultado[cols_pct].values.flatten()
    valores_pct = valores_pct[~np.isnan(valores_pct)]

    # Calcular el máximo valor absoluto para normalizar de -max_abs a max_abs
    max_abs = np.abs(valores_pct).max()

    # Crear un valor de recorte más representativo
    max_abs_visible = 10  # o 75, o 50 según el contraste deseado
    vmax_visible = np.percentile(np.abs(df_resultado[cols_pct].values), 95)

    # Recalcular normalización y colores
    norma = TwoSlopeNorm(vmin=-vmax_visible, vcenter=0, vmax=vmax_visible)

    # Crear columnas normalizadas con vmax_visible
    for col in cols_pct:
        col_norm = f"{col}_norm"
        df_resultado[col_norm] = (
            df_resultado[col]
            .clip(-vmax_visible, vmax_visible)
            .astype(float) / vmax_visible
        )

    # Crear colormap divergente: rojo - gris - verde
    colors = ['#b2182b', '#e6e6e6', '#4d9221']
    cmap = LinearSegmentedColormap.from_list("custom_red_gray_green", colors)
    #st.write(df_resultado[cols_pct].describe())
    #st.write(df_resultado)

    #Convierte valor entre -1 y 1 en un color HEX
    def valor_a_color(valor_norm):
        try:
            val = float(valor_norm)
            if np.isnan(val):
                return "#ffffff"
            return to_hex(cmap(norma(val)))
        except Exception:
            return "#ffffff"

    tabla_provincia = GT(data=df_resultado)

    for row_idx in range(len(df_resultado)):
        for col in cols_pct:
            col_norm = f"{col}_norm"
            valor_norm = df_resultado.loc[row_idx, col_norm]
            #st.write("row_idx", row_idx,  "valor_norm", valor_norm, "col_norm", col_norm)
            color_hex = valor_a_color(valor_norm)
            tabla_provincia = tabla_provincia.tab_style(
                style=style.fill(color=color_hex),
                 locations=gt_loc.body(columns=[col], rows=[row_idx])
            )

    # Configurar formato y estilos
    gt_tbl = tabla_provincia \
        .tab_header(
            title="*Superficie por Provincia*",
            subtitle="Evolución anual y variaciones porcentuales"
        ) \
        .cols_label(provincia="Provincia") \
        .fmt_number(columns=anios, decimals=2) \
        .fmt_percent(columns=cols_pct, decimals=2) \
        .cols_hide(columns=cols_norm) \
        .tab_source_note(
            md(
                '<br><div style="text-align: left;">'
                "*Source*: Observatorio Vitinicola Argentino" 
                " <br>All zones are publicly available on the Carbon intensity and emission factors tab via Google docs link<br>"
                "</div>"
                "<br>"
                )
            ) \
        .tab_options(
            source_notes_font_size='x-small',
            source_notes_padding=3,
            table_font_names=["Roboto", "sans-serif"],
            data_row_padding='1px',
            source_notes_background_color='#ea1c22',
            column_labels_background_color='#666666',
            data_row_padding_horizontal=3,
            column_labels_padding_horizontal=58
            ) \
        .tab_style(
            style=style.fill("#e6e6e6"),
            locations=gt_loc.body(columns=[
                '2024','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011',
                                '2010','2009','2008','2007','2006','2005','2004','2003','2002'
            ])
        ) \
        .cols_align(align='center') \
        .cols_align(align='left', columns=['provincia']) \
        .tab_style(
            style=style.fill(color="#909090"),
            locations=gt_loc.body(columns=["provincia"])
        )
    html_output = gt_tbl.repr_html()

    html_wrapped = f"""
    <div style="text-align: center; margin-bottom: 1em;">
        <h2 style="margin-bottom: 0.2em;">Superficie por Provincia</h2>
        <div style="width: 60px; height: 4px; background-color: red; margin: 0 auto 0.5em auto;"></div>
        <p><em>Evolución anual y variaciones porcentuales</em></p>
    </div>
    <div style="overflow-x: auto; overflow-y: auto; width: 100%; white-space: nowrap;">
        {html_output}
    </div>
    """

    st.components.v1.html(html_wrapped, height=1000, scrolling=False)

