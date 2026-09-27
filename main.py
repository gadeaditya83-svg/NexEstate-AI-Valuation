from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model.pkl")

class PropertyInputs(BaseModel):
    location: str
    area_sqft: float
    bhk: int
    balcony: str
    property_type: str
    furnished_status: str
    property_age: str
    amenities_score: float

@app.post("/predict")
def predict_valuation(data: PropertyInputs):
    start_time = time.time()
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    latency = round((time.time() - start_time) * 1000, 2)
    
    return {
        "predicted_price": round(prediction, 2),
        "latency_ms": f"{latency} ms"
    }