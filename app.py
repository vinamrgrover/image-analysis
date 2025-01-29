from fastapi import FastAPI
from models import Image
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get("/api/v1")
async def get_root():
    return {"message": "Welcome to the image analysis API!"}


@app.get("/api/v1/image/description")
async def get_description(image_url: str):
    i = Image(image=image_url)
    return dict(i.get_image_description())


@app.get("/api/v1/image/analysis")
async def get_description(image_url: str):
    i = Image(image=image_url)
    return dict(i.get_image_analysis())


@app.get("/api/v1/image/sentiment")
async def get_description(image_url: str):
    i = Image(image=image_url)
    return dict(i.get_image_sentiment())
