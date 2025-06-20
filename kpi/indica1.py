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
        product_name="Despachos",
        description='2024', 
        price=345.345,       
        product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
        picture_position="left",
        button_text=None,   
        key="core_name_only"
    )
