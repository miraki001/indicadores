
import streamlit as st


conn = st.connection("postgresql", type="sql")
df = conn.query('select distinct anio from superficievariedad_m ;', ttl="0")
year_list = list(df.anio.unique())[::-1]

dv = conn.query('select distinct variedad from superficievariedad_m ;', ttl="0")
var_list = list(dv.variedad.unique())[::-1]

dp = conn.query('select distinct provincia from superficievariedad_m ;', ttl="0")
prov_list = list(dp.provincia.unique())[::-1]
color_list =  ("Tinto", "Blanco","Rosado","Sin Dato")

with st.popover("Abrir Filtros"):
    st.markdown("Filtros 👋")
    anio = st.selectbox( "Año :", year_list )
    var = st.selectbox( "Variedad :", var_list )
    prov = st.selectbox( "Provincia :", prov_list )
    color = st.selectbox( "Color :", color_list )
    st.button("Ok", type="primary")



tab1, tab2, tab3 = st.tabs(["Superficie", "Cosecha", "Rendimientos"])

with tab1:
    st.header("Cantidad de Viñedos")
    dv1 = conn.query('select anio,sum(sup) sup,count(*) cnt  from superficievariedad_m group by anio ;', ttl="0")

    dv1['anio'] = dv1['anio'].astype(str)

    newdf=dv1.set_index('anio',inplace=False).rename_axis(None)
    
    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": { "type": 'cross' }
            },
        "legend": {},    
        "xAxis": {
            "type": "category",
            "data": dv1['anio'].to_list(),
        },
        "yAxis": {"type": "value"},
        "series": [{"data": dv1['sup'].to_list(), "type": "line", "name": 'Hectareas'}
                   ,{"data": dv1['cnt'].to_list(), "type": "line","name":'Cnt Viñedos'}]
    }
    st_echarts(
        options=option, height="400px" ,
    )

    
    
with tab2:
    st.header("A dog")
    
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
