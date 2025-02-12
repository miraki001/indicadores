import streamlit as st
import streamlit.components.v1 as components
from pivottablejs import pivot_ui
import pandas as pd

iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)

t = pivot_ui(iris)

with open(t.src) as t:
    components.html(t.read(), width=900, height=1000, scrolling=True)
