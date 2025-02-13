import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder

conn = st.connection("postgresql", type="sql")
qu = 'select año anio,sum(cnt) cnt,provincia,subgrupoenvase from inf_desp_prov group by provincia,año,subgrupoenvase ;'  
dfpv1 = conn.query(qu, ttl="0"),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2010]

#pivot = pd.pivot_table(dfpv1, values="cnt", index=['anio','provincia'],columns=['subgrupoenvase'])
#st.dataframe(pivot)
data = dfpv1


gb = GridOptionsBuilder()

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

gb.configure_column(field="provincia", header_name="provincia", width=80, rowGroup= True, )

gb.configure_column(
    field="subgrupoenvase",
    header_name="Tipo Envase",
    flex=1,
    tooltipField="subgrupoenvase",
    rowGroup=True 
)




gb.configure_column(
    field="anio",
    header_name="anio",
    width=100,    
    pivot=True,
)
gb.configure_column(
    field="cnt",
    header_name="cnt",
    width=50,
    type=["numericColumn"],
    aggFunc="sum",
)

gb.configure_grid_options(
    tooltipShowDelay=0,
    pivotMode=True,
)
go = gb.build()

AgGrid(data, gridOptions=go, height=400)
