import streamlit as st
import pandas as pd
#from .database import get_connection

conn = st.connection("postgresql", type="sql"

@st.cache_data
def exportaciones_filtros():
    #conn = get_connection()
    query =  "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais,grupoenvase from exportaciones2_m where producto not in ('Mosto','Alcohol')"
    try:
        df = conn.query(query, ttl="0")
        df.to_parquet("data/processed/exportaciones.parquet", engine="pyarrow", index=False)

        #como esta consulta solo sirve para luego llenar los select de los filtros, puedo poner estos datos en sus correspondientes parquet
        year_list = sorted(df["anio"].dropna().unique(), reverse=True)
        pd.DataFrame({"anio": year_list}).to_parquet("data/processed/expo_anios.parquet", engine="pyarrow", index=False)

        var_list = sorted(df["variedad"].dropna().unique())
        pd.DataFrame({"variedad": var_list}).to_parquet("data/processed/expo_variedades.parquet", engine="pyarrow", index=False)
        
        envase_list = sorted(df["tipo_envase"].dropna().unique())
        pd.DataFrame({"tipo_envase": envase_list}).to_parquet("data/processed/expo_envases.parquet", engine="pyarrow", index=False)

        color_list = sorted(df["color"].dropna().unique())
        pd.DataFrame({"color": color_list}).to_parquet("data/processed/expo_colores.parquet", engine="pyarrow", index=False)

        producto_list = sorted(df["producto"].dropna().unique())
        pd.DataFrame({"producto": producto_list}).to_parquet("data/processed/expo_productos.parquet", engine="pyarrow", index=False)

        pais_list = sorted(df["pais"].dropna().unique())
        pd.DataFrame({"pais": pais_list}).to_parquet("data/processed/expo_paises.parquet", engine="pyarrow", index=False) 

        grupoenvase_list = sorted(df["grupoenvase"].dropna().unique())
        pd.DataFrame({"grupoenvase": grupoenvase_list}).to_parquet("data/processed/expo_grupoenvases.parquet", engine="pyarrow", index=False)                

        #return df #en lugar de retornarlo lo guardo en parquet 
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()  

@st.cache_data           
def filtro_anual(condiciones):
    conn = get_connection()
    where_clause = " AND ".join(condiciones)
    query =  f"""
        SELECT anio, SUM(cantlitros) AS litros, sum(valorfobsolo) AS fob, sum(valorfobsolo) / sum(cantlitros) AS ppl
        FROM exportaciones2_m 
        WHERE {where_clause}
        and producto not in ('Mosto','Alcohol')
        GROUP BY anio 
        ORDER BY anio 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

@st.cache_data           
def registro_anual():
    conn = get_connection()
    query =  f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob, 1 as ppl, variedad1 as variedad, tipo_envase as envase, color, producto
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
        ORDER BY anio 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

@st.cache_data           
def registro_anual_pais():
    conn = get_connection()
    query =  f"""
        SELECT anio, cantlitros AS litros, valorfobsolo AS fob, variedad1, tipo_envase, pais, color, grupoenvase, producto
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
        ORDER BY anio 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()            
          
@st.cache_data           
def filtro_mensual(condiciones, anio):     
    conn = get_connection()
    where_clause = " AND ".join(condiciones)
    query =  f"""
        SELECT anio, mes,mes ||' '|| mess as mes1, SUM(cantlitros) AS litros, sum(valorfobsolo) AS fob, sum(valorfobsolo) / sum(cantlitros) AS ppl
        FROM exportaciones2_m 
        WHERE {where_clause}
        and producto not in ('Mosto','Alcohol')
        and anio > {anio}
        GROUP BY anio, mes 
        ORDER BY anio, mes 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

@st.cache_data           
def registro_mensual(anio):     
    conn = get_connection()
    query =  f"""
        SELECT anio, mes,mes ||' '|| mess as mes1, cantlitros AS litros, valorfobsolo AS fob, 1 as ppl, variedad1 as variedad, tipo_envase as envase, color, producto
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
        and anio > {anio}
        ORDER BY anio, mes 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()


@st.cache_data
def mosto_exportaciones_filtros():
    conn = get_connection()
    query =  "select distinct anio,variedad1 variedad,tipo_envase,color,producto,pais from exportaciones2_m  where producto = 'Mosto' and codigoproducto like '%CONCENTRADO%'"
    try:
        df = conn.query(query, ttl="0")
        df.to_parquet("data/processed/exportaciones_mosto.parquet", engine="pyarrow", index=False)

        #como esta consulta solo sirve para luego llenar los select de los filtros, puedo poner estos datos en sus correspondientes parquet
        year_list = sorted(df["anio"].dropna().unique(), reverse=True)
        pd.DataFrame({"anio": year_list}).to_parquet("data/processed/expo_mosto_anios.parquet", engine="pyarrow", index=False)

        var_list = sorted(df["variedad"].dropna().unique())
        pd.DataFrame({"variedad": var_list}).to_parquet("data/processed/expo_mosto_variedades.parquet", engine="pyarrow", index=False)
        
        envase_list = sorted(df["tipo_envase"].dropna().unique())
        pd.DataFrame({"tipo_envase": envase_list}).to_parquet("data/processed/expo_mosto_envases.parquet", engine="pyarrow", index=False)

        color_list = sorted(df["color"].dropna().unique())
        pd.DataFrame({"color": color_list}).to_parquet("data/processed/expo_mosto_colores.parquet", engine="pyarrow", index=False)

        producto_list = sorted(df["producto"].dropna().unique())
        pd.DataFrame({"producto": producto_list}).to_parquet("data/processed/expo_mosto_productos.parquet", engine="pyarrow", index=False)

        pais_list = sorted(df["pais"].dropna().unique())
        pd.DataFrame({"pais": pais_list}).to_parquet("data/processed/expo_mosto_paises.parquet", engine="pyarrow", index=False)               

        #return df #en lugar de retornarlo lo guardo en parquet 
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

@st.cache_data           
def mosto_registro_anual():
    conn = get_connection()
    query =  f"""
        SELECT anio, cantlitros/743.5 AS litros, valorfobsolo AS fob, 1 AS ppl, pais,variedad1,tipo_envase ,codigoproducto as producto
        FROM exportaciones2_m 
        WHERE producto = 'Mosto' and codigoproducto like '%CONCENTRADO%'
        ORDER BY anio 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

@st.cache_data           
def mosto_registro_mensual(anio):     
    conn = get_connection()
    query =  f"""
        SELECT anio, mes,mes ||' '|| mess as mes1, cantlitros/743.5 AS litros, valorfobsolo AS fob,1 AS ppl,pais
        FROM exportaciones2_m 
        WHERE producto not in ('Mosto','Alcohol')
        and anio > {anio}
        ORDER BY anio, mes 
    """
    try:
        df = conn.query(query, ttl="0")
        return df 
        
        conn.close()
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()
