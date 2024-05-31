#####################################################################
# This is the main for the service that is used to detect grass and
# weed in an image. It uses the Custom Vision API to detect the
# objects in the image.
#####################################################################

# IMPORT LIBRARIES
# 1. import libraries that are part of the standard python library

import sys
import logging
from logging import Logger

# 2. import other third party libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

# 3. import my own libraries
from kot.grass_weed_detection import GrassWeedDetector
from kot.common.models import Config


def configure_logging() -> Logger:
    # Acquire the logger for this client library.
    logger = logging.getLogger("kot")
    logger.setLevel(logging.DEBUG)

    # Create a handler for stdout.
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def setup_logging() -> Logger:
    logger: Logger = None
    logger = configure_logging()
    return logger


def setup_config() -> Config:
    config = Config()
    config.load()
    return config


app = FastAPI()
logger = setup_logging()
config = setup_config()
detector = GrassWeedDetector(config, logger)
logger.debug("app started...")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    detector.display()
    return {"greetings": "Hello, and welcome to Azure AI and Python!"}


@app.get("/image")
def read_root():
    image_path = "grass-analyzed.jpg"
    with open(image_path, "rb") as image_file:
        return Response(image_file.read(), media_type="image/jpeg")


@app.post(
    "/analyze",
)
async def analyze(file: UploadFile = File(...)):
    logger.debug("analyze called")
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    logger.debug(f"file: {file.filename}")

    file_extension = file.filename.split(".")[-1]

    # read the image as bytes
    image = None
    try:
        image = await file.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=400, detail="Error reading file")

    # call the detector to analyze the image
    result = detector.analyze(image, 2)
    print("result:", result)
    logger.debug("analyzed image...")

    # prefer to return the image as bytes rather than saving to disk
    # return Response(result.image, media_type="image/jpeg")

    # but for now return a message, and do a fetch to get the image
    return JSONResponse(content={"message": "image analysis complete."})


# uvicorn --reload api:app
