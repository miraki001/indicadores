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

year_list = sorted(dv1["anio"].dropna().unique(), reverse=True)
#st.write(year_list)
año = st.multiselect("Año",  year_list, default=['2024'],label_visibility="collapsed",help="Selecciona uno o más años")
año = [str(a) for a in año]  # Asegura que la selección sea string también


df_filtered = dv1.copy()
df_filtered = df_filtered[df_filtered['anio'].isin(año)]
df_filtered["anio"] = df_filtered["anio"].astype(str)

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

top_bottom_11 = df_variedad.sort_values("litros", ignore_index=True).iloc[indexe1]
#st.write(top_bottom_11)
pais_list11 = sorted(top_bottom_11["pais"].dropna().unique(), reverse=True)
var_list11 = sorted(top_bottom_11["variedad1"].dropna().unique())



#agregamos los litros del resto de los paises y el resto de las variedade
#st.write(df_varlts)


por1 = []
por2 = []


for index in range(len(df_varlts)):
    var = df_varlts['variedad1'].iloc[index]
    valor = df_varlts['litros'].iloc[index]
    valor1 = df_var.loc[df_var["variedad1"] == var, "litros"]
    por1.append( (int(valor) / int(valor1) ) *100 )
    pais = df_varlts['pais'].iloc[index]
    valor = df_varlts['litros'].iloc[index]
    valor1 = df_pais.loc[df_pais["pais"] == pais, "litros"]    
    por2.append(  (int(valor) / int(valor1)) *100 )

df_varlts['porceVar'] = por1
df_varlts['porcePais'] = por2
#st.write(df_varlts)

df_var3 = df_varlts.groupby(['pais'], as_index=False)[['fob', 'litros']].sum()
df_var4 = df_varlts.groupby(['variedad1'], as_index=False)[['fob', 'litros']].sum()
#st.write(top_litros_10_pais)
#st.write(top_litros_10_var)


total_var = df_var['litros'].sum()
#st.write(total_var)
tot1 = 0
for index in range(len(top_litros_10_pais)) :
    valor = top_litros_10_pais['litros'].iloc[index]
    pais = top_litros_10_pais['pais'].iloc[index]
    valor1 = df_var3.loc[df_var3["pais"] == pais, "litros"]
    dif = valor - int(valor1)
    tot1 = tot1 + dif
    por1 = (dif/total_var)* 100
    new_row = pd.Series({'fob': 1, 'pais': pais, 'variedad1': 'OTRAS','litros': dif,'porceVar':por1,'porcePais': por1, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row)    
    
st.write(df_varlts)
for index in range(len(top_litros_10_pais)) :
    valor = top_litros_10_pais['litros'].iloc[index]
    pais = top_litros_10_pais['pais'].iloc[index]
    por1 =  100
    new_row = pd.Series({'fob': 1, 'pais': 'TOTAL PAISES', 'variedad1': pais,'litros': valor,'porceVar':por1,'porcePais': por1, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row) 



tot = 0
for index in range(len(top_litros_10_var)) :
    valor = top_litros_10_var['litros'].iloc[index]
    var = top_litros_10_var['variedad1'].iloc[index]
    valor1 = df_var4.loc[df_var4["variedad1"] == var, "litros"]
    dif = valor - int(valor1)
    tot = tot + dif
    por1 = (dif/total_var)* 100
    new_row = pd.Series({'fob': 1, 'pais': 'OTROS', 'variedad1': var,'litros': dif,'porceVar':por1,'porcePais': por1, 'index' : len(df_var2)})
    df_varlts = append_row(df_varlts, new_row)    


#st.write(tot)


df5 = df_variedad[~df_variedad['variedad1'].isin(var_listlts)]
df5 = df5[~df5['pais'].isin(pais_listlts)]
Total = df5['litros'].sum()
#st.write(Total)
por1 =  100
new_row = pd.Series({'fob': 1, 'pais': 'TOTAL PAISES', 'variedad1': 'OTROS','litros': tot+ Total,'porceVar':por1,'porcePais': por1, 'index' : len(df_varlts)})
df_varlts = append_row(df_varlts, new_row) 

for index in range(len(top_litros_10_pais)) :
    valor = top_litros_10_var['litros'].iloc[index]
    var = top_litros_10_var['variedad1'].iloc[index]
    por1 = 100
    new_row = pd.Series({'fob': 1, 'variedad1': 'TOTAL VARIEDAD', 'pais': var,'litros': valor,'porceVar':por1,'porcePais': por1, 'index' : len(df_varlts)})
    df_varlts = append_row(df_varlts, new_row)  

por1 =  100
new_row = pd.Series({'fob': 1, 'variedad1': 'TOTAL VARIEDAD', 'pais': 'OTRAS','litros': tot1+ Total,'porceVar':por1,'porcePais': por1, 'index' : len(df_varlts)})
df_varlts = append_row(df_varlts, new_row) 



df11 = pd.DataFrame({'name':var_listlts + pais_listlts})
result11 = df11.to_json(orient="records")
lista = ''

df_varlts.drop(['fob'], axis='columns', inplace=True)
df_varlts = df_varlts.rename(columns={'pais': "source",'variedad1': "target",'litros': "value"})
result32 = df_varlts.to_json(orient="records")
pp11 = '{ "nodes": ' + result11 + ' , "links": ' + lista + result32   + '}' 
data11 = json.loads(pp11)
pp12 =  lista + result32 
data12 = json.loads(pp12)
st.write(result32)

option = {
    "title": {"text": "Top 10 en Litros"},
    "tooltip": {"trigger": "item", "triggerOn": "mousemove",
                "formatter": JsCode("function (info) { if (info.dataType === 'edge')  { return info.porceVar || (info.data.porcePais + ' > ' + info.data.target + '<br/>FOB: USD ' + info.data.value.toLocaleString()); } else {return info.data.name}};").js_code,  
            
               },
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
                    "lineStyle": {"color": "source", "opacity": 0.6},
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
