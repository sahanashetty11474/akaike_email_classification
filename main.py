from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils import preprocess, mask_pii
import pickle

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

@app.post("/predict/")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    preprocessed_text = preprocess(text)
    prediction = model.predict([preprocessed_text])[0]
    masked_text = mask_pii(text) if prediction == 1 else text
    return JSONResponse(content={"prediction": int(prediction), "masked_text": masked_text})
