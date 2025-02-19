import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder,DataReturnMode,GridUpdateMode
import altair as alt
import numpy as np

conn = st.connection("postgresql", type="sql")

@st.cache_data
def query():
  df3 = conn.query('select año,sum(sup) supeficie,sum(cant) cant_viñedos from superficie_m group by año  ;', ttl="0"),
  return df3
df3 = query()
df2 = df3[0]
st.write(df2)
total = []
for index in range(len(df2)):
  if index > 0:
    total.append(df2['supeficie'].loc[index] / df2['supeficie'].loc[index -1])
st.write(total)
df2['var ha'] = total
st.write(df2)


