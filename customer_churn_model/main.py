
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# 1. Load the saved model with exception handling
try:
    model = joblib.load('customer_churn_model.joblib')
except FileNotFoundError:
    raise Exception("Model file not found, please ensure the file path is correct.")

# 2. Create a FastAPI app
app = FastAPI()

# 3. Define the input data format with optional validation
class CustomerData(BaseModel):
    SeniorCitizen: int
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: int
    InternetService: int
    PaymentMethod: int

    # You can add custom validation if needed, for example:
    # @root_validator
    # def check_total_charges(cls, values):
    #     total_charges = values.get('TotalCharges')
    #     if total_charges <= 0:
    #         raise ValueError("TotalCharges must be positive.")
    #     return values

# 4. Create a predict route
@app.post("/predict")
def predict_churn(data: CustomerData):
    # Convert input into numpy array
    input_features = np.array([[ 
        data.SeniorCitizen, data.tenure, data.MonthlyCharges,
        data.TotalCharges, data.Contract, data.InternetService, data.PaymentMethod
    ]])
    
    # Predict churn
    try:
        prediction = model.predict(input_features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")
    
    # Map 0 -> No Churn, 1 -> Churn
    result = "Churn" if prediction[0] == 1 else "No Churn"
    return {"prediction": result}