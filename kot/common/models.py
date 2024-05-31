import os
from dotenv import load_dotenv
from kot.common import constants
from pydantic import BaseModel


class GrassPredictionData:
    def __init__(self, name: str, confidence_level: int, bounding_box: any) -> None:
        self.name = name
        self.confidence_level = confidence_level
        self.bounding_box = bounding_box


class MarkedDetectedArea:
    def __init__(self) -> None:
        self.name = None
        self.confidence_level = None
        self.bounding_box = None
        self.marked_color = None

    # def __init__(
    #    self, name: str, confidence_level: int, bounding_box: any, marked_color: str
    # ) -> None:
    #    self.name = name
    #    self.confidence_level = confidence_level
    #    self.bounding_box = bounding_box
    #    self.marked_color = marked_color


class GrassAnalysisResponse:
    def __init__(self, image: bytes, detected_details: list[GrassPredictionData]) -> None:
        self.image = image
        self.detected_details = detected_details    

class Config:
    def __init__(self) -> None:
        self.project_name = None
        self.deployed_name = None
        self.prediction_endpoint = None
        self.prediction_key = None
        self.project_id = None
        self.storage_account = None

    def load(self):
        load_dotenv()
        self.project_name = os.getenv(constants.CONFIG_PROJECT_NAME)
        self.deployed_name = os.getenv(constants.CONFIG_DEPLOYED_NAME)
        self.prediction_endpoint = os.getenv(constants.CONFIG_PREDICTION_ENDPOINT)
        self.prediction_key = os.getenv(constants.CONFIG_PREDICTION_KEY)
        self.project_id = os.getenv(constants.CONFIG_PROJECT_ID)
        self.storage_account = os.getenv(constants.CONFIG_STORAGE_ACCOUNT)
