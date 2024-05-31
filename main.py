#####################################################################
# This is the main for the service that is used to detect grass and
# weed in an image. It uses the Custom Vision API to detect the
# objects in the image.
#####################################################################

# IMPORT LIBRARIES
# 1. import libraries that are part of the standard python library

from logging import Logger

# 2. import other third party libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 3. import my own libraries


app = FastAPI()

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
    return {"greetings": "Hello, and welcome to Azure AI and Python!"}
