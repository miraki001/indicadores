import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import locale
from script.exportaciones import mosto_registro_mensual
from streamlit_kpi import streamlit_kpi
from streamlit_product_card import product_card 
from despachos import desp_consumo


def handle_card_click(card_name):
    st.session_state.click_message = f"'{card_name}' was clicked!"
    st.toast(f"Clicked: {card_name}")
    desp_consumo.despachos_consumo() 



def indica1(dv1):
    product_card(
        product_name="2.3%",
        description='Despachos 2024', 
        price=345.345,       
        product_image='https://enolife.com.ar/es/wp-content/uploads/2025/06/Imagen1-10-1024x440.jpg', 
        picture_position="left",
        image_aspect_ratio="3/2",
        button_text=None,   
        on_button_click=lambda: handle_card_click("Clickable Card Area"),
        key="core_name_only"
    )
