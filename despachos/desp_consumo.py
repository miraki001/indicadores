import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime as dt

def despachos_consumo():


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

    QUERY_V0 = f"""
        SELECT distinct canal
        FROM scentia_res       

    """
    df_filtros = cargar_datos(QUERY_V0)
    
  # Listas de valores únicos para los filtros
    canal_list = sorted(df_filtros["canal"].dropna().unique())
    if "filtroseemv" not in st.session_state:
        st.session_state.filtrosee = {
            "canal": "Todos",
        }

    QUERY_V1 = f"""
        SELECT periodo,anio,mes,canal,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" 
        FROM scentia_res
    """    
    QUERY_V2 = f"""
        SELECT periodo,anio,mes,canal,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" 
        FROM scentia_valores
    """    

    dv1 = cargar_datos(QUERY_V1)
    df_filtered = dv1.copy() 
    #dv1['anio'] = dv1['anio'].astype(str)

    dv2 = cargar_datos(QUERY_V2)
    st.write(dv2)
    
    QUERY_V3 = f"""
        SELECT anio,mes,canal,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" 
        FROM scentia_resumen
    """  
    dv3 = cargar_datos(QUERY_V3)


    with st.container(border=True):
        col1,col2 =  st.columns([1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Canal"):
                st.caption("Selecciona uno o más Canales de la lista")
                canal = st.multiselect("Canal",  ["Todos"] + canal_list, default=["Todos"],label_visibility="collapsed",help="Selecciona uno o más Canales")
                 
    
    Filtro = 'Filtro = '    
        
    if canal:
        if canal[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['canal'].isin(canal)]
            dv2 = dv2[dv2['canal'].isin(canal)]
        Filtro = Filtro + ' Canal = ' +  str(canal) 
    
    #df_filtered = dv1.copy()
    actual = dt.now().year -4 
    #df_filtered = df_filtered[df_filtered['anio'] > actual ]   
    #df_filtered = df_filtered.groupby(['periodo'], as_index=False).sum()

    litros = df_filtered.pivot_table(
          index='periodo', 
          values=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS"],
          aggfunc='sum'
    )  
    if st.checkbox('Ver Consumo en litros en forma de tabla'):
        st.write(litros)

    #litros.columns = litros.columns.droplevel(0)
    litros = litros.reset_index().rename_axis(None, axis=1)  
    #st.write(litros['periodo'])
    litros['periodo'] = litros['periodo'].astype(str)    



    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])  
    for y in df_filtered.anio.unique():
        dfy = df_filtered[df_filtered.anio == y]
        #dfy["litro"] = dfy["litros"].astype(str)

        fig.add_trace(
          go.Scatter(x=dfy.mes, y=dfy.CERVEZAS.cumsum(), name=str(y), mode="lines",text='Acumulados'),
          secondary_y=True
        )   
        fig.add_trace(
          go.Scatter(x=dfy.mes, y=dfy.VINOS_COMUNES.cumsum(), name=str(y), mode="lines",text='Acumulados'),
          secondary_y=True
        ) 

        fig.add_bar(x = dfy.mes,  y = dfy.CERVEZAS,name = str(y) )
        fig.add_bar(x = dfy.mes,  y = dfy.VINOS_COMUNES,name = str(y) )

    fig.show()
    st.plotly_chart(fig, theme="streamlit")
    
    st.caption(Filtro)
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": litros['periodo'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": litros['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
                   ,{"data": litros['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
                   ,{"data": litros['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
                   ,{"data": litros['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
                   ,{"data": litros['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
                   ,{"data": litros['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
                   ,{"data": litros['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
                   ,{"data": litros['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
    }
    st_echarts(
        options=option, height="400px",
    )

    litros2 = dv2.pivot_table(
          index='periodo', 
          values=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS"],
          aggfunc='sum'
    )  
    if st.checkbox('Ver Consumo en Valores en forma de tabla'):
        st.write(litros2)

    #litros.columns = litros.columns.droplevel(0)
    litros2 = litros2.reset_index().rename_axis(None, axis=1)  
    #st.write(litros['periodo'])
    litros2['periodo'] = litros2['periodo'].astype(str)    
    
    st.caption(Filtro)
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
        },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": litros2['periodo'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": litros2['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
                   ,{"data": litros2['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
                   ,{"data": litros2['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
                   ,{"data": litros2['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
                   ,{"data": litros2['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
                   ,{"data": litros2['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
                   ,{"data": litros2['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
                   ,{"data": litros2['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
    }
    st_echarts(
        options=option, height="400px",
    )


    valvc = []
    valvf = []
    valc = []
    valrtd = []
    vales = []
    valap = []
    valf = []
    vals = []
    for index in range(len(litros2)):
       valvc.append(  (litros2['VINOS_COMUNES'].loc[index] / litros['VINOS_COMUNES'].loc[index ]) )
       valvf.append(  (litros2['VINOS_FINOS'].loc[index] / litros['VINOS_FINOS'].loc[index ])  )
       valc.append(  (litros2['CERVEZAS'].loc[index] / litros['CERVEZAS'].loc[index ])  )
       valrtd.append(  (litros2['APERITIVOS_RTD'].loc[index] / litros['APERITIVOS_RTD'].loc[index ])  )
       vales.append(  (litros2['ESPUMANTES'].loc[index] / litros['ESPUMANTES'].loc[index ])  )
       valap.append(  (litros2['APERITIVOS_ALC'].loc[index] / litros['APERITIVOS_ALC'].loc[index ])  )
       valf.append(  (litros2['VINOS_FORTIFICADOS'].loc[index] / litros['VINOS_FORTIFICADOS'].loc[index ])  )
       vals.append(  (litros2['SIDRAS_Y_SABORES'].loc[index] / litros['SIDRAS_Y_SABORES'].loc[index ])  )
    litros2['ppl Vinos Comunes'] = valvc
    litros2['ppl Vinos Finos'] = valvf
    litros2['ppl Cervezas'] = valc
    litros2['ppl RTD'] = valrtd
    litros2['ppl Espumantes'] = vales
    litros2['ppl Aperitivos Alc.'] = valap
    litros2['ppl Vinos Fort.'] = valf
    litros2['ppl Sidras y Sab.'] = vals
    litros2 = litros2.astype({'ppl Vinos Comunes': int} )
    litros2 = litros2.astype({'ppl Vinos Finos': int} )
    litros2 = litros2.astype({'ppl Cervezas': int})
    litros2 = litros2.astype({'ppl RTD': int})
    litros2 = litros2.astype({'ppl Espumantes': int})
    litros2 = litros2.astype({'ppl Aperitivos Alc.': int})
    litros2 = litros2.astype({'ppl Vinos Fort.': int})
    litros2 = litros2.astype({'ppl Sidras y Sab.': int})
    st.write(litros2)
    
    #pesos['VINOS_COMUNES'] = litros2['VINOS_COMUNES']/litros['VINOS_COMUNES']
    #st.write(pesos)
    
    
    dv3 = dv3.set_index(["anio","mes","canal"])
    dv3 = dv3.reset_index().rename_axis(None, axis=1)  
    #st.write(dv3)
    dv3 = dv3[dv3['anio'] == 2023 ] 
    #st.write(dv3)
    #dv3 = dv3.reset_index().rename_axis(None, axis=1)  
    #dv3 = dv3.assign(row_number=range(len(dv3)))
    #dv3 = dv3.set_index(['anio','mes','canal']) 
    

    acu1 = 0
    acu2 = 0
    acu3 = 0
    acu4 = 0
    st.write(dv1)
    dft = dv1.melt(id_vars=['anio','mes','periodo','canal'], var_name='producto', value_name='litros')
    st.write(dv2)
    fig = px.sunburst(dft, path=['anio', 'producto'], values='litros',
                      color='producto', hover_data=['anio'],
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(dft['litros'], weights=dft['litros']))
    st.plotly_chart(fig, theme="streamlit")    
    dft = dv2.melt(id_vars=['anio','mes','periodo','canal'], var_name='producto', value_name='valores')
    st.write(dft)    
    st.write(
        """
             Scentia releva información sobre venta en volumen y facturación de vinos fraccionados en hipermercados, supermercados, autoservicios, drugstore y kioscos de todo el país. Su muestra equivale aproximadamente al 40% del total de despachos de vino en volumen al mercado interno de la Argentina.
        
    """)
