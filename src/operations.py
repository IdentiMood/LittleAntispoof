import json
import cv2
from deepface import DeepFace


class Operations:
    """
    Operations is the LittleAntispoof class that handles the recognition operations.
    """

    def __init__(self, config):
        self.config = config
        self.is_debug = config["debug"]

    def detect_face(self, probe):
        """
        Returns the cropped and aligned image, from the given probe.
        """
        return DeepFace.detectFace(
            probe, detector_backend=self.config["verify"]["detector_backend"]
        )

    def verify_emotion(self, probe, requested_emotion) -> bool:
        """
        Return True if the emotion extracted from the given probe against the requested one.
        """

        if self.is_debug:
            print("Performing emotion recognition")

        result = DeepFace.analyze(
            probe,
            actions=["emotion"],
            detector_backend=self.config["emotion"]["detector_backend"],
        )

        return result["dominant_emotion"] == requested_emotion
