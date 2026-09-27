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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('model.pkl')

class PropertyData(BaseModel):
    city: str
    locality: str
    area_sqft: float
    bhk: int
    balcony: str
    property_type: str
    furnished_status: str
    property_age: str
    amenities_score: int

@app.post("/predict")
def predict_price(data: PropertyData):
    start_time = time.time()
    
    input_data = pd.DataFrame([{
        'city': data.city,
        'locality': data.locality,
        'area_sqft': data.area_sqft,
        'bhk': data.bhk,
        'balcony': data.balcony,
        'property_type': data.property_type,
        'furnished_status': data.furnished_status,
        'property_age': data.property_age,
        'amenities_score': data.amenities_score
    }])
    
    prediction = model.predict(input_data)[0]
    execution_time = round((time.time() - start_time) * 1000, 2)
    
    return {
        "predicted_price": round(float(prediction), 2),
        "latency_ms": f"{execution_time} ms"
    }