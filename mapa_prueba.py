# -*- coding: utf-8 -*-
"""apuntes3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16HOvE3mxIiCTv9EJsRMz-bKhCh5xXhM-
"""

import streamlit as st
import pandas as pd

st.title("Police Incident Reports from 2018 to 2020 in San Francisco")

df = pd.read_csv("https://drive.google.com/file/d/11oLcKiW8SgCOp3tGiQCYuRG7pLL_J-Zf/view?usp=drive_link")

st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.")

# Obtener las coordenadas de todas las filas del dataframe
sf_coords = df[['Latitude', 'Longitude']]

# Mostrar el mapa de San Francisco con los marcadores de todas las ubicaciones
st.map(sf_coords)
