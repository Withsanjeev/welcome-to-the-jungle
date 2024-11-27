from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the model (replace with your actual file path)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the request body model
class JobRequest(BaseModel):
    title: str  # This will be the input to your model (e.g., job title)

# Prediction function
def make_prediction(title: str) -> dict:
    # Your preprocessing logic goes here if needed
    input_data = [title]  # For simplicity, using title directly; adjust based on your model
    prediction = model.predict(input_data)  # Use your model to predict

    return {"prediction": prediction.tolist()}

# Define the endpoint to handle the POST request
@app.post("/predict", response_model=dict)
def predict(job_request: JobRequest):
    try:
        # Get predictions for the provided title
        result = make_prediction(job_request.title)
        return result
    except Exception as e:
        return {"error": str(e)}

# To run the app, use the following command in the terminal:
# uvicorn fastapi_api:app --reload
