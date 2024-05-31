from enum import Enum

DETECTED_TYPE_GRASS = "Grass"
DETECTED_TYPE_WEED = "Weed"

BOUNDING_BOX_COLOR_GRASS = "#FFDF00"
BOUNDING_BOX_COLOR_WEED = "red"

# config elements
CONFIG_PROJECT_NAME = "ProjectName"
CONFIG_DEPLOYED_NAME = "DeployedName"
CONFIG_PREDICTION_ENDPOINT = "PredictionEndpoint"
CONFIG_PREDICTION_KEY = "PredictionKey"
CONFIG_PROJECT_ID = "ProjectId"
CONFIG_STORAGE_ACCOUNT = "StorageAccount"


DetectionType = Enum("DetectionType", ["WEED", "GRASS", "BOTH"])
