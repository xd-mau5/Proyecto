from pydantic import BaseModel
from pydantic import Field
import pandas as pd
import joblib

class InputModel(BaseModel):
    fecha: str = Field(..., description="Fecha de la predicción", example="2021-01-01"
    )

class OutputModel(BaseModel):
    prediction: str = Field(..., description="Predicción de la cantidad de accidentes", example=1000)

class APIResponse:
    def __init__(self, fecha):
        self.fecha = fecha

    def _cargar_modelo(self):
        self.modelo = joblib.load("model.pkl")

    def _preprocesar_datos(self):
        fecha = self.fecha
        fecha = pd.to_datetime(fecha)
        self.fecha = fecha

    def predict(self):
        self._cargar_modelo()
        self._preprocesar_datos()
        prediction = self.modelo.predict(self.fecha)
        return prediction