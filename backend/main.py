from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse
from typing import Annotated
import pickle
import pandas as pd

app = FastAPI()
model = pickle.load(open('model/trained_pipeline.pkl','rb'))

def predict(data):
    input = pd.DataFrame([data.dict()])
    prediction = model.predict(input) 
    return prediction[0]

class InputModel(BaseModel):
    City:Annotated[str, Field(..., description='Name of the city')]
    Location:Annotated[str, Field(..., description='Location of the house')]
    Price_per_sqft:Annotated[float, Field(..., description='Price per square feet')]
    Area:Annotated[float, Field(..., description='Total area of the house')]
    Bedrooms:Annotated[int, Field(..., description='No. of bedrooms available')]
    Gymnasium:Annotated[int, Field(..., description='Gym service availability')]
    SwimmingPool:Annotated[int, Field(..., description='Swimming pool serviec available')]
    Resale:Annotated[bool, Field(..., description='House is for resale')]
    AC:Annotated[int, Field(..., description='No. of AC machines provided')]
    Gasconnection:Annotated[int, Field(..., description='No. of gas connections')]

class PredictedPrice(BaseModel):
    Price:Annotated[float, Field(...,description='Predicted price of the house')]

@app.get('/')
def home():
    return {'message': 'House Price Prediction System'}

@app.post('/predict',response_model=PredictedPrice)
def get_recommendation(data:InputModel):
    try:
        price = predict(data)
        return JSONResponse(status_code=200, content={'price': price})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))