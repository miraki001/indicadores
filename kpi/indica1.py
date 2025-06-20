import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import locale
from script.exportaciones import mosto_registro_mensual
from streamlit_kpi import streamlit_kpi
from streamlit_product_card import product_card 




def indica1(dv1):
    product_card(
        product_name="Product Name Only",
        description=None, 
        price=None,       
        product_image=None, 
        button_text=None,   
        key="core_name_only"
    )
