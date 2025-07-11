from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.inference import predict
from src.config import is_valid_api_key
import numpy as np
import cv2
import io
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_api_key(x_api_key: str = Header(...)):
    if not is_valid_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.post("/predict", dependencies=[Depends(verify_api_key)])
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image file")
        class_name, confidence = predict(image)
        return JSONResponse({
            "class_name": class_name,
            "confidence": float(confidence)
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/auth")
def auth_check(x_api_key: str = Header(...)):
    print(f"Received x_api_key: '{x_api_key}'")
    from src.config import is_valid_api_key
    if not is_valid_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"detail": "API Key valid"}