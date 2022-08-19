import datetime
import os
from xmlrpc.client import boolean
import requests
from typing import Any, List, Optional

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from mangum import Mangum
import boto3

from models import Cluster
import db
import conf
import auth
import processing

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:3000",
    "http://skycolours.fifthcontinent.io",
    "https://sky.kip.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
client = boto3.client("s3")


@app.get("/")
def read_root():
    return {"urls": ["/docs", "/api/v1/colourclusters"]}


@app.post("/api/v1/colourclusters", dependencies=[Depends(auth.has_access)])
async def save_image_colours(
    image: UploadFile = File(...), count: int = 5, save: Optional[bool] = None
):
    pixels = processing.get_pixels(image.file)
    colours = processing.get_colour_values(pixels, clusters=count)
    data: Cluster = Cluster.parse_obj(
        {
            "colours": colours,
            "date": datetime.datetime.now(),
        }
    )
    if save:
        print("Saving")
        connection = db.get_database()
        connection.colours.insert_one(data.dict())

    return data


@app.post("/api/v1/message/", dependencies=[Depends(auth.has_access)])
def send_message(data):
    send_text = (
        "https://api.telegram.org/bot"
        + conf.BOT_TOKEN
        + "/sendMessage?chat_id="
        + conf.BOT_CHATID
        + "&parse_mode=Markdown&text="
        + data.message
    )
    response = requests.get(send_text)
    return response.json()


@app.post("/api/v1/colourclusters/image", dependencies=[Depends(auth.has_access)])
async def save_image(image: UploadFile = File(...)):
    print(image.file, conf.BUCKET, os.path.join("images", image.filename))
    response = client.upload_fileobj(
        image.file, conf.BUCKET, os.path.join("images", image.filename)
    )

    return {"filename": image.filename}


@app.get("/api/v1/colourclusters")
def get_all(latest: bool = False, limit: int = 100, offset: int = 0) -> List[Cluster]:
    connection = db.get_database()
    data = (
        connection.colours.find({}, projection={"_id": False})
        .sort("date", -1)
        .skip(offset)
        .limit(limit)
    )
    return list(data)


@app.get("/api/v1/colourclusters/{date}")
def get(date: datetime.date) -> List[Cluster]:
    connection = db.get_database()
    zero_datetime = datetime.datetime.combine(date, datetime.datetime.min.time())
    return list(
        connection.colours.find(
            {
                "$and": [
                    {"date": {"$lt": zero_datetime + datetime.timedelta(days=30)}},
                    {"date": {"$gt": zero_datetime}},
                ]
            }
        ).sort("date", -1)
    )


def custom_schema():
    DOCS_TITLE = "Colour Clusters API V1"
    DOCS_VERSION = "1.0"
    openapi_schema = get_openapi(
        title=DOCS_TITLE,
        version=DOCS_VERSION,
        routes=app.routes,
    )
    return openapi_schema


app.openapi_schema = custom_schema()

handler = Mangum(app)  # type: ignore
