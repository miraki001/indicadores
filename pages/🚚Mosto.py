import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np

return_mode = st.sidebar.selectbox(
    "Return Mode", list(DataReturnMode.__members__), index=1
)
return_mode_value = DataReturnMode.__members__[return_mode]


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
    width=100,
    type=["numericColumn"],
    aggFunc="sum",
    valueFormatter="value.toLocaleString()",
)

gb.configure_grid_options(
    tooltipShowDelay=0,
    pivotMode=True,
)

gb.configure_grid_options(
    autoGroupColumnDef=dict(
        minWidth=300, 
        enableRangeSelection=True,
        enableRangeHandle=True,
        headerName = 'Provincias',
        pinned="left", 
        cellRendererParams=dict(suppressCount=True)
    )
)
go = gb.build()

grid_response  = AgGrid(data, gridOptions=go,data_return_mode=return_mode_value, height=400)

df = grid_response["data"]
st.write(df)
selected = grid_response["selected_rows"]
selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors="coerce")

chart_data = df.loc[:, ["provincia"]].assign(source="total")

if not selected_df.empty:
    selected_data = selected_df.loc[:, ["provincia"]].assign(
        source="selection"
    )
    chart_data = pd.concat([chart_data, selected_data])


#chart_data = data
chart_data = pd.melt(
    chart_data, id_vars=["provincia"], var_name="item", value_name="quantity"
)
chart = (
    alt.Chart(data=chart_data)
    .mark_bar()
    .encode(
        x=alt.X("item:O"),
        y=alt.Y("sum(quantity):Q", stack=False),
        color=alt.Color("source:N", scale=alt.Scale(domain=["total", "selection"])),
    )
)
st.altair_chart(chart, use_container_width=True)
