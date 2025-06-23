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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime as dt



def exporta_evolucion():

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

   
    
    
    #st.markdown(" <style>iframe{ height: 500px !important } ", unsafe_allow_html=True)

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


    actual = dt.now().year -10 
    df_anios = pd.read_parquet("data/processed/expo_anios.parquet", engine="pyarrow")
    #st.write(df_anios)
    year_list = df_anios["anio"].to_numpy()
    dv22 = df_anios[df_anios['anio'] > actual ]
    year_filter = dv22["anio"].to_numpy()
    #st.write(dv22)
    #year_list = np.append("Todos",envase_list)

    #year_list = np.append("Todos",year_list)
    #year_list = df_anios["anio"].to_numpy()
    if "filtrosee" not in st.session_state:
        st.session_state.filtrosee = {
            "anio": "Todos",
            "var": "Todas",
            "envase": "Todos",
            "color": "Todos",
            "producto": "Todos",
            "Pais": "Todos",
        }

    st.html(
        '''
            <style>
                div[data-testid="stPopover"]>div>button {
                    min-height: 32.4px;
                    height: 32.4px;
                    background-color: #A9F8FA !important;
                    color: black;
                }
            </style>
        '''
    )

    actual = dt.now().year -4 

    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob, 1 as ppl
        ,variedad1 as variedad,tipo_envase as envase,color,producto,pais
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
    """

    QUERY_V2 = f"""
        SELECT anio, mes,mes ||' '|| mess as mes1, cantlitros AS litros, valorfobsolo AS fob, 1 as ppl 
        ,variedad1 as variedad,tipo_envase as envase,color,producto,pais
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
        and anio > {actual}
    """

    # Dataframe de datos filtrados

    dv1 = cargar_datos(QUERY_V1)
    dv2 = cargar_datos(QUERY_V2)

    df_filtered = dv1.copy() 


    with st.container(border=True):
        col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año",    year_list, default=year_filter,label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
        # Columna 2: Filtro para Países
        with col2:
            with st.popover("Variedad"):
                st.caption("Selecciona uno o más Variedades de la lista")
                variedad = st.multiselect("Variedad34",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
        with col3:
            with st.popover("Envase"):
                st.caption("Selecciona uno o más Envases de la lista")
                envase = st.multiselect("Envaseee",  ["Todos"] + envase_list, default=["Todos"],label_visibility="collapsed")
        with col4:
            with st.popover("Producto"):
                st.caption("Selecciona uno o más Productos de la lista")
                producto = st.multiselect("Productoeo",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed")                

        with col5:
            with st.popover("Color"):
                st.caption("Selecciona uno o más Colores de la lista")
                color = st.multiselect("Coloreo",  ["Todos"] + color_list, default=["Todos"],label_visibility="collapsed")                
        with col6:
            with st.popover("Pais"):
                st.caption("Selecciona uno o más Paisesde la lista")
                pais = st.multiselect("Pais",  ["Todos"] + pais_list, default=["Todos"],label_visibility="collapsed")  
                pais = [str(a) for a in pais]
                st.write(pais)



    
    df_filtered = dv1.copy()    
    df_filtered['anio'] = df_filtered['anio'].astype(str)
    Filtro = 'Filtro = Año = '
    
    if año:
        if año[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)
        dv2 = dv2[dv2['anio'] > actual ]
        #data = producto1[producto1['tipo_envase'] == envase]
        Filtro = Filtro + str(año) + ' '

    if variedad:
        if variedad[0] != 'Todas':
            df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
            dv2 = dv2[dv2['variedad'].isin(variedad)]
        Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
    if envase:
        if envase[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['tipo_envase'].isin(envase)]
            dv2 = dv2[dv2['tipo_envase'].isin(envase)]
        Filtro = Filtro + ' Envase = ' +  str(envase) + ' '              
    if color:
        if color[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['color'].isin(color)]          
            dv2 = dv2[dv2['color'].isin(color)]       
        Filtro = Filtro + ' Color = ' +  str(color) + ' '              
    if pais:
        if pais[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['pais'].isin(pais)]               
            dv2 = dv2[dv2['pais'].isin(pais)]
        Filtro = Filtro + ' Paises  = ' +  str(pais) + ' '                   
    if producto:
        if producto[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['producto'].isin(producto)]     
            dv2 = dv2[dv2['producto'].isin(producto)]
        Filtro = Filtro + ' Producto  = ' +  str(producto) + ' '       
    

   

    dv2 = dv2.astype({'fob' : int, 'litros': int} )

    litros = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['litros'],
          aggfunc='sum'
    )

    litros.columns = litros.columns.droplevel(0)
    litros = litros.reset_index().rename_axis(None, axis=1)

    fob = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['fob'],
          aggfunc='sum'
    )
    
    
    ppl = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['ppl'],
          aggfunc='sum'
    )

    litros = litros.reset_index().rename_axis(None, axis=1)
    fob.columns = fob.columns.droplevel(0)
    fob = fob.reset_index().rename_axis(None, axis=1)
    ppl.columns = ppl.columns.droplevel(0)
    ppl = ppl.reset_index().rename_axis(None, axis=1)
    fob  = fob.fillna(0)
    litros  = litros.fillna(0)
    anio1 = litros.columns[2]
    anio2 = litros.columns[3]
    anio3 = litros.columns[4]
    anio4 = litros.columns[5]


    for index in range(len(ppl)):
        ppl[anio1].loc[index] = fob[anio1].loc[index] / litros[anio1].loc[index]  
        ppl[anio2].loc[index] = fob[anio2].loc[index] / litros[anio2].loc[index]  
        ppl[anio3].loc[index] = fob[anio3].loc[index] / litros[anio3].loc[index]  
        ppl[anio4].loc[index] = fob[anio4].loc[index] / litros[anio4].loc[index]  

    ppl  = ppl.fillna('')

    tot1 = []
    tot2 = []
    tot3 = []
    tot4 = []
    acu1 = 0
    acu2 = 0
    acu3 = 0
    acu4 = 0
    
    for index in range(len(litros)):
          if index == 0:
              tot1.append((  (litros[anio1].loc[index])))
              tot2.append((  (litros[anio2].loc[index])))
              tot3.append((  (litros[anio3].loc[index])))
              tot4.append((  (litros[anio4].loc[index])))
              acu1 = litros[anio1].loc[index]
              acu2 = litros[anio2].loc[index]
              acu3 = litros[anio3].loc[index]
              acu4 = litros[anio4].loc[index]
          if index > 0:
            tot1.append((  (litros[anio1].loc[index] + acu1 ) ))
            tot2.append((  (litros[anio2].loc[index] + acu2 )))
            tot3.append((  (litros[anio3].loc[index] + acu3 ) ))
            tot4.append((  (litros[anio4].loc[index] + acu4 )))
            acu1 = acu1 + litros[anio1].loc[index]
            acu2 = acu2 + litros[anio2].loc[index]
            acu3 = acu3 + litros[anio3].loc[index]
            acu4 = acu4 + litros[anio4].loc[index]
              
    litros['Acum ' + str(anio1) ] = tot1
    litros['Acum ' + str(anio2)] = tot2
    litros['Acum ' + str(anio3) ] = tot3
    litros['Acum ' + str(anio4)] = tot4
    desc1 = litros.columns[6]
    desc2 = litros.columns[7]
    desc3 = litros.columns[8]
    desc4 = litros.columns[9]        

    # ahora en Fob


    tot1 = []
    tot2 = []
    tot3 = []
    tot4 = []
    acu1 = 0
    acu2 = 0
    acu3 = 0
    acu4 = 0
    
    for index in range(len(fob)):
          if index == 0:
              tot1.append((  (fob[anio1].loc[index])))
              tot2.append((  (fob[anio2].loc[index])))
              tot3.append((  (fob[anio3].loc[index])))
              tot4.append((  (fob[anio4].loc[index])))
              acu1 = fob[anio1].loc[index]
              acu2 = fob[anio2].loc[index]
              acu3 = fob[anio3].loc[index]
              acu4 = fob[anio4].loc[index]
          if index > 0:
            tot1.append((  (fob[anio1].loc[index] + acu1 ) ))
            tot2.append((  (fob[anio2].loc[index] + acu2 )))
            tot3.append((  (fob[anio3].loc[index] + acu3 ) ))
            tot4.append((  (fob[anio4].loc[index] + acu4 )))
            acu1 = acu1 + fob[anio1].loc[index]
            acu2 = acu2 + fob[anio2].loc[index]
            acu3 = acu3 + fob[anio3].loc[index]
            acu4 = acu4 + fob[anio4].loc[index]
              
    fob['Acum ' + str(anio1) ] = tot1
    fob['Acum ' + str(anio2)] = tot2
    fob['Acum ' + str(anio3) ] = tot3
    fob['Acum ' + str(anio4)] = tot4    

    dv1 = df_filtered.groupby(['anio'], as_index=False)[['fob', 'litros','ppl']].sum()
    
    actual = dt.now().year -4 


    if dv1.empty:
        st.warning("No se encontraron resultados con los filtros seleccionados.")
    else:
        # Tabla
        st.subheader("Exportaciones")
        for index in range(len(dv1)):
             dv1['ppl'].loc[index] = dv1['fob'].loc[index] / dv1['litros'].loc[index]  

        
        total = []
        tot1 = []
        tot2 = []
        total.append(0)
        tot1.append(0)
        tot2.append(0)
        for index in range(len(dv1)):
          if index > 0:
            total.append((  (dv1['litros'].loc[index] / dv1['litros'].loc[index -1]) -1 ) *100 )
            tot1.append((  (dv1['fob'].loc[index] / dv1['fob'].loc[index -1]) -1 ) *100 )
            tot2.append((  (dv1['ppl'].loc[index] / dv1['ppl'].loc[index -1]) -1 ) *100     )
            #tot2.append((  ( ppl.loc[index] / pp.loc[index -1]) -1 ) *100     )
        dv1 = dv1.rename(columns={'litros': "Litros", 'fob': "Fob",'anio': "Año","ppl": 'ppl'})
        dv1['Litros Var %'] = total
        dv1['Fob Var. %'] = tot1
        dv1['Prec x Litro Var. %'] = tot2
        dv1 = dv1.astype({'Fob' : int, 'Litros': int} )

        dv1 = dv1.sort_index(axis = 1)
        dv1 = dv1.rename(columns={'ppl': "Prec x Litro"})

        styled_df = dv1.style.applymap(bgcolor_positive_or_negative, subset=['Litros Var %','Fob Var. %','Prec x Litro Var. %']).format(
            {"Litros": lambda x : '{:,.0f}'.format(x), 
            "Fob": lambda x : '{:,.0f}'.format(x),
            "Prec x Litro": lambda x : '{:,.2f}'.format(x),
            "Litros Var %": lambda x : '{:,.2f} %'.format(x),
            "Fob Var. %": lambda x : '{:,.2f} %'.format(x),
            "Prec x Litro Var. %": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
        )


        if st.checkbox('Ver datos en forma de tabla'):
            column_orders =("Año", "Litros", "Litros Var %","Fob","Fob Var. %","Prec x Litro","Prec x Litro Var. %" )            
            st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Litros Var %': st.column_config.Column('Litros Var %'),
                'Fob Var. %': st.column_config.Column('Fob Var. %'),
                'Prec x Litro': st.column_config.Column('Prec x Litro'),
                'Prec x Litro Var. %': st.column_config.Column('Prec x Litro Var. %'),
        
                },
                column_order = column_orders, 
                width = 1000,   
                height = 800,
                hide_index=True)

  

        # Convertir 'anio' a string para el gráfico
        dv1["Año"] = dv1["Año"].astype(str)
        placeholder = st.empty()
        # Crear gráfico de líneas y barras
        st.caption(Filtro)

        option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "title": {
                "text": 'Exportaciones Evolución ',
                "subtext": '',
            },              
            "legend": {},
            "xAxis": {"type": "category", "data": dv1["Año"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Litros/Fob" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,
                {"type": "value" , "name" : "",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,
                 "axisLine": {
                    "show": 'false',
                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },
                {"type": "value" , "name" : "Precio x Lts",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    "formatter": '{value} u$s '
                      }
                },            
            ],
            "series": [                
                {"top": 55,
                "data": dv1["Litros"].tolist(),"position" : 'rigth', "type": "line", "name": "Litros", "yAxisIndex": 1, },
                {"data": dv1["Fob"].tolist(), "type": "bar", "name": "Fob", "yAxisIndex": 1, },
                {"data": dv1["ppl"].tolist(), "type": "line", "name": "Precio x Lts", "yAxisIndex": 2, "color":'#07ECFA', },
            ],
        }

        st_echarts(options=option,key="gauge" + str(dt.now()), height="400px")



        st.write('nuevo')
        df2 = dv2.groupby(['anio','mes1'], as_index=False)[['litros']].sum()
        #dv2 = dv2[dv2['anio'] > actual ] 
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])  
        for y in df2.anio.unique():
            dfy = df2[df2.anio == y]
            dfy["litro"] = dfy["litros"].astype(str)

            fig.add_trace(
              go.Scatter(x=dfy.mes1, y=dfy.litros.cumsum(), name=str(y), mode="lines",text='Acumulados'),
              secondary_y=True
            )    

            fig.add_bar(x = dfy.mes1,  y = dfy.litros,name = str(y) )

        fig.show()
        st.plotly_chart(fig, theme="streamlit")

        #st.subheader("Exportaciones evolución mensual en litros")
       
        litros["mes"] = litros["mes"].astype(str)
        st.caption(Filtro)



        # Crear gráfico de líneas y barras
        option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "title": {
                "text": 'Exportaciones evolución mensual en litro ',
                "textStyle": {
                        "fontSize": 14,
                },                  
                "subtext": '',
            },            
            "xAxis": {"type": "category", "data": litros["mes"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Litros" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,
                {"type": "value" , "name" : "",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,
                 "axisLine": {
                    "show": 'false',
                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },
                {"type": "value" , "name" : "Litros Acum",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                },            
            ],            
            #"yAxis": {"type": "value"},
            "series": [
                {"data": litros[anio1].tolist(), "type": "bar", "name": anio1,"yAxisIndex": 1, "color":'#FCE2D6'  },
                {"data": litros[anio2].tolist(), "type": "bar", "name": anio2,"yAxisIndex": 1,  "color":'#F9C8B4' },
                {"data": litros[anio3].tolist(), "type": "bar", "name": anio3, "color":'#07ECFA',"yAxisIndex": 1, "color":'#F49F82'  },
                {"data": litros[anio4].tolist(), "type": "bar", "name": anio4, "color":'#C92488',"yAxisIndex": 1,  "color":'#EC654A' },
                {"data": litros[desc1].tolist(), "type": "line", "name": desc1, "yAxisIndex": 2,  "color":'#C92488'},
                {"data": litros[desc2].tolist(), "type": "line", "name": desc2,"yAxisIndex": 2,  "color":'#C92488'},
                {"data": litros[desc3].tolist(), "type": "line", "name": desc3, "color":'#07ECFA', "yAxisIndex": 2, },
                {"data": litros[desc4].tolist(), "type": "line", "name": desc4, "color":'#604994', "yAxisIndex": 2,},
                
            ],
        }

        st_echarts(options=option,key="otro" + str(dt.now()), height="400px")

        if st.checkbox('Ver tabla Evolución mensual en litros'):
            st.dataframe(litros,
                width = 600,   
                height = 800,
                hide_index=True)

        #st.subheader("Exportaciones evolución mensual en Fob")
   
        #fob["mes"] = fob["mes"].astype(str)
        anio1 = fob.columns[1]
        #st.write(fob.columns[1])
        anio2 = fob.columns[2]
        anio3 = fob.columns[3]
        anio4 = fob.columns[4]
        st.caption(Filtro)

        # Crear gráfico de líneas y barras
        option = {
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "title": [
                {
                "text": 'Exportaciones evolución mensual en Fob',
                "textStyle": {
                        "fontSize": 14,
                },                    
                "subtext": '',
                }, 
                {
                    "title": 'otro abajo',
                    "textStyle": {
                        "fontSize": 10,
                        },
                    "left": '20%',
                    "top": '50%',
                },
            ],
            "xAxis": {"type": "category", "data": litros["mes"].tolist(),
                    "splitArea": {
                        "show": 'true',
                    },
                     },
            #"yAxis": {"type": "value"},
            "yAxis": [
                {"type": "value" ,"name" : "Fob" ,
                 "axisLine": {
                    "show": 'false',
                  },              
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                } ,
                {"type": "value" , "name" : "",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,
                 "axisLine": {
                    "show": 'false',
                  },             
                 "axisLabel": {
                    "formatter": '{value}  '
                      }
                },
                {"type": "value" , "name" : "Fob Acum",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    "formatter": '{value} '
                      }
                },            
            ],            
            
            "series": [
                {"data": fob[anio1].tolist(), "type": "bar", "name": anio1,"yAxisIndex": 1, "color":'#FCE2D6'  },
                {"data": fob[anio2].tolist(), "type": "bar", "name": anio2,"yAxisIndex": 1,  "color":'#F9C8B4' },
                {"data": fob[anio3].tolist(), "type": "bar", "name": anio3, "color":'#07ECFA',"yAxisIndex": 1, "color":'#F49F82'  },
                {"data": fob[anio4].tolist(), "type": "bar", "name": anio4, "color":'#C92488',"yAxisIndex": 1,  "color":'#EC654A' },
                {"data": fob[desc1].tolist(), "type": "line", "name": desc1, "yAxisIndex": 2,  "color":'#C92488'},
                {"data": fob[desc2].tolist(), "type": "line", "name": desc2,"yAxisIndex": 2,  "color":'#C92488'},
                {"data": fob[desc3].tolist(), "type": "line", "name": desc3, "color":'#07ECFA', "yAxisIndex": 2, },
                {"data": fob[desc4].tolist(), "type": "line", "name": desc4, "color":'#604994', "yAxisIndex": 2,},
            ],
        }

        st_echarts(options=option,key="otro1" + str(dt.now()), height="400px")

        
        if st.checkbox('Ver tabla Evolución mensual en Fob'):
            st.dataframe(fob,
                width = 600,   
                height = 800,
                hide_index=True)

        #st.subheader("Exportaciones evolución precio promedio por litro ")
   
        #ppl["mes"] = ppl["mes"].astype(str)
        anio1 = ppl.columns[1]
        #st.write(fob.columns[1])
        anio2 = ppl.columns[2]
        anio3 = ppl.columns[3]
        anio4 = ppl.columns[4]
        st.caption(Filtro)


        # Crear gráfico de líneas y barras
        option = {
            "title": [
                {
                "text": 'Exportaciones evolución precio promedio por litro ',
                "textStyle": {
                        "fontSize": 14,
                },                    
                "subtext": '',
                }, 
                {
                    "title": 'otro abajo',
                    "textStyle": {
                        "fontSize": 10,
                        },
                    "left": '20%',
                    "top": '50%',
                },
            ],            
          "color": [
                '#332D75',
                '#1E8DB6',
                '#604994',
                '#dd6b66',
            ],
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
            "legend": {},
            "xAxis": {"type": "category", "data": litros["mes"].tolist()},
            "yAxis": {"type": "value"},
            "series": [
                {"data": ppl[anio1].tolist(), "type": "line", "name": anio1, },
                {"data": ppl[anio2].tolist(), "type": "line", "name": anio2,},
                {"data": ppl[anio3].tolist(), "type": "line", "name": anio3, "color":'#07ECFA', },
                {"data": ppl[anio4].tolist(), "type": "line", "name": anio4, "color":'#C92488', },
            ],
        }

        st_echarts(options=option,key="otro2" + str(dt.now()), height="400px")

        if st.checkbox('Ver tabla Evolución mensual en precio por litro'):
            st.dataframe(ppl,
                width = 600,   
                height = 800,
                hide_index=True)
