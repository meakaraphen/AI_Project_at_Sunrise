from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load trained model
model = joblib.load("api_churn_model.pkl")

# Pydantic model for request
class ChurnInput(BaseModel):
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    Contract_Month_to_month: int = Field(..., alias="Contract_Month-to-month")
    InternetService_Fiber_optic: int = Field(..., alias="InternetService_Fiber optic")
    TechSupport_No: int
    OnlineSecurity_No: int
    PaymentMethod_Electronic_check: int = Field(..., alias="PaymentMethod_Electronic check")

    class Config:
        allow_population_by_field_name = True

# FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Churn Prediction API is live 🚀"}

@app.post("/predict")
def predict_churn(data: ChurnInput):
    try:
        input_df = pd.DataFrame([data.dict(by_alias=True)])
        logging.debug(f"Input DataFrame:\n{input_df}")
        prediction = model.predict(input_df)[0]
        return {"churn_prediction": int(prediction)}
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error(f"Prediction error: {error_details}")
        return {"error": f"Prediction failed: {str(e)}"}