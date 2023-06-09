# -*- coding: utf-8 -*-
"""dashboard_police.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WxguOuyu8cFrjBCfDj0EqOB23URegLzy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import matplotlib.pyplot as plt

# Página completa
st.set_page_config(layout="wide")

# Se agrega columnas para poner el logo del departamento
col1, col2 = st.columns([5, 1])
with col1:
    st.title("Police Incident Reports from 2018 to 2020 in San Francisco")
    # Agregar una breve instruccion con emoji para mayor interactividad
    st.subheader(":arrow_left: Use the filters in the sidebar to navigate and explore the information")

    df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

    st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.")

    mapa = pd.DataFrame()
    mapa["Date"] = df["Incident Date"]
    mapa["Year"] = pd.to_datetime(df["Incident Date"]).dt.year
    mapa["Day"] = df["Incident Day of Week"]
    mapa["Police District"] = df["Police District"]
    mapa["Neighborhood"] = df["Analysis Neighborhood"]
    mapa["Incident Category"] = df["Incident Category"]
    mapa["Incident Subcategory"] = df["Incident Subcategory"]
    mapa["Resolution"] = df["Resolution"]
    mapa["lat"] = df["Latitude"]
    mapa["lon"] = df["Longitude"]
    mapa = mapa.dropna()

    subset_data2 = mapa
    police_district_input = st.sidebar.multiselect(
        'Police District',
        mapa.groupby('Police District').count().reset_index()['Police District'].tolist()
    )
    if len(police_district_input) > 0:
        subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

    subset_data1 = subset_data2
    neighborhood_input = st.sidebar.multiselect(
        'Neighborhood',
        subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist()
    )
    if len(neighborhood_input) > 0:
        subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

    subset_data = subset_data1
    incident_input = st.sidebar.multiselect(
        'Incident Category',
        subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
    )
    if len(incident_input) > 0:
        subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

    # Selección del año mediante un selectbox en el sidebar
    selected_year = st.sidebar.selectbox("Select Year", sorted(mapa['Year'].unique()))

    # Filtrar los datos por el año seleccionado
    subset_data = subset_data[subset_data['Year'] == selected_year]

    subset_data

    # Cambiar orden de gráficos para ir de lo general a lo particular
    # MAPA
    st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')
    st.subheader('Crime locations in San Francisco')
    st.map(subset_data)

    # GRÁFICA 2 (Editada para escala de color)
    st.subheader('Type of crimes committed')
    # Obtener el conteo de cada categoría de incidente
    incident_counts = subset_data['Incident Category'].value_counts()
    # Definir colores nuevos para la gráfica
    color_range = ["#250407", "#ba1424"]
    # Crear la gráfica de barras
    fig = px.bar(
        x=incident_counts.index,
        y=incident_counts.values,
        color=incident_counts.values,
        color_continuous_scale=['#250407', '#ba1424']
    )
    fig.update_layout(
        xaxis_title="Incident Category",
        yaxis_title="Number of Incidents",
        title="Type of Crimes Committed"
    )
    st.plotly_chart(fig)

    # GRÁFICA 3
    st.subheader('Crimes occurred per date')
    st.line_chart(subset_data['Date'].value_counts())

    # GRÁFICA 4 (Cambiar a ploty para colocar una escala de color)
    st.subheader('Crimes occurred per day of the week')
    fig4 = px.bar(subset_data['Day'].value_counts(), color=subset_data['Day'].value_counts(), color_continuous_scale='Blues')
    st.plotly_chart(fig4)

    # GRÁFICA 5
    agree = st.button('Click to see Incident Subcategories')
    if agree:
        st.subheader('Subtype of crimes committed')
        st.bar_chart(subset_data['Incident Subcategory'].value_counts())

    # GRÁFICA 6 (Cambiar a ploty para colocar una escala de color)
    st.subheader('Resolution status')
    fig6 = px.pie(subset_data, names='Resolution', color_discrete_sequence=px.colors.sequential.Cividis)
    st.plotly_chart(fig6)

with col2:
    st.image("Logo_Police.jpg", width=150)