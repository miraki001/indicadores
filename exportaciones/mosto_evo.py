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



def exporta_mosto_evo():

    def formato(value):
        return int(float(value))/1000000

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

    #st.markdown(" <style>iframe{ height: 300px !important } ", unsafe_allow_html=True)

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
    QUERY_INICIAL = "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais  from exportaciones2_m  where producto = 'Mosto' and codigoproducto like '%CONCENTRADO%'  ;"
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
    if "filtrosme" not in st.session_state:
        st.session_state.filtrosme = {
            "anio": "Todos",
            "var": "Todas",
            "envase": "Todos",
            "color": "Todos",
            "producto": "Todos"
        }



    QUERY_V1 = f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob, 1 AS ppl,pais
        FROM exportaciones2_m 
        WHERE producto = 'Mosto'
        and codigoproducto like '%CONCENTRADO%' 

    """
    actual = dt.now().year -4 

    QUERY_V2 = f"""
        SELECT anio, mes, cantlitros AS litros, valorfobsolo AS fob,1 AS ppl,pais
        FROM exportaciones2_m 
        WHERE  producto in ('Mosto')
        and codigoproducto like '%CONCENTRADO%' 
        and anio > {actual}

    """

    # Dataframe de datos filtrados

    dv1 = cargar_datos(QUERY_V1)
    dv2 = cargar_datos(QUERY_V2)

    with st.container(border=True):
        col1, col2 = st.columns([1, 1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
        with col1:
            with st.popover("Año"):
                st.caption("Selecciona uno o más años de la lista")
                año = st.multiselect("Año22",   ["Todos"] + year_list, default=['Todos'],label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año22:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
            
        # Columna 2: Filtro para Países             
        with col2:
            with st.popover("Pais"):
                st.caption("Selecciona uno o más Paisesde la lista")
                pais = st.multiselect("Pais22",  ["Todos"] + pais_list, default=["Todos"],label_visibility="collapsed")      



    
    df_filtered = dv1.copy()  

    Filtro = 'Filtro = Año = '
    
    if año:
        if año[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)
        dv2 = dv2[dv2['anio'] > actual ]
        #data = producto1[producto1['tipo_envase'] == envase]
        Filtro = Filtro + str(año) + ' '

           
    if pais:
        if pais[0] != 'Todos':
            df_filtered = df_filtered[df_filtered['pais'].isin(pais)]               
            dv2 = dv2[dv2['pais'].isin(pais)]
        Filtro = Filtro + ' Paises  = ' +  str(pais) + ' '                   


    
    dv2 = dv2.astype({'litros' : int, 'fob': int,'ppl' :int } )

    litros = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['litros'],
          aggfunc='sum'
    )

    fob = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['fob'],
          aggfunc='sum'
    )
    ppf = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['fob'],
          aggfunc='sum'
    )
    ppt = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['litros'],
          aggfunc='sum'
    )
    ppl = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['ppl'],
          aggfunc='sum'
    )
    
    #st.write(ppl)
    #st.write(ppf)
    #st.write(ppt)
    litros.columns = litros.columns.droplevel(0)
    
       
    litros = litros.reset_index().rename_axis(None, axis=1)
    fob.columns = fob.columns.droplevel(0)
    fob = fob.reset_index().rename_axis(None, axis=1)
    ppl.columns = ppl.columns.droplevel(0)
    ppl = ppl.reset_index().rename_axis(None, axis=1)
    ppl  = ppl.fillna('')
    fob  = fob.fillna('')
    litros  = litros.fillna('')
    #ppf.columns = ppf.columns.droplevel(0)
    #ppf = ppf.reset_index().rename_axis(None, axis=1)
    #ppf  = ppf.fillna('')    
    #ppt.columns = ppt.columns.droplevel(0)
    #ppt = ppt.reset_index().rename_axis(None, axis=1)
    #ppt  = ppt.fillna('')  
    ppt.columns = ppt.columns.droplevel(0)
    ppf.columns = ppf.columns.droplevel(0)
    #ppl.columns = ppl.columns.droplevel(0)
    ppf = ppf.reset_index().rename_axis(None, axis=1)
    ppt = ppt.reset_index().rename_axis(None, axis=1)

    actual = dt.now().year -4 
    dv1 = df_filtered.groupby(['anio'], as_index=False)[['fob', 'litros','ppl']].sum()
    for index in range(len(dv1)):
        dv1['ppl'].loc[index] = dv1['fob'].loc[index] / dv1['litros'].loc[index]  

    anio1 = ppl.columns[1]
    anio2 = ppl.columns[2]
    anio3 = ppl.columns[3]
    anio4 = ppl.columns[4]   
    st.write(anio1)
    st.write(str(anio1))

    for index in range(len(ppl)):
        ppl[anio1].loc[index] = ppf[anio1].loc[index] / ppt[anio1].loc[index]  
        
    if dv1.empty:
        st.warning("No se encontraron resultados con los filtros seleccionados.")
    else:
        # Tabla
        st.subheader("Exportaciones de Mosto")
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
        dv1 = dv1.rename(columns={'litros': "Toneladas", 'fob': "Fob",'anio': "Año","ppl": 'ppt'})
        dv1['Tn Var %'] = total
        dv1['Fob Var. %'] = tot1
        dv1['Prec x Tn Var. %'] = tot2

        dv1 = dv1.sort_index(axis = 1)

        styled_df = dv1.style.applymap(bgcolor_positive_or_negative, subset=['Tn Var %','Fob Var. %','Prec x Tn Var. %']).format(
            {"Toneladas": lambda x : '{:,.0f}'.format(x), 
            "Fob": lambda x : '{:,.0f}'.format(x),
            "ppt": lambda x : '{:,.2f}'.format(x),
            "Tn Var %": lambda x : '{:,.2f} %'.format(x),
            "Fob Var. %": lambda x : '{:,.2f} %'.format(x),
            "Prec x Tn Var. %": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
        )

        if st.checkbox('Ver datos en forma de tabla '):
            st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),
                'Toneladas': st.column_config.Column('Toneladas'),
                'Fob': st.column_config.Column('Fob'),
                'Tn Var %': st.column_config.Column('Tn Var %'),
                'Fob Var. %': st.column_config.Column('Fob Var. %'),
                'ppt': st.column_config.Column('ppt'),
                'Prec x Tn Var. %': st.column_config.Column('Prec x Tn Var. %'),
        
                },
                width = 600,   
                height = 800,
                hide_index=True)

            #st.write(dv1.describe(include=[np.number]))

  

        # Convertir 'anio' a string para el gráfico
        dv1["Año"] = dv1["Año"].astype(str)
        dv1 = dv1.astype({'Fob' : int, 'Toneladas': int,'ppt' :int } )

        placeholder = st.empty()
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
                "text": 'Exportaciones de Mosto evolución ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
            },             
            "xAxis": {"type": "category", "data": dv1["Año"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Tn." ,
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 0,                 
                 "axisLine": {
                    "show": 'False',
                  },              
                 "axisLabel": {
                    #"formatter":  '{value}'        
                    "formatter": JsCode(
                        "function(value){return (value /1000) + ' K' };"
                        ).js_code,                     
                 },  
                },
                {"type": "value" , "name" : "Fob",
                 "position" : 'left',
                 "alignTicks": 'true',
                 "offset": 60,
                 "axisLine": {
                    "show": 'True',
                  },             
                 "axisLabel": {
                    #"formatter":   '{value}',     
                    "formatter": JsCode(
                        "function(value){return (value /1000000) + ' M' };"
                        ).js_code,                     
                    #"formatter": function (a) {a == +a;  return isFinite(a) ? echarts.format.addCommas(+a / 1000000) : ''; }, 
                 },
                },
                {"type": "value" , "name" : "Precio x Tn.",
                 "position" : 'rigth',
                 "alignTicks": 'true',
                 "offset": 10,
                 "axisLine": {
                    "show": 'true',

                  },             
                 "axisLabel": {
                    #"formatter": '{value} u$s '
                    "formatter": JsCode(
                        "function(value){return (value).toFixed(0) + ' u$s' };"
                        ).js_code,                     
                      }
                },            
            ],
            "series": [
                {"data": dv1["Toneladas"].tolist(),"position" : 'rigth', "type": "line", "name": "Toneladas", "yAxisIndex": 0, },
                {"data": dv1["Fob"].tolist(), "type": "bar", "name": "Fob", "yAxisIndex": 1, "formatter": '{value} kg' },
                {"data": dv1["ppt"].tolist(), "type": "line", "name": "Precio x Tn.", "yAxisIndex": 2, "color":'#07ECFA', },
            ],
        }

        st_echarts(options=option,key="gauge444" + str(dt.now()), height="400px")

        #st.subheader("Exportaciones evolución mensual en Toneladas")
        st.caption(Filtro)
        anio1 = litros.columns[1]
        anio2 = litros.columns[2]
        anio3 = litros.columns[3]
        anio4 = litros.columns[4]

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
                "text": 'Evolución mensual en Toneladas" ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
            },              
            "xAxis": {"type": "category", "data": litros["mes"].tolist()},
            "yAxis": {"type": "value"},
            "series": [
                {"data": litros[anio1].tolist(), "type": "line", "name": anio1, },
                {"data": litros[anio2].tolist(), "type": "line", "name": anio2,},
                {"data": litros[anio3].tolist(), "type": "line", "name": anio3, "color":'#07ECFA', },
                {"data": litros[anio4].tolist(), "type": "line", "name": anio4, "color":'#C92488', },
            ],
        }

        st_echarts(options=option,key="otro" + str(dt.now()), height="400px")

        #st.subheader("Exportaciones evolución mensual en Fob")
        st.caption(Filtro)
   
        anio1 = fob.columns[1]
        anio2 = fob.columns[2]
        anio3 = fob.columns[3]
        anio4 = fob.columns[4]

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
                "text": 'Evolución mensual en Fob" ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
            },              
            
            "xAxis": {"type": "category", "data": litros["mes"].tolist()},
            "yAxis": {"type": "value"},
            "series": [
                {"data": fob[anio1].tolist(), "type": "line", "name": anio1, },
                {"data": fob[anio2].tolist(), "type": "line", "name": anio2,},
                {"data": fob[anio3].tolist(), "type": "line", "name": anio3, "color":'#07ECFA', },
                {"data": fob[anio4].tolist(), "type": "line", "name": anio4, "color":'#C92488', },
            ],
        }

        st_echarts(options=option,key="otro1" + str(dt.now()), height="400px")

        #st.subheader("Exportaciones evolución precio promedio por Tonelada ")
        st.caption(Filtro)
   
        anio1 = ppl.columns[1]
        anio2 = ppl.columns[2]
        anio3 = ppl.columns[3]
        anio4 = ppl.columns[4]

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
                "text": 'Evolución mensual en Precio por Tn." ',
                "textStyle": {
                        "fontSize": 12,
                },                  
                "subtext": '',
            },              
            
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
