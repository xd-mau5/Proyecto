from fastapi import FastAPI
from typing import List
import uvicorn
import pandas as pd
from classes import OutputModel, InputModel, APIResponse

app = FastAPI(title="API para la predicción de accidentes de lesiones personales y en accidentes de tránsito en Colombia con fechas específicas usando modelos de Machine Learning", description="Esta API permite realizar predicciones de la cantidad de accidentes de tránsito en Colombia", version="1.0.0")

@app.post("/predict", response_model=List[OutputModel])
async def predict(input: InputModel):
    response = APIResponse(input.fecha)
    prediction = response.predict()
    return [OutputModel(prediction=prediction)]