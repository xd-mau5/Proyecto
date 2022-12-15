import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analisis de Datos", layout='wide')

def plot_time_series(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_traces(mode='lines')
    fig.update_layout(hovermode='x unified')
    return fig
@st.cache(allow_output_mutation=True)
# Carga de datos
def load_data():
    df = pd.read_csv('Reporte_Lesiones_Personales_y_en_Accidente_de_Tr_nsito_Polic_a_Nacional.csv', low_memory=False)
    return df
df = load_data()
df = df.dropna()
df = df.drop('CODIGO DANE', axis=1)
df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], format='%d/%m/%Y')
df = pd.DataFrame(df)
st.plotly_chart(plot_time_series(df, 'FECHA HECHO', 'CANTIDAD', 'Total de Lesionados por Fecha'), use_container_width=True)