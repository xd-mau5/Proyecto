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
        # Bienvenido al dashboard del análisis de lesiones personales y accidentes de tránsito en Colombia
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
        tabs1, tabs2, tabs3 = st.tabs([f"🗃Tabla {i}" for i in range(1, 4)])
        with tabs1.container():
            tabs1.subheader('Cantidad de accidentes por fecha')
            tabs1.subheader('Filtros para la tabla')
            tabs1.write("Seleccione el rango de fechas para ver la cantidad de accidentes por fecha")
            tabs1.write('Nota: Los datos de la tabla se actualizan cada vez que se cambia el rango de fechas')
            min_date = tabs1.date_input('Fecha mínima', value=df['FECHA HECHO'].min(),     min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
            max_date = tabs1.date_input('Fecha máxima', value=df['FECHA HECHO'].max(),     min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
            tabs1.table(df[(df['FECHA HECHO'] >= pd.to_datetime(min_date)) & (df['FECHA HECHO'] <= pd. to_datetime(max_date))].groupby(by='FECHA HECHO')['FECHA HECHO'].count().reset_index (name='Cantidad'))
        with tabs2.container():
            tabs2.subheader('Cantidad de accidentes por fecha y departamento')
            tabs2.subheader('Filtros para la tabla')
            tabs2.markdown(
                'Seleccione el rango de fechas y el departamento para ver la cantidad de accidentes por fecha y departamento'+'<br>' + '**Nota:** Los datos de la tabla se actualizan cada vez que se cambia el rango de fechas o el departamento', unsafe_allow_html=True
                )
            min_date2 = tabs2.date_input('Fecha mínima', value=df['FECHA HECHO'].min(),    min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=100)
            max_date2 = tabs2.date_input('Fecha máxima', value=df['FECHA HECHO'].max(),    min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=101)
            departamento = tabs2.selectbox('Departamento', df['DEPARTAMENTO'].unique())
            tabs2.markdown('**Departamento de: {}**'.format(departamento))
            tabs2.table(df[(df['FECHA HECHO'] >= pd.to_datetime(min_date2)) & (df['FECHA HECHO'] <= pd.    to_datetime(max_date2)) & (df['DEPARTAMENTO'] == departamento)].groupby(by='FECHA HECHO')   ['FECHA HECHO'].count().reset_index(name='Cantidad'))
        with tabs3.container():
            tabs3.subheader('Cantidad de accidentes por fecha, departamento y municipio')
            tabs3.subheader('Filtros para la tabla')
            tabs3.markdown(
                'Seleccione el rango de fechas, el departamento y el municipio para ver la cantidad de accidentes por fecha, departamento y municipio'+'<br>' + '**Nota:** Los datos de la tabla se actualizan cada vez que se cambia el rango de fechas, el departamento o el municipio', unsafe_allow_html=True
                )
            min_date3 = tabs3.date_input('Fecha mínima', value=df['FECHA HECHO'].min(),    min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=200)
            max_date3 = tabs3.date_input('Fecha máxima', value=df['FECHA HECHO'].max(),    min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max(), key=201)
            departamento3 = tabs3.selectbox('Departamento', df['DEPARTAMENTO'].unique(), key=300)
            municipio3 = tabs3.selectbox('Municipio', df[df['DEPARTAMENTO'] == departamento3]['MUNICIPIO'].unique(), key=400)
            tabs3.markdown('**Departamento de: {}**'.format(departamento3))
            tabs3.markdown('**Municipio de: {}**'.format(municipio3))
            tabs3.table(df[(df['FECHA HECHO'] >= pd.to_datetime(min_date3)) & (df['FECHA HECHO'] <= pd.    to_datetime(max_date3)) & (df['DEPARTAMENTO'] == departamento3) & (df['MUNICIPIO'] == municipio3)].groupby(by='FECHA HECHO')['FECHA HECHO'].count().reset_index(name='Cantidad'))

    if page == 'Gráficas':
        tab1, tab2, tab3 = st.tabs(['📈Gráfica 1', '📈Gráfica 2', '📈Gráfica 3'])
        tab1.header('Cantidad de accidentes por fecha')
        tab1.subheader('Filtros para la gráfica 1')
        with tab1.container():
            min_date_graph = tab1.date_input('Fecha mínima', value=df['FECHA HECHO'].min(),   min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
            max_date_graph = tab1.date_input('Fecha máxima', value=df['FECHA HECHO'].max(),   min_value=df['FECHA HECHO'].min(), max_value=df['FECHA HECHO'].max())
            fig = serie_tiempo(df, pd.to_datetime(min_date_graph), pd.to_datetime(max_date_graph),  'FECHA HECHO', 'CANTIDAD', 'Cantidad de accidentes por fecha')
            tab1.plotly_chart(fig, use_container_width=True)
        with tab2.container():
            tab2.subheader('Cantidad de accidentes de tránsito por departamento')
            tab2.container()
            df_lesiones = df.copy()
            df_lesiones[df_lesiones["DESCRIPCIÓN CONDUCTA"] == "LESIONES CULPOSAS ( EN ACCIDENTE DE     TRANSITO )"][["ARMAS MEDIOS"]].value_counts()
            df_lesiones = df_lesiones.groupby('DEPARTAMENTO').agg({'CANTIDAD': 'sum'}).reset_index()
            # sort by quantity of upper to lower
            fig2 = px.bar(df_lesiones.sort_values(by='CANTIDAD',ascending=False), x='DEPARTAMENTO', y='CANTIDAD', color_discrete_sequence= ['#f4d03f'])
            fig2.update_layout(
                title='Cantidad de accidentes de tránsito por departamento',
                xaxis_title='Departamento',
                yaxis_title='Cantidad de accidentes',
                font=dict(
                family="Cascadia Code, monospace",
                size=12
                )
            )
            fig2.update_traces(
                hovertemplate="<b>Departamento</b>: %{x} <br><b>Cantidad</b>: %{y}"
            )
            tab2.plotly_chart(fig2, use_container_width=True)
        with tab3.container():
            tab3.subheader('Cantidad de lesionados por tipo de arma o medio')
            tab3.subheader('Filtros para la gráfica 3')
            df_lesiones = df.copy()
            df_lesiones = df_lesiones.groupby('DESCRIPCIÓN CONDUCTA').agg({'CANTIDAD': 'sum'}).reset_index()
            conducta = tab3.selectbox('Tipo de arma o medio', df_lesiones['DESCRIPCIÓN CONDUCTA'].unique())
            df_lesiones = df[df['DESCRIPCIÓN CONDUCTA'] == conducta]
            df_lesiones = df_lesiones.groupby('ARMAS MEDIOS').agg({'CANTIDAD': 'sum'}).reset_index()
            fig3 = px.bar(df_lesiones.sort_values(by='CANTIDAD',ascending=False), x='ARMAS MEDIOS', y='CANTIDAD', color_discrete_sequence= ['#f4d03f'])
            fig3.update_layout(
                title='Cantidad de lesionados por tipo de arma o medio',
                xaxis_title='Tipo de arma o medio',
                yaxis_title='Cantidad de lesionados',
                font=dict(
                family="Cascadia Code, monospace",
                size=12
                )
            )
            fig3.update_traces(
                hovertemplate="<b>Tipo de arma o medio</b>: %{x} <br><b>Cantidad</b>: %{y}"
            )
            tab3.plotly_chart(fig3, use_container_width=True)


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
