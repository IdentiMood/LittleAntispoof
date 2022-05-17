import json
import cv2
from deepface import DeepFace
from gaze_tracking import GazeTracking
from utils import TASK_GAZE_CENTER, TASK_GAZE_LEFT, TASK_GAZE_RIGHT


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

    def verify_emotion(self, probe, requested_emotion: str) -> bool:
        """
        Return True if the emotion extracted from the given probe matches against the requested one.
        """

        result = DeepFace.analyze(
            probe,
            actions=["emotion"],
            detector_backend=self.config["emotion"]["detector_backend"],
        )

        if self.is_debug:
            print(
                f"Requested emotion: {requested_emotion}; got {result['dominant_emotion']}"
            )

        return result["dominant_emotion"] == requested_emotion

    def verify_gaze(self, probe, requested_gaze: str) -> bool:
        """
        Return True if the gaze in the probe matches with the requested one.
        """

        def __get_gaze_direction(gaze):
            if gaze.is_left():
                return TASK_GAZE_LEFT
            if gaze.is_center():
                return TASK_GAZE_CENTER
            if gaze.is_right():
                return TASK_GAZE_RIGHT

        if self.is_debug:
            print("Performing emotion recognition")

        gaze = GazeTracking()
        gaze.refresh(probe)

        if self.is_debug:
            print(
                f"Requested gaze: {requested_gaze}; got: {__get_gaze_direction(gaze)}"
            )

        return requested_gaze == __get_gaze_direction(gaze)
