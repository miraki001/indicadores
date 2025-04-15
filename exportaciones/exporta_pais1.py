import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Sankey
from pyecharts import options as opts
from collections import defaultdict

from datetime import datetime as dt

def exporta_destino():




    # --- Datos iniciales con niveles ---
    raw_nodes = [
        {"name": "Botella", "level": 1},
        {"name": "Granel", "level": 1},
        {"name": "Tinto", "level": 2},
        {"name": "Blanco", "level": 2},
        {"name": "Europa", "level": 3},
        {"name": "America", "level": 3},
    ]

    links = [
        {"source": "Botella", "target": "Tinto", "value": 10},
        {"source": "Granel", "target": "Tinto", "value": 5},
        {"source": "Granel", "target": "Blanco", "value": 7},
        {"source": "Tinto", "target": "Europa", "value": 12},
    {"source": "Blanco", "target": "America", "value": 7},
    ]


    # --- Calcular entradas y salidas por nodo ---
    node_input = defaultdict(int)
    node_output = defaultdict(int)

    for link in links:
        node_input[link["target"]] += link["value"]
        node_output[link["source"]] += link["value"]

    # --- Agrupar por nivel y calcular totales por nivel ---
    level_totals = defaultdict(int)
    node_values = {}

    for node in raw_nodes:
        name = node["name"]
        level = node["level"]
        if level == 1:
            value = node_output.get(name, 0)  # nivel 1 usa salidas
        else:
            value = node_input.get(name, 0)   # los demás usan entradas
        node_values[name] = value
        level_totals[level] += value

    # --- ?? Acá colocás el mapa de nombres a etiquetas con valor y porcentaje ---
    name_to_label = {
        node["name"]: f'{node["name"]}\n{node_values[node["name"]]:.0f} ({(node_values[node["name"]] / level_totals[node["level"]] * 100):.0f}%)'
        for node in raw_nodes
    }

    # --- ?? Luego generás los nodos con los labels en "name" ---
    nodes = [{"name": label} for label in name_to_label.values()]

    # --- ?? Y también actualizás los links con esos labels ---
    updated_links = [
        {"source": name_to_label[link["source"]], "target": name_to_label[link["target"]], "value": link["value"]}
        for link in links
    ]

    # --- Agregar valores y porcentajes al label de cada nodo ---
    nodes = []
    for node in raw_nodes:
        name = node["name"]
        level = node["level"]
        value = node_values.get(name, 0)
        total = level_totals[level]
        percentage = (value / total * 100) if total > 0 else 0
        label = f"{name}\n{value:.0f} ({percentage:.0f}%)"
        nodes.append({"name": label})

    # --- Crear gráfico Sankey ---
    chart = (
        Sankey()
        .add(
            "Flujos",
            nodes=nodes,
            links=updated_links,
            linestyle_opt=opts.LineStyleOpts(curve=0.5, opacity=0.5),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Sankey con valores y porcentajes por nivel"))
    )

    # --- Mostrar en Streamlit ---
    st.title("Sankey con valores y % por nivel")
    st_pyecharts(chart)

