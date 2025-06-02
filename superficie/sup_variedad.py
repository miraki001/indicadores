import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
import folium
from streamlit_folium import st_folium
import altair as alt
import plotly.express as px

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
    df = dv1.groupby(['provincia','variedad'], as_index=False)[['sup']].sum()    
    df = df.reset_index().rename_axis(None, axis=1) 
    
    options = {
        "title": {"text": "堆叠区域图"},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "legend": {"data": df['provincia'].tolist()},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": [
            {
                "type": "category",
                "boundaryGap": False,
                "data": df['variedad'].tolist(),
            }
        ],
        "yAxis": [{"type": "value"}],
        "series": [
            {
                "name": "邮件营销",
                "type": "line",
                "stack": "总量",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['sup'].tolist(),
            },
            {
                "name": "联盟广告",
                "type": "line",
                "stack": "总量",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df['provincia'].tolist(),
            },
            {
                "name": "视频广告",
                "type": "line",
                "stack": "总量",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [150, 232, 201, 154, 190, 330, 410],
            },
            {
                "name": "直接访问",
                "type": "line",
                "stack": "总量",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [320, 332, 301, 334, 390, 330, 320],
            },
            {
                "name": "搜索引擎",
                "type": "line",
                "stack": "总量",
                "label": {"show": True, "position": "top"},
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
            },
     ],
    }
    st_echarts(options=options, height="400px")
 
    dfm = df[df['provincia'] =='Mendoza']
    dfs = df[df['provincia'] =='San Juan']
    chart_data = df
    st.scatter_chart(
        chart_data,
        x="provincia",
        y="sup",
        color="variedad",
        size="sup",
    )
    source = df

    chart = alt.Chart(source).mark_circle().encode(
        alt.X('provincia', scale=alt.Scale(zero=False)),
        alt.Y('sup', scale=alt.Scale(zero=False, padding=1)),
        color='variedad',
        size='sup'
    )
    st.altair_chart(chart, theme="streamlit", use_container_width= True)
    chart = alt.Chart(source).mark_circle().encode(
        x='variedad',
        y='provincia',
        color='variedad',
        size='sup'
    )
    st.altair_chart(chart, theme="streamlit", use_container_width= True)
    fig = px.scatter(df, x="sup", y="provincia",
	         size="sup", color="variedad",
                 hover_name="provincia", log_x=True, size_max=200)
    #fig.show()
    fig.update_traces(marker_size=40)	
    event = st.plotly_chart(fig, key="iris")
