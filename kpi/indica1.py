import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import locale
from script.exportaciones import mosto_registro_mensual
from streamlit_card import card
from streamlit_kpi import streamlit_kpi




def indica1(dv1):

  despachos = card(
        title="Despachos",
        text="Some description",
        image="http://placekitten.com/200/300",
        styles={
          "card": {
              "width": "200px",
              "height": "200px",
              "border-radius": "10px",
              "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
          },
          "text": {
              "font-family": "serif",
          }
      }        
  )
