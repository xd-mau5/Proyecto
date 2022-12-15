import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import joblib


import pandas as pd


st.set_page_config(page_title="App Bonita", layout='wide')
#importamos datos del repo del profe :)


def plot_heatmap(df: pd.DataFrame, x: str, y: str = 'left'):
    data_heatmap = (
        df.reset_index()[[x, y, "index"]]
            .groupby([x, y])
            .count()
            .reset_index()
            .pivot(x, y, "index")
            .fillna(0)
    )
    fig = px.imshow(
        data_heatmap,
        color_continuous_scale="Reds",
        aspect="auto",
        title=f"Heatmap {x} vs {y}",
    )
    fig.update_traces(
        hovertemplate="<b><i>"
                      + x
                      + "</i></b>: %{y} <br><b><i>"
                      + y
                      + "</i></b>: %{x} <br><b><i>Conteo interacción variables</i></b>: %{z}<extra></extra>"
    )
    return fig


@st.cache(allow_output_mutation=True)
def cargar_datos(lol='lol'):
    df = pd.read_csv('https://raw.githubusercontent.com/JECaballeroR/DiplomadoPythonModulo6Cohorte2/master/datos.csv')
    model = joblib.load('logistica.pkl')
    return df, model
df, model = cargar_datos()


opciones = list(df.columns)

opciones.pop(opciones.index('left'))

st.sidebar.header('Holi')




st.sidebar.header("Elija los valores de la variable para el modelo")

satisfaction_level = st.sidebar.slider(label='Satisfacción', min_value=0.0, max_value=1.0, step=0.01,value= 0.69)
last_evaluation = st.sidebar.slider(label='Ultima evaluación de desempeño', min_value=0.0, max_value=1.0, step=0.01,value= 0.42)
number_project = st.sidebar.number_input(label='Numero de proyectos', min_value=1, max_value=10, step=1,value= 5)
average_montly_hours = st.sidebar.number_input(label='Horas mensuales trabajadas', min_value=96, max_value=310, step=1,value= 137)
time_spend_company = st.sidebar.number_input(label='Tiempo en compañia', min_value=1, max_value=10, step=1,value= 2)
Work_accident = int(st.sidebar.checkbox("¿ha tenido accidente de trabajo?"))
promotion_last_5years=int(st.sidebar.checkbox("¿ha tenido algún ascenso en los últimos 5 años?"))
sales = st.sidebar.selectbox(label='Departamento', options=list(df['sales'].unique()))
salary = st.sidebar.selectbox(label='Salario', options=list(df['salary'].unique()))

col1, col2 = st.columns(2)
col1.write("PyCharm xd by Omar")

seleccion = col1.selectbox(label='Columna X a elegir del DataFrame', options=opciones, index=1)
opciones2=opciones.copy()
opciones2.pop(opciones.index(seleccion ))
seleccion2 = col1.selectbox(label='Columna Y a elegir del DataFrame', options=opciones2, index=1)

col1.plotly_chart( plot_heatmap(df, x=seleccion, y=seleccion2), use_container_width=True)

col2.dataframe(df)
def crear_binarios(prefijo, eleccion_usuario, lista_columnas_xtrain):
    return [int(f"{prefijo}_{eleccion_usuario}" == x) for x in lista_columnas_xtrain]

if st.sidebar.button(":v"):
    st.balloons()
    salary_binarios = [int(f"salary_{salary}" == x) for x in ["salary_low", "salary_medium"]]
    dept_binarios = crear_binarios(
        "dept",
        sales,
        [
            "dept_RandD",
            "dept_accounting",
            "dept_hr",
            "dept_management",
            "dept_marketing",
            "dept_product_mng",
            "dept_sales",
            "dept_support",
            "dept_technical",
        ],
    )
    X_val = pd.DataFrame(
        data=[
            [
                satisfaction_level,
                last_evaluation,
                number_project,
                average_montly_hours,
                time_spend_company,
                Work_accident,
                promotion_last_5years,
                *dept_binarios,
                *salary_binarios
            ]
        ],
        # columnas del X_train
        columns=[
            "satisfaction_level",
            "last_evaluation",
            "number_project",
            "average_montly_hours",
            "time_spend_company",
            "Work_accident",
            "promotion_last_5years",
            "dept_RandD",
            "dept_accounting",
            "dept_hr",
            "dept_management",
            "dept_marketing",
            "dept_product_mng",
            "dept_sales",
            "dept_support",
            "dept_technical",
            "salary_low",
            "salary_medium",
        ],
    )

    #st.write(df[seleccion].unique())
    #st.write(X_val)

    if model.predict(X_val)==1:
        prediccion='Va a dejar la compañía, lloremos :('
    else:
        prediccion='Se queda el papu'
    st.write(f'La predicción del modelo es: {prediccion}')

else:
    st.write("No se ha oprimido el botón en la última corrida")
