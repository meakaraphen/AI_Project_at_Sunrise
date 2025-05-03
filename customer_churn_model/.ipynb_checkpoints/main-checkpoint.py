{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ca3dc264-c543-44f3-88a0-c19387365b7d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# main.py\n",
    "from fastapi import FastAPI, HTTPException\n",
    "from pydantic import BaseModel\n",
    "import joblib\n",
    "import numpy as np\n",
    "\n",
    "# 1. Load the saved model with exception handling\n",
    "try:\n",
    "    model = joblib.load('customer_churn_model.joblib')\n",
    "except FileNotFoundError:\n",
    "    raise Exception(\"Model file not found, please ensure the file path is correct.\")\n",
    "\n",
    "# 2. Create a FastAPI app\n",
    "app = FastAPI()\n",
    "\n",
    "# 3. Define the input data format with optional validation\n",
    "class CustomerData(BaseModel):\n",
    "    SeniorCitizen: int\n",
    "    tenure: int\n",
    "    MonthlyCharges: float\n",
    "    TotalCharges: float\n",
    "    Contract: int\n",
    "    InternetService: int\n",
    "    PaymentMethod: int\n",
    "\n",
    "    # You can add custom validation if needed, for example:\n",
    "    # @root_validator\n",
    "    # def check_total_charges(cls, values):\n",
    "    #     total_charges = values.get('TotalCharges')\n",
    "    #     if total_charges <= 0:\n",
    "    #         raise ValueError(\"TotalCharges must be positive.\")\n",
    "    #     return values\n",
    "\n",
    "# 4. Create a predict route\n",
    "@app.post(\"/predict\")\n",
    "def predict_churn(data: CustomerData):\n",
    "    # Convert input into numpy array\n",
    "    input_features = np.array([[ \n",
    "        data.SeniorCitizen, data.tenure, data.MonthlyCharges,\n",
    "        data.TotalCharges, data.Contract, data.InternetService, data.PaymentMethod\n",
    "    ]])\n",
    "    \n",
    "    # Predict churn\n",
    "    try:\n",
    "        prediction = model.predict(input_features)\n",
    "    except Exception as e:\n",
    "        raise HTTPException(status_code=500, detail=f\"Model prediction failed: {e}\")\n",
    "    \n",
    "    # Map 0 -> No Churn, 1 -> Churn\n",
    "    result = \"Churn\" if prediction[0] == 1 else \"No Churn\"\n",
    "    return {\"prediction\": result}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "258422fa-7ed6-4b44-8d1b-d4796a88afbe",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "12c9fba9-b5dd-4695-8109-1265707323e5",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
