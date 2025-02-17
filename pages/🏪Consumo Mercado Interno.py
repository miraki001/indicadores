import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts

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




hide_streamlit_style = """
            <style>
                
                header {visibility: hidden;}
                footer {visibility: hidden;} 
                .streamlit-footer {display: none;}
                
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT periodo,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" FROM scentia_res;', ttl="0")

st.subheader('Ventas en el Canal Mayorista, Según datos de Scentia')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)

df1 = df[df['canal'] ==  'Mayoristas' ]
df1['periodo'] = df['periodo'].astype(str)

newdf=df1.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df1['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df1['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": df1['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": df1['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": df1['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": df1['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": df1['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": df1['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)

data1 = conn.query('SELECT periodo,canal,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES","SIDRAS_Y_SABORES","VINOS_FORTIFICADOS" FROM scentia_valores order by periodo ;', ttl="0")
#st.write(df)

st.subheader('Ventas en el Canal Mayorista, Según datos de Scentia en Valores')


if st.checkbox('Ver datos en forma de tabla Valores'):
    st.write(data1)

#data1['canal'] = 'Mayoristas'
data_filt = data1[data1['canal'] ==  'Mayoristas' ]

data_filt['periodo'] = data_filt['periodo'].astype(str)


newdf=data_filt.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": data_filt['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": data_filt['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": data_filt['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": data_filt['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": data_filt['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": data_filt['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": data_filt['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": data_filt['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)


st.subheader('Ventas en el Canal Self Cadenas, Según datos de Scentia')

df1 = df[df['canal'] ==  'Self Cadenas' ]

df1['periodo'] = df1['periodo'].astype(str)

newdf1=df1.set_index('periodo',inplace=False).rename_axis(None)



option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df1['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df1['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": df1['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": df1['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": df1['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": df1['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": df1['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": df1['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)


st.subheader('Ventas en el Canal Self Cadenas, Según datos de Scentia en Valores')


data_filt = data1[data1['canal'] ==  'Self Cadenas' ]

data_filt['periodo'] = data_filt['periodo'].astype(str)


newdf=data_filt.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": data_filt['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": data_filt['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": data_filt['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": data_filt['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": data_filt['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": data_filt['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": data_filt['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": data_filt['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)



df1 = df[df['canal'] ==  'Independientes' ]

df1['periodo'] = df1['periodo'].astype(str)

newdf2=df1.set_index('periodo',inplace=False).rename_axis(None)



option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df1['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df1['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": df1['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": df1['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": df1['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": df1['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": df1['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": df1['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)

st.subheader('Ventas en el Canal Independiente, Según datos de Scentia en Valores')


#data1['canal'] = 'Mayoristas'
data_filt = data1[data1['canal'] ==  'Independientes' ]

data_filt['periodo'] = data_filt['periodo'].astype(str)


newdf=data_filt.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": data_filt['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": data_filt['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": data_filt['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": data_filt['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": data_filt['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": data_filt['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": data_filt['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": data_filt['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)

st.subheader('Ventas en el Canal Tiendas y Kioscos, Según datos de Scentia en Valores')
df1 = df[df['canal'] ==  'Tiendas' ]

df1['periodo'] = df1['periodo'].astype(str)

newdf21=df1.set_index('periodo',inplace=False).rename_axis(None)


option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df1['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df1['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": df1['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": df1['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": df1['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": df1['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": df1['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": df1['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)


st.subheader('Ventas en el Canal Tiendas y Kioscos, Según datos de Scentia en Valores')


#data1['canal'] = 'Mayoristas'
data_filt = data1[data1['canal'] ==  'Tiendas' ]

data_filt['periodo'] = data_filt['periodo'].astype(str)


newdf=data_filt.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": data_filt['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": data_filt['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": data_filt['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": data_filt['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": data_filt['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": data_filt['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": data_filt['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": data_filt['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)




st.subheader('Ventas Totales, Según datos de Scentia')

pivot_table_basic = data1.pivot_table(
    index='periodo', 
    values=['VINOS_COMUNES', 'VINOS_FINOS', 'CERVEZAS','APERITIVOS_RTD','ESPUMANTES','APERITIVOS_ALC','VINOS_FORTIFICADOS','SIDRAS_Y_SABORES'],
    aggfunc='sum'
)

df1 = pd.DataFrame(pivot_table_basic)
df1 = data_filt.reset_index()  

df1['periodo'] = df1['periodo'].astype(str)

newdf3=df1.set_index('periodo',inplace=False).rename_axis(None)



option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df1['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df1['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": df1['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": df1['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": df1['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": df1['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": df1['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": df1['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)


st.subheader('Ventas Totales, Según datos de Scentia en Valores')


#data1['canal'] = 'Mayoristas'
#data_filt = data1.groupby('periodo').sum()

pivot_table_basic = data1.pivot_table(
    index='periodo', 
    values=['VINOS_COMUNES', 'VINOS_FINOS', 'CERVEZAS','APERITIVOS_RTD','ESPUMANTES','APERITIVOS_ALC','VINOS_FORTIFICADOS','SIDRAS_Y_SABORES'],
    aggfunc='sum'
)

data_filt = pd.DataFrame(pivot_table_basic)
data_filt = data_filt.reset_index()  
#data_filt = data1



#data_filt.columns = pivot_table_basic.columns.droplevel(0)
#data_filt = pivot_table_basic.reset_index().rename_axis(None, axis=1)
st.write(data_filt)




data_filt['periodo'] = data_filt['periodo'].astype(str)


#newdf=data_filt.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": data_filt['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": data_filt['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": data_filt['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} 
               ,{"data": data_filt['APERITIVOS_RTD'].to_list(), "type": "line","name":'Ape. RTD'} 
               ,{"data": data_filt['ESPUMANTES'].to_list(), "type": "line","name":'Espumantes'} 
               ,{"data": data_filt['APERITIVOS_ALC'].to_list(), "type": "line","name":'Ape. Alc'} 
               ,{"data": data_filt['VINOS_FORTIFICADOS'].to_list(), "type": "line","name":'Vinos Fort.'} 
               ,{"data": data_filt['SIDRAS_Y_SABORES'].to_list(), "type": "line","name":'Sidras'} ],
#    "series": [{"data": data_filt['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)





df4 = conn.query('SELECT "Values" as value ,"Columns" as name  FROM scentia_tot_anual;', ttl="0")

st.subheader('Ventas Totales ultimo año, Según datos de Scentia')

#st.write(json.dumps(df3['VINOS_COMUNES'].tolist()))
#df4.to_json('diskData', orient='records', lines=True)
json_list = json.loads(json.dumps(list(df4.T.to_dict().values())))
#diskData = json.loads(temp.json)
#st.write('convert')
#st.write(diskData)
#st.write(json_list)


option = {
    "tooltip": {
        #"trigger": 'axis',
        #"axisPointer": { "type": 'cross' },
        "formatter": JsCode(
            "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
        ).js_code,
    },
    "legend": {"data": ["value","name"]},   
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
    options=option, height="600px",
)
