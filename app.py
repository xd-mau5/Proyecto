import streamlit as st
import pandas as pd
from holidays_co import is_holiday_date
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
st.set_page_config(
    page_title="Presentacion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        Bienvenido al dashboard de lesiones personales y accidentes de tránsito en Colombia
        Esta aplicación fue desarrollada por el equipo 6 del diplomado de Python para el análisis de datos de la Universidad de Córdoba.

        Esta aplicación permite visualizar la cantidad de accidentes de tránsito en Colombia, así como la cantidad de lesiones personales por día, mes, y año.
        Además, permite realizar predicciones de la cantidad de accidentes de tránsito en Colombia
        
        Esto es el resultado del trabajo de:
        - Omar Alejandro Izquierdo Berrio
        - Tania Alexandra Florez Ramos
        - German Ricardo Orozco Villareal
        - Luis Manuel Roqueme
        - Fary Leonardo Urriaga Causil
        - Miguel Sebastián Nisperuza Sierra
        """
        }
    )
def serie_tiempo(data, min, max, x, y, title):
    # Filtrar por fecha
    data_range = data[(data[x] >= min) & (data[x] <= max)]
    # Agrupar los datos por fecha y sumar la cantidad
    data = data_range.groupby(by=x)[y].sum().reset_index()
    fig = px.line(data, x=x, y=y, title=title, color_discrete_sequence=['#F4D03F'],  render_mode='svg')
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad",
        font=dict(
            family="Cascadia Code, monospace",
            size=18,
            color="black"
        )
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(step="day", stepmode="backward", label="1 semana", count=7),
                    dict(step="month", stepmode="backward", label="1 mes", count=1),
                    dict(step="month", stepmode="backward", label="3 meses", count=3),
                    dict(label="Todos", step="all"),
                ]
            )
        )
    )
    fig.update_traces(
        hovertemplate="<b>Fecha</b>: %{x} <br><b>Cantidad</b>: %{y}"
    )
    return fig

pages = ['Inicio', 'Tablas', 'Gráficas', 'Predicción']
#st.title('Dashboard')
@st.cache(allow_output_mutation=True)
def cargar_datos():
    df = pd.read_csv('https://files.xd-mau5.xyz/Diplomado%20Python/Proyecto/Reporte_Lesiones_Personales_y_en_Accidente_de_Tr_nsito_Polic_a_Nacional.csv', low_memory=False)
    df = df.dropna()
    df = df.drop('CODIGO DANE', axis=1)
    df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], format='%d/%m/%Y')
    df = pd.DataFrame(df)
    df['DIA'] = df['FECHA HECHO'].dt.day
    df['MES'] = df['FECHA HECHO'].dt.month
    df['FESTIVO'] = df['FECHA HECHO'].apply(lambda x: 1 if is_holiday_date(x) else 0)
    df = pd.DataFrame(df)
    return df
df = cargar_datos()
def request_api(fecha):
    request_data = {'fecha': str(fecha)}
    #df = str(request_data).replace("'", '"')
    request_data = json.dumps(request_data)
    url_api = 'http://api.xd-mau5.xyz/predict'
    headers = {'Content-type': 'application/json'}
    # make a request like this fecha: "2023-01-01"
    response = requests.post(url_api, data=request_data, headers=headers, json=True)
    response = response.json()
    response = pd.DataFrame(response)
    return response["prediction"][0]


def run_UI():
    page = st.sidebar.selectbox('Selecciona una página', pages)
    if page == 'Inicio':
        st.markdown('''
        # Bienvenido al dashboard del analisis de lesiones personales y accidentes de transito en Colombia
        Este dashboard fue realizado por estudiantes de la Universidad de Córdoba, en el marco del diplomado de Python para el análisis de datos.
        
        ## Integrantes:
        - Omar Alejandro Izquierdo Berrio
        - Tania Alexandra Florez Ramos
        - German Ricardo Orozco Villareal
        - Luis Manuel Roqueme
        - Fary Leonardo Urriaga Causil
        - Miguel Sebastián Nisperuza Sierra
        ''')
    if page == 'Tablas':
        """# Tablas"""
        st.subheader('Cantidad de accidentes por fecha')
        st.sidebar.subheader('Filtros para la tabla 1')
        st.container()
        min_date = st.sidebar.date_input('Fecha mínima', value=df['FECHA HECHO'].min(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
        max_date = st.sidebar.date_input('Fecha máxima', value=df['FECHA HECHO'].max(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
        st.table(df[(df['FECHA HECHO'] >= pd.to_datetime(min_date)) & (df['FECHA HECHO'] <= pd.to_datetime(max_date))].groupby(by='FECHA HECHO')['FECHA HECHO'].count().reset_index(name='Cantidad'), height=500)
        st.subheader('Cantidad de accidentes por fecha y departamento')
        st.sidebar.subheader('Filtros para la tabla 2')
        st.container()
        min_date2 = st.sidebar.date_input('Fecha mínima', value=df['FECHA HECHO'].min(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=100)
        max_date2 = st.sidebar.date_input('Fecha máxima', value=df['FECHA HECHO'].max(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=101)
        departamento = st.sidebar.selectbox('Departamento', df['DEPARTAMENTO'].unique())
        st.table(df[(df['FECHA HECHO'] >= pd.to_datetime(min_date2)) & (df['FECHA HECHO'] <= pd.to_datetime(max_date2)) & (df['DEPARTAMENTO'] == departamento)].groupby(by='FECHA HECHO')['FECHA HECHO'].count().reset_index(name='Cantidad'), height=500)
        st.container()
    if page == 'Gráficas':
        st.subheader('Cantidad de accidentes por fecha')
        st.sidebar.subheader('Filtros para la gráfica 1')
        st.container()
        min_date = st.sidebar.date_input('Fecha mínima', value=df['FECHA HECHO'].min(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
        max_date = st.sidebar.date_input('Fecha máxima', value=df['FECHA HECHO'].max(), min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
        fig = serie_tiempo(df, pd.to_datetime(min_date), pd.to_datetime(max_date), 'FECHA HECHO', 'CANTIDAD', 'Cantidad de accidentes por fecha')
        st.plotly_chart(fig, use_container_width=True)
        st.container()
        st.subheader('Cantidad de accidentes por departamento')
        st.container()
        # Hacer una grafica por DESCRIPCION CONDUCTA = 'LESIONES CULPOSAS ( EN ACCIDENTE DE TRANSITO )' en total
        # Con un solo color difuminado
        df_lesiones = df.copy()
        df_lesiones[df_lesiones["DESCRIPCIÓN CONDUCTA"] == "LESIONES CULPOSAS ( EN ACCIDENTE DE TRANSITO )"][["ARMAS MEDIOS"]].value_counts()
        df_lesiones = df_lesiones.groupby('DEPARTAMENTO').agg({'CANTIDAD': 'sum'}).reset_index()
        fig = px.bar(df_lesiones, x='DEPARTAMENTO', y='CANTIDAD', color_discrete_sequence=['#f4d03f'])
        fig.update_layout(
            title='Cantidad de accidentes de transito por departamento',
            xaxis_title='Departamento',
            yaxis_title='Cantidad de accidentes',
            font=dict(
            family="Cascadia Code, monospace",
            size=12
            )
        )
        fig.update_traces(
            hovertemplate="<b>Departamento</b>: %{x} <br><b>Cantidad</b>: %{y}"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.container()
        st.container()
    if page == 'Predicción':
        st.header('Predicción')
        st.subheader('Realiza una predicción')
        st.write('Selecciona los parámetros para realizar la predicción')
        fecha = st.date_input('Fecha', value=df['FECHA HECHO'].max(), min_value=df['FECHA HECHO'].min())
        if st.button('Realizar predicción'):
            prediction = request_api(fecha)
            st.write('La predicción es de: ', prediction, 'accidentes en', fecha)
if __name__ == '__main__':
    run_UI()
