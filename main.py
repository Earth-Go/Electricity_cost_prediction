from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
from pydantic import BaseModel , Field, computed_field
import pickle 
import os
import requests
import pandas as pd
import joblib

MODEL_URL = "https://github.com/Earth-Go/Electricity_cost_predictor/releases/download/v1.0/model.pkl"
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    response = requests.get(MODEL_URL)
    if response.status_code == 200:
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download model.pkl: {response.status_code}")

# Load the model
model = joblib.load(MODEL_PATH)

app= FastAPI()

class Input(BaseModel):
    site_area: Annotated[int , Field(..., description="enter the site area!" , gt=0)]
    structure_type:Annotated[Literal["Mixed-use", "Industrial", "Commercial" , "Residential"] ,Field(..., description="enter the structure type!" ) ]
    water_consumption:Annotated[int , Field(..., description="enter the water_consumption!" , gt=0)]
    recycling_rate:Annotated[int , Field(..., description="enter the recycling_rate!" , gt=0)]
    utilisation_rate:Annotated[int , Field(..., description="enter the utilisation_rate!" , gt=0)]
    air_qality_index:Annotated[int , Field(..., description="enter the air_qality_index!" , gt=0)]
    issue_reolution_time:Annotated[int , Field(..., description="enter the issue_reolution_time!" , gt=0)]
    resident_count:Annotated[int , Field(..., description="enter the resident_count!" , gt=0)]

@app.post("/predict")
def predict_cost(data : Input):
    input_df = pd.DataFrame([{
        'site area':data.site_area,
        'structure type': data.structure_type,
        'water consumption':data.water_consumption,
        'recycling rate':data.recycling_rate,
        'utilisation rate':data.utilisation_rate,
        'air qality index':data.air_qality_index,
        'issue reolution time':data.issue_reolution_time,
        'resident count':data.resident_count
    }])

    prediction =model.predict(input_df)[0]
    return JSONResponse(status_code=200 , content=("Predicted Cost is : " , prediction))

