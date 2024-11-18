
import streamlit as st


conn = st.connection("postgresql", type="sql")
df = conn.query('select distinct anio from superficievariedad_m ;', ttl="0")
year_list = list(df.anio.unique())[::-1]

dv = conn.query('select distinct variedad from superficievariedad_m ;', ttl="0")
var_list = list(dv.variedad.unique())[::-1]

with st.popover("Abrir Filtros"):
    st.markdown("Filtros 👋")
    anio = st.selectbox( "Año :", year_list )
    var = st.selectbox( "Variedad :", var_list )
    st.button("Ok", type="primary")



tab1, tab2, tab3 = st.tabs(["Superficie", "Cosecha", "Rendimientos"])

with tab1:
    st.header("A cat")
    
with tab2:
    st.header("A dog")
    
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
