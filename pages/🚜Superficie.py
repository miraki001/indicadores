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
  df3 = conn.query('select año,sum(sup) supeficie,sum(cant) cant_viñedos from superficie_m group by año order by año  ;', ttl="0"),
  return df3
df3 = query()
df2 = df3[0]
st.write(df2)
total = []
tot1 = []
total.append(0)
tot1.append(0)
for index in range(len(df2)):
  if index > 0:
    total.append((  (df2['supeficie'].loc[index] / df2['supeficie'].loc[index -1]) -1 ) *100 )
    tot1.append((  (df2['cant_viñedos'].loc[index] / df2['cant_viñedos'].loc[index -1]) -1 ) *100 )
st.write(total)
df2['sup var'] = total
df2['var_cnt'] = tot1
st.write(df2)


