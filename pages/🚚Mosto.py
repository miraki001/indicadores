import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json


qu = 'select año anio,sum(cnt) cnt,provincia,subgrupoenvase from inf_desp_prov group by provincia,año,subgrupoenvase ;'  
dfpv1 = conn.query(qu, ttl="0"),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2010]

pivot = pd.pivot_table(dfpv1, values="cnt", index=['anio','provincia'],columns=['subgrupoenvase'], aggfunc={'cnt': [min,max,np.mean,np.std]} )
st.dataframe(pivot)
