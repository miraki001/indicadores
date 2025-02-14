import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np



conn = st.connection("postgresql", type="sql")
qu = 'select * from despachos_m ;'  
dfpv1 = conn.query(qu, ttl="0"),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2014]
data = dfpv1
#st.write(data)


AgGrid(data,height=500)


