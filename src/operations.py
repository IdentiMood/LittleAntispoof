import json
import cv2
from deepface import DeepFace
from gaze_tracking import GazeTracking
from utils import TASK_GAZE_CENTER, TASK_GAZE_LEFT, TASK_GAZE_RIGHT, CLOSED_EYES


class Operations:
    """
    Operations is the LittleAntispoof class that handles the recognition operations.
    """

    def __init__(self, config):
        self.config = config
        self.is_debug = config["debug"]
        self.gaze = GazeTracking()

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
        Returns True if the given gaze in the given probe matches the requested one
        """

        def __get_gaze_direction():
            if self.gaze.is_left():
                return TASK_GAZE_LEFT
            if self.gaze.is_center():
                return TASK_GAZE_CENTER
            if self.gaze.is_right():
                return TASK_GAZE_RIGHT

        if self.is_debug:
            print("Performing emotion recognition")

        self.gaze.refresh(probe)

        if self.is_debug:
            print(f"Requested gaze: {requested_gaze}; got: {__get_gaze_direction()}")

        return requested_gaze == __get_gaze_direction()

    def is_blinking(self, probe) -> bool:
        """
        Returns True if the eyes in the given probe are closed
        """
        self.gaze.refresh(probe)
        return self.gaze.is_blinking()

    def do_blinks_ratio_check(
        self, blinks_checks_count: int, blinks_count: int
    ) -> bool:
        """
        Returns True if the ratio of blinks is within the configured thresholds range
        """
        return (
            self.config["blinking"]["min_threshold"]
            <= blinks_count / blinks_checks_count
            <= self.config["blinking"]["max_threshold"]
        )
