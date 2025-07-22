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
from streamlit_echarts import Map
from st_keyup import st_keyup
from util import desp_prov
from datetime import datetime as dt
from despachos import desp_prov
from despachos import desp_color
from despachos import desp_envase
from despachos import desp_variedad
from despachos import desp_consumo
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

st.set_page_config(initial_sidebar_state="collapsed",
                  layout="wide",menu_items=None)


conn = st.connection("postgresql", type="sql")

def bgcolor_positive_or_negative(value):
    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

def _format_with_thousands_commas(val): 
  return f'{val:.,0f}' 

def _format_as_percentage(val, prec=0): 
  return f'{val:.{prec}%}' 

def imprimir1():
    print
  
def imprimir():  
    show_print_button = """
          <script>
            function print_page(obj) {
                obj.style.display = "none";
                parent.window.print();
            }
          </script>
    """
    components.html(show_print_button) 

@st.cache_data
def cargar_datos(consulta):
    try:
        df = conn.query(consulta, ttl="0")
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()


QUERY_V0 = f"""
        SELECT distinct anio,variedad1 as variedad,provincia,departamento,producto,subgrupoenvase
        FROM despachos_m 
        where producto not in ('Mosto','Alcohol')
        

"""

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


df_filtros = cargar_datos(QUERY_V0)

if df_filtros.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()

QUERY_V1 = f"""
        SELECT anio,mes, cantidadlitros AS litros,variedad1 as variedad,provincia,departamento,producto,color,subgrupoenvase
        FROM despachos_m 
        WHERE producto not in ('Mosto','Alcohol')
"""

    # Listas de valores únicos para los filtros
year_list = sorted(df_filtros["anio"].dropna().unique(), reverse=True)

var_list = sorted(df_filtros["variedad"].dropna().unique())
prov_list = sorted(df_filtros["provincia"].dropna().unique())
depto_list = sorted(df_filtros["departamento"].dropna().unique())
producto_list = sorted(df_filtros["producto"].dropna().unique())
#pais_list = sorted(df_filtros["pais"].dropna().unique())

actual = dt.now().year -10 

#year_filter = str([a for a in year_list if a > actual ])
#year_filter = year_filter.to_numpy()


df_anios = pd.read_parquet("data/processed/despachos_anios.parquet", engine="pyarrow")
year_list = df_anios["anio"].to_numpy()
dv22 = df_anios[df_anios['anio'] > actual ]
year_filter = dv22["anio"].to_numpy()

year_list = np.append("Todos",year_list)
year_list = df_anios["anio"].to_numpy()
df_envases = pd.read_parquet("data/processed/despachos_envases.parquet", engine="pyarrow")
envase_list = df_envases["subgrupoenvase"].to_numpy()
envase_list = np.append("Todos",envase_list)

df_color = pd.read_parquet("data/processed/despachos_color.parquet", engine="pyarrow")
color_list = df_color["color"].to_numpy()
color_list = np.append("Todos",color_list)



if "filtroseee" not in st.session_state:
        st.session_state.filtrosee = {
            "anio": "Todos",
            "var": "Todas",
            "prov": "Todas",
            "depto": "Todos",
            "producto": "Todos",
            "Pais": "Todos",
            "Envase": 'Todos'
        }



#dv1 = cargar_datos(QUERY_V1)

dv1 = pd.read_parquet("data/processed/despachos_datos.parquet", engine="pyarrow")

df_filtered = dv1.copy() 
actual = dt.now().year -4 
#dv1.to_parquet("data/processed/despachos.zip", engine="pyarrow", index=False)
#df_nuevo = pd.read_parquet("data/processed/despachos.zip", engine="pyarrow")
#st.write(df_nuevo)
#df_filtered = df_nuevo.copy() 
df_filtered['anio'] = df_filtered['anio'].astype(str)




tab1, tab2, tab3,tab4,tab5,tab6 = st.tabs(["Evolución", "Por Provincias", "Por Color/Tipo","Por Envase","Por Variedades","Consumo Interno"])

with tab1:

  with st.container(border=True):
    col1, col2, col3,col4,col5,col6,col7,col8= st.columns([1, 1, 1,1,1,1,1,1])  # Ajusta los tamaños de las columnas

    # Columna 1: Filtro para Año
    with col1:    
        with st.popover("Año", use_container_width=True):
                st.caption("Selecciona uno o más años de la lista")
                #año = st.multiselect("Año",  year_list, default= ['Todos'],label_visibility="collapsed",help="Selecciona uno o más años")
                año = st.multiselect("Año",  year_list, default= year_filter,label_visibility="collapsed",help="Selecciona uno o más años")
                #anio = st.multiselect("Año:", ["Todos"] + year_list, default=["Todos"])
                año = [str(a) for a in año]  # Asegura que la selección sea string también
    
    with col2:
        with st.popover("Variedad", use_container_width=True):
            st.caption("Selecciona uno o más Variedades de la lista")
            variedad = st.multiselect("Variedad343",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")
    
        # Columna 3: Espacio vacío (puedes agregar algo más si lo deseas)
    with col3:
        with st.popover("Provincia", use_container_width=True):
            st.caption("Selecciona uno o más Provincias de la lista")
            provincia = st.multiselect("Proncias33",  ["Todas"] + prov_list, default=["Todas"],label_visibility="collapsed")
    with col4:
        with st.popover("Departamento", use_container_width=True):
            st.caption("Selecciona uno o más Departamentos de la lista")
            departamento = st.multiselect("dpto",  ["Todos"] + depto_list, default=["Todos"],label_visibility="collapsed")                

    with col5:
        with st.popover("Producto", use_container_width=True):
            st.caption("Selecciona uno o más Productos de la lista")
            producto = st.multiselect("Coloreo",  ["Todos"] + producto_list, default=["Todos"],label_visibility="collapsed")                
    with col6:
        with st.popover("Envase", use_container_width=True):
            st.caption("Selecciona uno o más Envases de la lista")
            envase = st.multiselect("Envased",  envase_list, default=["Todos"],label_visibility="collapsed")                

    with col7:
        with st.popover("Color", use_container_width=True):
            st.caption("Selecciona uno o más Colores de la lista")
            color = st.multiselect("colord",  color_list, default=["Todos"],label_visibility="collapsed")      
    with col8:          
        st.button(" ", icon=":material/print:", on_click=imprimi1 ,use_container_width=True)

        #show_print_button ="""
        #  <script>
        #    function print_page(obj) {
        #        obj.style.display = "none";
        #        parent.window.print();
        #    }
        #  </script>
        #  <button onclick="print_page(this)">
        #      🖨️
        #  </button>
        #"""
        #components.html(show_print_button)       
        #if st.button(" ", icon=":material/print:", use_container_width=True):

  Filtro = 'Filtro = Año = '
  Filtro = Filtro +  ' Todos '

  if año:
    #st.write(año)
    if año[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['anio'].isin(año)]
        df_filtered["anio"] = df_filtered["anio"].astype(str)  
        Filtro = Filtro +  ' ' +str(año) + ' '
          
  
  #st.write(df_filtered)
  if variedad:
    if variedad[0] != 'Todas':
        df_filtered = df_filtered[df_filtered['variedad'].isin(variedad)]
        #st.write(variedad)
    Filtro = Filtro + ' Variedades = ' +  str(variedad) + ' '
  
  if departamento:
    if departamento[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['departamento'].isin(departamento)]
    Filtro = Filtro + ' Departamento = ' +  str(departamento) + ' '
          
  if provincia:        
    if provincia[0] != 'Todas':
        df_filtered = df_filtered[df_filtered['provincia'].isin(provincia)]          
    Filtro = Filtro + ' Provincia = ' +  str(provincia) + ' '

  if producto:
    if producto[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['producto'].isin(producto)]
    Filtro = Filtro + ' Producto = ' +  str(producto) + ' '
  if envase:
    if envase[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['subgrupoenvase'].isin(envase)]
    Filtro = Filtro + ' Envase = ' +  str(envase) + ' '
  if color:
    if color[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['color'].isin(color)]
    Filtro = Filtro + ' Color = ' +  str(color) + ' '


  
  if df_filtered.empty:
    st.error("No se encontraron datos en la base de datos.")
    st.stop()
  dv3= df_filtered
  df2 = df_filtered.groupby(['anio','mes1'], as_index=False)[['litros']].sum()
  
  df_filtered = df_filtered.groupby(['anio'], as_index=False)[['litros']].sum()

  total = []
  total.append(0)
  for index in range(len(df_filtered)):
      if index > 0:
            total.append((  (df_filtered['litros'].loc[index] / df_filtered['litros'].loc[index -1]) -1 ) *100 )
  df_filtered = df_filtered.rename(columns={'litros': "Litros",'anio': "Año"})
  df_filtered['Litros Var %'] = total
  df_filtered = df_filtered.astype({'Litros': int} )
    
    
  #st.write(df_filtered)
 
  st.subheader('Evolución de los despachos por año')

  if st.checkbox('Ver datos en forma de tabla'):
        st.caption(Filtro)


        df_filtered = df_filtered.sort_index(axis = 1)

        styled_df = df_filtered.style.applymap(bgcolor_positive_or_negative, subset=['Litros Var %']).format(
            {"Litros": lambda x : '{:,.0f}'.format(x), 
            "Litros Var %": lambda x : '{:,.2f} %'.format(x),
                                        }
            ,
            thousands='.',
            decimal=',',
        )
        column_orders =("Año", "Litros", "Litros Var %" )
        st.dataframe(styled_df,
              column_config={
                'Año': st.column_config.Column('Año'),
                'Litros': st.column_config.Column('Litros'),
                'Fob': st.column_config.Column('Fob'),
                'Litros Var %': st.column_config.Column('Litros Var %'),
                'Fob Var. %': st.column_config.Column('Fob Var. %'),
                'ppl': st.column_config.Column('ppl'),
                'Prec x Litro Var. %': st.column_config.Column('Prec x Litro Var. %'),
        
                },
                column_order = column_orders,                     
                width = 600,   
                height = 800,
                hide_index=True)

    
      #st.write(df_filtered)
  st.caption(Filtro)
  option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df_filtered['Año'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df_filtered['Litros'].to_list(), "type": "line", "name": 'Hl'},
               ]
  }
  st_echarts(
    options=option, height="400px" ,
  )


  st.write('nuevo')

  #fig = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")  
  #t.plotly_chart(fig, theme="streamlit")
  dv2 = dv3   
  dv3["anio"] = dv3["anio"].astype(int)
  dv2 = dv2[dv2['anio'] > actual ]    
  litros = dv2.pivot_table(
          index='mes', 
          columns='anio',  
          values=['litros'],
          aggfunc='sum'
  )  
  litros.columns = litros.columns.droplevel(0)
  litros = litros.reset_index().rename_axis(None, axis=1)    
  litros  = litros.fillna(0)
  #df2 = dv2.groupby(['anio','mes'], as_index=False)[['litros']].sum()
  df2["anio"] = df2["anio"].astype(str)

  
  colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']

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

  #fig = go.Figure(data=[go.Histogram(y=df2['litros'],cumulative_enabled=True)])
  #fig.show()
  #st.plotly_chart(fig, theme="streamlit")






  
  
  anio1 = litros.columns[1]
  anio2 = litros.columns[2]
  anio3 = litros.columns[3]
  anio4 = litros.columns[4]

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
  desc1 = litros.columns[5]
  desc2 = litros.columns[6]
  desc3 = litros.columns[7]
  desc4 = litros.columns[8]

  st.subheader('Evolución de los despachos por Mes')
  st.caption(Filtro)  
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
                "text": '',
                "textStyle": {
                        "fontSize": 14,
                },                  
                "subtext": '',
            },            
            "xAxis": {"type": "category", "data": litros["mes"].tolist()},
            "yAxis": [
                {"type": "value" ,"name" : "Hl" ,
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
                {"type": "value" , "name" : "Hl Acum",
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

  show_print_button ="""
    <script>
        function print_page(obj) {
            obj.style.display = "none";
            parent.window.print();
        }
    </script>
    <button onclick="print_page(this)">
        🖨️
    </button>
    """
  components.html(show_print_button)  

with tab2:    
    desp_prov.despachos_prov(df_filtros,dv1)
with tab3:    
    desp_color.despachos_color(df_filtros,dv1)  
with tab4:    
    desp_envase.despachos_envase(df_filtros,dv1)  
with tab5:    
    desp_variedad.despachos_variedad(df_filtros,dv1)  
with tab6:    
    desp_consumo.despachos_consumo()  
  
