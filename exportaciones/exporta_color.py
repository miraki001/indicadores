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

def exporta_color():

    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"

    def append_row(df, row):
        return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)
        
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
    
    #st.markdown(" <style>iframe{ height: 400px !important } ", unsafe_allow_html=True)
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
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto  from exportaciones2_m  where producto not in ('Mosto','Alcohol');"
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
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob,variedad1,tipo_envase,color,pais,producto
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
                año = st.multiselect("Año2",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad2",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envase2",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")

    df_filtered = dv1.copy()

    if año:
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)

    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad1'].isin(variedad)]
            st.write(variedad)
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipo_envase'].isin(envase)]

    df_anual = df_filtered.groupby(['color'], as_index=False)[['fob', 'litros']].sum()
    dv = df_anual.copy()
    total = []
    tot1 = []
    tot2 = []
    totlitros = df_anual['litros'].sum()
    totfob = df_anual['fob'].sum()
    for index in range(len(df_anual)):
        #if index > 0:
            total.append((  (df_anual['litros'].loc[index] / totlitros ) *100 ))
            tot1.append((  (df_anual['fob'].loc[index] / totfob *100 )))
            tot2.append((  (df_anual['fob'].loc[index] / df_anual['litros'].loc[index]) )    )
    df_anual = df_anual.sort_index(axis = 1)
    df_anual = df_anual.rename(columns={'litros': "Litros", 'fob': "Fob",})
    df_anual['Part. % Litros'] = total
    df_anual['Part % Fob'] = tot1
    df_anual['Prec x Litro'] = tot2

    
    df_sorted = df_anual.sort_values(by='Fob', ascending=False)


#    styled_df = df_sorted.style.applymap(bgcolor_positive_or_negative, subset=['anio','anio']).format(
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
                'color': st.column_config.Column('color'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litro': st.column_config.Column('Part. % Litro'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                width = 800,   
                height = 200,
                hide_index=True)

    #st.dataframe(styled_df)
    #dv.drop('fob', axis=1, inplace=True)
    dv = dv.rename(columns={'litros': "value", 'color': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.subheader('Exportaciones por color en Litros')
    #st.write(json_list)

    col = st.columns([0.25, 0.25], gap='small')


    with col[0]:
    
        options = {
            "color": [
                '#07ECFA',
                '#C92488',
                '#604994',
                '#dd6b66',
                '#759aa0',
                '#e69d87',
                '#8dc1a9',
                '#ea7e53',
                '#eedd78',
                '#73a373',
                '#73b9bc',
                '#7289ab',
                '#91ca8c',
                '#f49f42'
            ],
            "title": {"text": "Exportaciones por color en Litros", "subtext": "", "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
                {
                    "name": json_list,
                    "type": "pie",
                    "radius": "50%",
                    "data":json_list,
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(
            options=options,key="pie1" + str(dt.now()), height="400px",
        )
    with col[1]:

        dv = dv.rename(columns={'value': "litros", 'color': "name",})
        dv = dv.rename(columns={'fob': "value", 'color': "name",})
        json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 

        options = {
            "color": [
                '#07ECFA',
                '#C92488',
                '#604994',
                '#dd6b66',
                '#759aa0',
                '#e69d87',
                '#8dc1a9',
                '#ea7e53',
                '#eedd78',
                '#73a373',
                '#73b9bc',
                '#7289ab',
                '#91ca8c',
                '#f49f42'
            ],
            "title": {"text": "Exportaciones por color en Fob", "subtext": "", "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
                {
                    "name": json_list,
                    "type": "pie",
                    "radius": "50%",
                    "data":json_list,
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(
            options=options,key="pie2" + str(dt.now()), height="400px",
        )   

  # ahora por envase



    df_anual = df_filtered.groupby(['tipo_envase'], as_index=False)[['fob', 'litros']].sum()
    dv = df_anual.copy()
    total = []
    tot1 = []
    tot2 = []
    totlitros = df_anual['litros'].sum()
    totfob = df_anual['fob'].sum()
    
    for index in range(len(df_anual)):
        #if index > 0:
            total.append((  (df_anual['litros'].loc[index] / totlitros ) *100 ))
            tot1.append((  (df_anual['fob'].loc[index] / totfob *100 )))
            tot2.append((  (df_anual['fob'].loc[index] / df_anual['litros'].loc[index]) )    )
    df_anual = df_anual.sort_index(axis = 1)
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
                'tipo_envase': st.column_config.Column('tipo_envase'),
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
    dv = dv.rename(columns={'litros': "value", 'tipo_envase': "name",})
    json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 
    #st.subheader('Exportaciones por tipo de envase en Litros')
    #st.write(json_list)

    col1 = st.columns([0.25, 0.25], gap='small')


    with col1[0]:

        options = {
            "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
                '#759aa0',
                '#e69d87',
                '#8dc1a9',
                '#ea7e53',
                '#eedd78',
                '#73a373',
                '#73b9bc',
                '#7289ab',
                '#91ca8c',
                '#f49f42'
            ],
            "title": {"text": "exportacion por tipo de envase en Litros", "subtext": "", "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
                {
                    "name": json_list,
                    "type": "pie",
                    "radius": "50%",
                    "data":json_list,
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(
            options=options,key="pie3" + str(dt.now()), height="400px",
        )
    with col1[1]:    
        dv = dv.rename(columns={'value': "litros", 'tipo_envase': "name",})
        dv = dv.rename(columns={'fob': "value", 'tipo_envase': "name",})
        json_list = json.loads(json.dumps(list(dv.T.to_dict().values()))) 

        options = {
            "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
                '#759aa0',
                '#e69d87',
                '#8dc1a9',
                '#ea7e53',
                '#eedd78',
                '#73a373',
                '#73b9bc',
                '#7289ab',
                '#91ca8c',
                '#f49f42'
            ],
            "title": {"text": "exportacion por tipo de envase en Fob", "subtext": "", "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left",},
            "series": [
                {
                    "name": json_list,
                    "type": "pie",
                    "radius": "50%",
                    "data":json_list,
                    "label": {"show": False, "position": "center"},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(
            options=options,key="pie4" + str(dt.now()), height="400px",
        )   
    #st.write(dv1)    
    producto1 = dv1.pivot_table(
          index=["tipo_envase","producto"], 
          #columns='producto',  
          values=['fob','litros'],
          aggfunc=np.sum,
          #margins=True,
          #margins_name='Totales',
    )
    producto1 = producto1.reset_index()

    
    envase2 = producto1['tipo_envase'].unique()
    for envase in envase2:
        data = producto1[producto1['tipo_envase'] == envase]
        totlts = data['litros'].sum()
        totfob = data['fob'].sum()

        new_row = pd.Series({'fob': totfob, 'tipo_envase': envase, 'producto': '_Sub-Total','litros': totlts, 'index' : len(producto1)})
        producto1 = append_row(producto1, new_row)         
        #category_pivot = data.pivot_table(index=['tipo_envase', 'producto'], values=['fob','litros'], aggfunc='sum', margins=True, margins_name='Subtotal')

        #producto1 = pd.concat([producto1, category_pivot])
    #producto1 = producto1.reset_index().rename_axis(None, axis=1)
    #producto1.columns = producto1.columns.droplevel(1)
    #producto1 = producto1.reset_index()
    #producto1.loc[len(producto1)] = ['Grand Total', '', producto1[producto1['tipo_envase'] != 'Subtotal']['fob'].sum()]

    producto1 = producto1.sort_values(by='tipo_envase', ascending=False)
    producto1 = producto1.reset_index()
    #st.dataframe(producto1)


    total = []
    tot1 = []
    tot2 = []
    totlitros = producto1['litros'].sum()
    totfob = producto1['fob'].sum()
    for index in range(len(producto1)):
        #if index > 0:
            total.append((  (producto1['litros'].loc[index] / totlitros ) *100 ))
            tot1.append((  (producto1['fob'].loc[index] / totfob *100 )))
            tot2.append((  (producto1['fob'].loc[index] / producto1['litros'].loc[index]) )    )
    producto1 = producto1.sort_index(axis = 1)
    producto1 = producto1.rename(columns={'litros': "Litros", 'fob': "Fob",})
    producto1['Part. % Litros'] = total
    producto1['Part % Fob'] = tot1
    producto1['Prec x Litro'] = tot2
    producto1 = producto1.sort_values(by='tipo_envase', ascending=False)
    styled_df = producto1.style.format(
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
                'tipo_envase': st.column_config.Column('tipo_envase'),
                'producto': st.column_config.Column('producto'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Part. % Litros': st.column_config.Column('Part. % Litros'),
                'Part % Fob': st.column_config.Column('Part % Fob'),
                'Prec x Litro': st.column_config.Column('Prec x Litr'),
        
                },
                column_order=[
                  "tipo_envase",
                  "producto",
                  "Fob",
                  "Part % Fob",
                  "Litros",
                  "Part. % Litros",
                  "Prec x Litro"
                ],
                width = 800,   
                height = 200,
                hide_index=True)
    #st.write(pd.pivot_table(producto1, values=['fob','litros'], index=["tipo_envase","producto"],observed=True,aggfunc="sum"))
