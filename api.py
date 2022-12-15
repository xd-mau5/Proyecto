from fastapi import FastAPI
from typing import List
from classes import OutputModel, InputModel, APIResponse

app = FastAPI(title="API para la predicción de accidentes de lesiones personales y en accidentes de tránsito en Colombia con fechas específicas usando modelos de Machine Learning", description="Esta API permite realizar predicciones de la cantidad de accidentes de tránsito en Colombia", version="1.0.0")

@app.post("/predict", response_model=List[OutputModel])
async def predict(input: List[InputModel]):
    response = []
    for i in input:
        api_response = APIResponse(fecha=i.fecha)
        prediction = api_response.predict()
        response.append(OutputModel(prediction=prediction))
    return response