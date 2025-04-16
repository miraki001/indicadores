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
from sqlalchemy import create_engine

st.set_page_config(layout="wide")


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

# Datos de conexión (modifica según tu entorno)
DB_USER = "observa"
DB_PASSWORD = "observa"
DB_HOST = "119.8.155.25"
DB_PORT = "5432"
DB_NAME = "observa"

# Crear conexión
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
st.write("Conexión SQL creada en evo:", engine)

# Función para cargar datos desde SQL
@st.cache_data
def cargar_datos(query):
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
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

dv1['anio'] = dv1['anio'].astype(str)

with st.container(border=True):
    col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])  # Ajusta los tamaños de las columnas

# Columna 1: Filtro para Año
    with col1:
        with st.popover("Año"):
            st.caption("Selecciona uno o más años de la lista")
            año = st.multiselect("Año",  year_list, default=[2024],label_visibility="collapsed",help="Selecciona uno o más años")
            año = [str(a) for a in año]  # Asegura que la selección sea string también
        
    # Columna 2: Filtro para Países
    with col2:
        with st.popover("Variedad"):
            st.caption("Selecciona uno o más Variedades de la lista")
            variedad = st.multiselect("Variedad",  ["Todas"] + var_list, default=["Todas"],label_visibility="collapsed")

    # Columna 3: Filtro envase
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
if color:
    if color[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['color'].isin(color)]          
if grupoenvase:
    if grupoenvase[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['grupoenvase'].isin(grupoenvase)]               
if producto:
    if producto[0] != 'Todos':
        df_filtered = df_filtered[df_filtered['producto'].isin(producto)]      


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
#st.write(var_listlts)
var_listp = var_listlts
var_listlts.append("TOTAL VARIEDAD")
pais_listlts.append("OTROS")
pais_listp =pais_listlts
pais_listlts.append("TOTAL PAISES")
#st.write(var_listlts)

df_var2 = df_var2.reset_index().rename_axis(None, axis=1)
#st.write(top_bottom_10_pais)

df11 = pd.DataFrame({'name':var_list1 + pais_list1})

#df41 = pd.DataFrame({'name': "TOTAL PAISES"})
df42 = pd.DataFrame({'name':var_listp})
level = []
for index in range(len(df42)):
     level.append('3')   
df42['level'] = level                       
new_row = pd.Series({'name':'TOTAL VARIEDAD','level': 4})
df42 = append_row(df42, new_row)    
#st.write(df42)

df43 = pd.DataFrame({'name': pais_listp})
level = []
for index in range(len(df43)):
     level.append('2')   
df43['level'] = level                       

new_row = pd.Series({'name':'TOTAL PAISES','level': 1})
df43 = append_row(df43, new_row)    

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
st.subheader('Exportaciones por Pais en Litros')
#agregamos el fob del resto de los paises y el resto de las variedade

df_var3 = df_var2.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
df_var4 = df_var2.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
#st.write(df_var3)
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


############# orden 
# Totales por source (nivel 0)


###############
# Renombramos columnas
df_var2 = df_var2.rename(columns={'pais': "source", 'variedad1': "target", 'fob': "value"})

# Eliminamos columna innecesaria
df_var2.drop(['litros'], axis='columns', inplace=True)

# Totales por source (nivel 0)
source_totals = df_var2.groupby('source')['value'].sum().to_dict()

# Calculamos porcentaje por fila
df_var2['percentage'] = df_var2.apply(
    lambda row: round((row['value'] / source_totals.get(row['source'], 1)) * 100, 2), axis=1
)

# Creamos un label por link (tooltip opcional)
df_var2['label'] = df_var2.apply(
    lambda row: f"{row['source']} ? {row['target']} ({row['percentage']}%)", axis=1
)

# Calculamos totales por nivel
total_source = df_var2.groupby('source')['value'].sum().sum()
total_target = df_var2.groupby('target')['value'].sum().sum()

# Listado único de nodos
nodes = list(set(df_var2['source']).union(set(df_var2['target'])))

# Enriquecemos nodos con total y %
nodes_enriched = []
for node in nodes:
    is_source = node in df_var2['source'].values
    is_target = node in df_var2['target'].values

    node_total = 0
    perc_total = 0
    if is_source:
        node_total = df_var2[df_var2['source'] == node]['value'].sum()
        perc_total = round((node_total / total_source) * 100, 2) if total_source else 0
    elif is_target:
        node_total = df_var2[df_var2['target'] == node]['value'].sum()
        perc_total = round((node_total / total_target) * 100, 2) if total_target else 0

    label = f"{node} ({node_total:,.0f} USD, {perc_total}%)"
    #nodes_enriched.append({"name": label})
    nodes_enriched.append({"original": node, "name": label, "total": node_total})

# Ordenamos los nodos por total (descendente)
nodes_data_sorted = sorted(nodes_enriched, key=lambda x: x["total"], reverse=True)

# Creamos el mapping original ? enriquecido
name_mapping = {item["original"]: item["name"] for item in nodes_data_sorted}
st.write(name_mapping)

# Aplicamos el mapping
df_var2['source'] = df_var2['source'].map(name_mapping)
df_var2['target'] = df_var2['target'].map(name_mapping)

# Creamos lista final de nodos enriquecidos, ordenada
#nodes_enriched = [{"name": item["name"]} for item in nodes_data_sorted]

# Recalculamos nodos únicos válidos
nodes = list(set(df_var2['source']).union(set(df_var2['target'])))
nodes = [n for n in nodes if pd.notna(n)]

#nodes_enriched = [{"name": node} for node in nodes]
st.write(df_var2)
# Convertimos a JSON
result1 = json.dumps(nodes_enriched)
result3 = df_var2.to_json(orient="records")

# Armamos el paquete final
pp = '{ "nodes": ' + result1 + ' , "links": ' + result3 + '}'
data1 = json.loads(pp)

# Construimos la visualización
option = {
    "tooltip": {
        "trigger": "item",
        "formatter": {
            "function": """
                function (info) {
                    if (info.dataType === 'edge') {
                        return info.data.label || 
                            (info.data.source + " ? " + info.data.target + "<br/>FOB: USD " + info.data.value.toLocaleString());
                    } else {
                        return info.name;
                    }
                }
            """
        }
    },

    "series": [
        {
            "type": "sankey",
            "data": data1["nodes"],
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
            ],
            "lineStyle": {"curveness": 0.5},
            "label": {
                "show": True,
                "position": "right",
                "formatter": "{b}"
            }
        }
    ],
}
st_echarts(option,key="otro", height="500px")


#agregamos los litros del resto de los paises y el resto de las variedade
#st.write(df_varlts)
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
    new_row = pd.Series({'fob': 1, 'pais': 'OTROS', 'variedad1': var,'litros': dif, 'index' : len(df_var2)})
    df_varlts = append_row(df_varlts, new_row)    


#st.write(tot)


df5 = df_variedad[~df_variedad['variedad1'].isin(var_listlts)]
df5 = df5[~df5['pais'].isin(pais_listlts)]
Total = df5['litros'].sum()
#st.write(Total)
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
result32 = df_varlts.to_json(orient="records")
pp11 = '{ "nodes": ' + result11 + ' , "links": ' + lista + result32   + '}' 
data11 = json.loads(pp11)
pp12 =  lista + result32 
data12 = json.loads(pp12)

option = {
    "title": {"text": "Top 10 en Litros"},
    "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
    "series": [
        {
            "type": "sankey",
            "data":  data11["nodes"],
            "links": data11["links"],
            "emphasis": {"focus": "adjacency"},
            "levels": [
                {
                    "depth": 0,
                    "itemStyle": {"color": "#06C2CC"},
                    "lineStyle": {"color": "variedad1", "opacity": 0.6},
                },
                {
                    "depth": 1,
                    "itemStyle": {"color": "#1E8DB6"},
                    "lineStyle": {"color": "pais", "opacity": 0.6},
                },
                {
                    "depth": 2,
                    "itemStyle": {"color": "#A9F8FA"},
                    "lineStyle": {"color": "pais", "opacity": 0.6},
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
