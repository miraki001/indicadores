import streamlit as st
import streamlit.components.v1 as components
from pivottablejs import pivot_ui
import pandas as pd

iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)

qu = 'select año anio,sum(cnt) cnt,provincia,subgrupoenvase from inf_desp_prov group by provincia,año,subgrupoenvase ;'  
dfpv1 = conn.query(qu, ttl="0"),
#if prov != "Todas": 
#  qu = 'select cnt,provincia from inf_desp_prov where provincia =  :prov;'
#  dfpv1 = conn.query(qu, ttl="0", params={"prov": prov},),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2010]
#dfpv1 = dfpv1[dfpv1['provincia'].isin(prov)]
#st.write(dfpv1)

t = pivot_ui(iris)

with open(t.src) as t:
    components.html(t.read(), width=900, height=1000, scrolling=True)
