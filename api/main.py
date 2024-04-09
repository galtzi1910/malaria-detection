from fastapi import FastAPI, HTTPException, UploadFile
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import time

app = FastAPI()

model = tf.keras.models.load_model("../models/lenet_model.h5")

# TO RUN: uvicorn main:app --reload
# TO RUN (WITH WORKERS): uvicorn main:app --workers 4 --reload OR gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

@app.get("/")
def read_main():
    return "Please refer to the docs at /docs or /redoc"


@app.post("/uploadFile/")
def create_upload_file(im: UploadFile):
    start_time = time.time()
    if im.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="File format not supported")

    image = Image.open(BytesIO(im.file.read()))
    image = np.array(image)
    image = cv2.resize(image, (224, 224))
    image = np.float32(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    pred = model.predict(image)
    pred = float(pred[0][0])
    text = "Parasitized" if pred <= 0.5 else "Uninfected"

    return {
        "status": text,
        "prediction_value": pred,
        "time": time.time() - start_time,
        }
