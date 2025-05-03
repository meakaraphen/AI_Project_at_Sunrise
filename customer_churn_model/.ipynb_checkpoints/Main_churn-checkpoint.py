{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "ca3dc264-c543-44f3-88a0-c19387365b7d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# main.py\n",
    "from fastapi import FastAPI\n",
    "from pydantic import BaseModel\n",
    "import joblib\n",
    "import numpy as np\n",
    "\n",
    "# 1. Load the saved model\n",
    "model = joblib.load('customer_churn_model.joblib')\n",
    "\n",
    "# 2. Create a FastAPI app\n",
    "app = FastAPI()\n",
    "\n",
    "# 3. Define the input data format\n",
    "class CustomerData(BaseModel):\n",
    "    SeniorCitizen: int\n",
    "    tenure: int\n",
    "    MonthlyCharges: float\n",
    "    TotalCharges: float\n",
    "    Contract: int\n",
    "    InternetService: int\n",
    "    PaymentMethod: int\n",
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
    "    prediction = model.predict(input_features)\n",
    "    \n",
    "    # Map 0 -> No Churn, 1 -> Churn\n",
    "    result = \"Churn\" if prediction[0] == 1 else \"No Churn\"\n",
    "    return {\"prediction\": result}\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "342517fc-9efd-4bff-b2f2-4235f30f0690",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (3807844594.py, line 1)",
     "output_type": "error",
     "traceback": [
      "  \u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[7]\u001b[39m\u001b[32m, line 1\u001b[39m\n\u001b[31m    \u001b[39m\u001b[31muvicorn main:app --reload\u001b[39m\n            ^\n\u001b[31mSyntaxError\u001b[39m\u001b[31m:\u001b[39m invalid syntax\n"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "258422fa-7ed6-4b44-8d1b-d4796a88afbe",
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
