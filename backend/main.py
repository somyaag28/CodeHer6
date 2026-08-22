from fastapi import FastAPI
from matching import match_image

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CodeHer6 API is running"}


@app.post("/identify")
def identify():
    product = match_image()
    return product
