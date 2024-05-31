#####################################################################
# This is the main for the service that is used to detect grass and
# weed in an image. It uses the Custom Vision API to detect the
# objects in the image.
#####################################################################

# IMPORT LIBRARIES

# 1. import libraries that are part of the standard python library
from logging import Logger

# 2. import azure libraries and other third party libraries
import requests

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    CustomVisionErrorException,
)
from msrest.authentication import ApiKeyCredentials


# 3. import my own libraries
from kot.common.models import GrassPredictionData, GrassAnalysisResponse
from kot.image_processing.utilities import mark_image_with_rectangle
from kot.common import constants
from kot.common.models import Config


class GrassWeedDetector:
    def __init__(self, config: Config, logger: Logger) -> None:
        self.config = config
        self.logger = logger

    def display(self):
        print("Displaying...")

    def analyze(
        self,
        image: any,
        top_n: int,
        detection_type: constants.DetectionType = constants.DetectionType.WEED,
    ) -> GrassAnalysisResponse:

        # Authenticate a client
        credentials = ApiKeyCredentials(
            in_headers={"Prediction-key": self.config.prediction_key}
        )
        prediction_client = CustomVisionPredictionClient(
            endpoint=self.config.prediction_endpoint, credentials=credentials
        )

        if isinstance(image, str):
            image_url = "{}{}".format(self.config.storage_account, image)
            self.logger.debug(f"image path:{image_url}")
            image_data = requests.get(image_url, stream=True).raw

        elif isinstance(image, bytes):
            image_data = image
        else:
            raise ValueError("image type not supported")

        self.logger.debug("analyzing image...")
        try:
            results = prediction_client.detect_image(
                self.config.project_id, self.config.deployed_name, image_data
            )

        except CustomVisionErrorException as ex:
            self.logger.error(ex)

        self.logger.debug(
            "analysis complete. detected areas: {}".format(len(results.predictions))
        )

        selected_predictions = self.process_analysis_results(results, top_n)

        analysis_response = mark_image_with_rectangle(
            image_data, selected_predictions, self.config, self.logger, detection_type
        )
        return analysis_response

    def process_analysis_results(
        self, results, top_n: int
    ) -> list[GrassPredictionData]:

        grass_predictions = {}
        weed_predictions = {}

        for prediction in results.predictions:
            # self.logger.debug(prediction)
            if prediction.tag_name == constants.DETECTED_TYPE_GRASS:
                grass_predictions[round(prediction.probability, 2)] = (
                    GrassPredictionData(
                        prediction.tag_name,
                        round(prediction.probability, 2),
                        prediction.bounding_box,
                    )
                )
            else:
                weed_predictions[round(prediction.probability, 2)] = (
                    GrassPredictionData(
                        prediction.tag_name,
                        round(prediction.probability, 2),
                        prediction.bounding_box,
                    )
                )

        self.logger.debug(
            f"grass areas: {len(grass_predictions)}, weed areas: {len(weed_predictions)}"
        )

        grass_keys = list(grass_predictions.keys())
        weed_keys = list(weed_predictions.keys())

        grass_keys.sort(reverse=True)
        weed_keys.sort(reverse=True)

        selected_predictions = []
        if len(grass_predictions) > 0:
            count = 0
            while count < top_n:
                selected_predictions.append(grass_predictions[grass_keys[count]])
                count += 1

        if len(weed_predictions) > 0:
            count = 0
            while count < top_n:
                selected_predictions.append(weed_predictions[weed_keys[count]])
                count += 1

        return selected_predictions
