from pydantic import BaseModel
from pydantic import Field
import pandas as pd
from prophet import Prophet
import joblib

class InputModel(BaseModel):
    fecha: str = Field(..., description="Fecha de la predicción", example="2021-01-01"
    )

class OutputModel(BaseModel):
    prediction: str = Field(..., description="Predicción de la cantidad de accidentes", example=1000)

class APIResponse:
    def __init__(self, fecha):
        self.fecha = fecha
        fecha = pd.to_datetime(fecha)
        if fecha < pd.to_datetime('2010-01-01'):
            raise ValueError('La fecha debe ser mayor a 2010-01-01')

    def predict(self):
        df = pd.read_csv('https://files.xd-mau5.xyz/Diplomado%20Python/Proyecto/Reporte_Lesiones_Personales_y_en_Accidente_de_Tr_nsito_Polic_a_Nacional.csv', low_memory=False)
        df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'])
        df = df.groupby('FECHA HECHO')['FECHA HECHO'].count().reset_index(name='Cantidad')
        df = df.rename(columns={'FECHA HECHO': 'ds', 'Cantidad': 'y'})
        # cargar modelo
        model = joblib.load('model.pkl')
        # predecir
        future = model.make_future_dataframe(periods=1000, freq='D')
        forecast = model.predict(future)
        # obtener la predicción
        prediction = int(forecast[forecast['ds'] == self.fecha]['yhat'].values[0])
        return prediction