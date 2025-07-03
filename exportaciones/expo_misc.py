import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Line
from datetime import datetime as dt
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Sankey
from collections import defaultdict
import plotly.graph_objects as go
import altair as alt
import matplotlib.colors as mcolors
from great_tables import GT, html

def exporta_misc():

    def append_row(df, row):
        return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)
    
    def bgcolor_positive_or_negative(value):
        bgcolor = "#EC654A" if value < 0 else "lightgreen"
        return f"background-color: {bgcolor};"
        



    
    hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    streamlit_style = """
        <style>
        iframe[title="streamlit_echarts.st_echarts"]{ height: 500px;} 
       </style>
        """
    st.markdown(streamlit_style, unsafe_allow_html=True) 



    
    
    dv1 = pd.read_parquet("data/processed/expo_registro_anual.parquet", engine="pyarrow")    
    dv1['anio'] = dv1['anio'].astype(str)

    
    
    # Pivotear el DataFrame para que cada fila sea una provincia y cada columna un año
    #st.write(dv1)
    #melted_df = melted_df[melted_df['litros'] != 0 ]
    #dv1 = dv1.groupby(['pais','anio'], as_index=False)[['litros']].sum()
    dv1 = dv1.groupby(['variedad','anio'], as_index=False)[['litros']].sum()
    dv1 = dv1[dv1['anio'] > '2014']
    #dv2 = dv1.groupby(['pais'], as_index=False)[['litros']].sum()
    dv2 = dv1.groupby(['variedad'], as_index=False)[['litros']].sum()
    indexe1 = np.r_[-20:0]
    dv2 = dv2.sort_values("litros", ignore_index=True).iloc[indexe1]
    #pais_list11 = sorted(dv2["pais"].dropna().unique(), reverse=True)
    var_list11 = sorted(dv2["variedad1"].dropna().unique(), reverse=True)
    #indexe1 = np.r_[-20:0]
    #dv1 = dv1.sort_values("litros", ignore_index=True).iloc[indexe1]
    #dv1 = dv1[dv1['anio'] > '2014']
    #dv1= dv1[dv1['pais'].isin(pais_list11)]
    dv1= dv1[dv1['variedad'].isin(var_list11)]
    #dv1 = dv1[dv1['pais']== pais_list11]
    #indexe1 = np.r_[-20:0]
    #dv1 = dv1.sort_values("litros", ignore_index=True).iloc[indexe1]
    #df_pivot = dv1.pivot(index='pais', columns='anio', values='litros').reset_index()
    df_pivot = dv1.pivot(index='variedad', columns='anio', values='litros').reset_index()

    # Asegurar que los años estén ordenados correctamente
    #df_pivot = df_pivot[['pais'] + sorted([col for col in df_pivot.columns if col != 'pais'])]
    df_pivot = df_pivot[['variedad1'] + sorted([col for col in df_pivot.columns if col != 'variedad1'])]

    # Identificar las columnas de año, ordenadas de mayor a menor
    #anios = sorted([col for col in df_pivot.columns if col != 'pais'])
    anios = sorted([col for col in df_pivot.columns if col != 'variedad1'])
        
    # Calcular el cambio porcentual entre años (sobre las columnas)
    df_pct = df_pivot[anios].pct_change(axis=1)
    df_pct = df_pct.round(4).fillna(0)  # Redondear y reemplazar NaN por 0

    # Renombrar columnas de porcentaje
    df_pct.columns = [f"{col}_Δ%" for col in df_pct.columns]

    # Insertar las columnas de diferencia al lado de cada año
    #df_resultado = df_pivot[['pais']].copy()
    df_resultado = df_pivot[['variedad']].copy()
    for año, col_delta in zip(anios, df_pct.columns):
        df_resultado[año] = df_pivot[año]
        df_resultado[col_delta] = df_pct[col_delta]*100
        
    st.write(df_resultado)
    # Ordenar columnas: primero 'provincia', luego años descendentes intercaladas con %Δ
    #columnas_ordenadas = ['pais']
    columnas_ordenadas = ['variedad']
    for año in sorted(anios, reverse=True):
        #columnas_ordenadas.append(año)
        columnas_ordenadas.append(f"{año}_Δ%")

    df_resultado = df_resultado[columnas_ordenadas]
      
    # Ordenar filas por provincia
    #df_resultado = df_resultado.sort_values(by="pais")
    df_resultado = df_resultado.sort_values(by="variedad")
    #st.write(df_resultado)
                
    #st.markdown("<h4 style='text-align: left;'>Superficie por Provincia y variación interanual (%)</h4>", unsafe_allow_html=True)

    # Obtener columnas de porcentaje
    cols_pct = [col for col in df_resultado.columns if col.endswith('_Δ%')]
    st.write(df_resultado)
    melted_df = df_resultado.melt(id_vars=['variedad'], 
                    var_name='anio', value_name='litros')
    melted_df = melted_df[melted_df['litros'] != 0 ]
    st.write(melted_df)
    input_color = 'blue'
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    sc = 'blues'
    st.write(selected_color_theme)
    heatmap = alt.Chart(melted_df).mark_rect().encode(
            y=alt.Y(f'{'anio'}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{'variedad'}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({'litros'}):Q',
                             legend=None,
                             #scale=alt.Scale(scheme=selected_color_theme)),
                             scale=alt.Scale(scheme=sc)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    st.altair_chart(heatmap, use_container_width=True)
        
    # Columnas normalizadas que se usarán solo para aplicar color
    cols_norm = [f"{col}_norm" for col in cols_pct]

    # Obtener todos los valores de % en una sola serie plana, sin NaN
    valores_pct = df_resultado[cols_pct].values.flatten()
    valores_pct = valores_pct[~np.isnan(valores_pct)]

    # Calcular el máximo valor absoluto para normalizar de -max_abs a max_abs
    max_abs = np.abs(valores_pct).max()

    # Crear un valor de recorte más representativo
    max_abs_visible = 10  # o 75, o 50 según el contraste deseado
    vmax_visible = np.percentile(np.abs(df_resultado[cols_pct].values), 95)

    # Recalcular normalización y colores
    norma = mcolors.TwoSlopeNorm(vmin=-vmax_visible, vcenter=0, vmax=vmax_visible)

    # Crear columnas normalizadas con vmax_visible
    for col in cols_pct:
        col_norm = f"{col}_norm"
        df_resultado[col_norm] = (
            df_resultado[col]
            .clip(-vmax_visible, vmax_visible)
            .astype(float) / vmax_visible
        )

    # Crear colormap divergente: rojo - gris - verde
    colors = ['#b2182b', '#e6e6e6', '#4d9221']
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_red_gray_green", colors)
    #st.write(df_resultado[cols_pct].describe())
    #st.write(df_resultado)

    #Convierte valor entre -1 y 1 en un color HEX
    def valor_a_color(valor_norm):
        try:
            val = float(valor_norm)
            if np.isnan(val):
                return "#ffffff"
            return to_hex(cmap(norma(val)))
        except Exception:
            return "#ffffff"
