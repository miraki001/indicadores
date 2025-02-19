
conn = st.connection("postgresql", type="sql")
qu = 'select * from despachos_m ;'  
dfpv1 = conn.query(qu, ttl="0"),
dfpv1 = dfpv1[0]
dfpv1 = dfpv1[dfpv1['anio'] > 2014]
data = dfpv1
#st.write(data)


AgGrid(data,height=500)
