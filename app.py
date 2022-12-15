import streamlit as st
import pandas as pd
from holidays_co import is_holiday_date
import plotly.express as px
import plotly.graph_objects as go
import requests
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
def request_api(DIA, MES, ETAREO, GENERO, FESTIVO):
    request_data = [{"DIA": DIA, "MES": MES, "ETAREO": ETAREO, "GENERO": GENERO, "FESTIVO": FESTIVO}]
    data_cleaned = str(request_data).replace("'", '"')
    url_api = ''
    prediction = requests.post(url_api, data=data_cleaned).text
    df_prediction = pd.read_json(prediction)
    return df_prediction
pages = ['Inicio', 'Tablas', 'Gráficas']
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
        dia = st.sidebar.number_input('Día', min_value=1, max_value=31, value=1)
        mes = st.sidebar.number_input('Mes', min_value=1, max_value=12, value=1)
        festivo = st.sidebar.selectbox('Festivo', ['SI', 'NO'])


        if st.button('Realizar predicción'):
            df_prediction = request_api(dia, mes, festivo)
            st.write(df_prediction)
if __name__ == '__main__':
    run_UI()
