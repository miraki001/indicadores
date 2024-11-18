
import streamlit as st


conn = st.connection("postgresql", type="sql")
df = conn.query('select * from superficievariedad_m ;', ttl="0")

with st.popover("Abrir Filtros"):
    st.markdown("Filtros 👋")
    anio = st.popover.selectbox( "Año :", (df['anio'].unique)
    )



tab1, tab2, tab3 = st.tabs(["Superficie", "Cosecha", "Rendimientos"])

with tab1:
    st.header("A cat")
    
with tab2:
    st.header("A dog")
    
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
