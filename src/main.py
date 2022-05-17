#!/usr/bin/env python3

import random
import sys
from operations import Operations
from window import Window
from utils import (
    load_config,
    get_random_emotion_task,
    get_random_gaze_task,
    OPERATION_VERIFY_EMOTION,
    OPERATION_VERIFY_GAZE,
    OPERATIONS_LIST,
)


class App:
    """
    App is the main coordinator for the LittleAntispoof application.
    """

    def __init__(self, config):
        self.config = config
        self.operations = Operations(config)
        self.operations_list = OPERATIONS_LIST
        random.shuffle(self.operations_list)

    def verify(self) -> bool:
        """
        Starts the antispoofing detection procedure.
        """
        passed_steps = 0
        for operation in self.operations_list:
            if operation in (OPERATION_VERIFY_EMOTION, OPERATION_VERIFY_GAZE):
                result, aborted = self.do_video_verification(operation)
            else:
                result, aborted = self.do_speech_verification()

            if aborted:
                return False

            passed_steps += result

        print(f"Passed steps: {passed_steps}")

        return passed_steps == len(self.operations_list)

    def do_video_verification(self, operation: int) -> tuple:
        """
        Shows a Window to shot the picture.
        Returns a tuple (success, operation_has_been_aborted).
        """
        task = (
            get_random_emotion_task()
            if operation == OPERATION_VERIFY_EMOTION
            else get_random_gaze_task()
        )

        window = Window(operation, task)
        if window.shot_button_pressed:
            return self.handle_probe(operation, window.frame, task), False

        return False, True

    def handle_probe(self, operation: int, frame, task: str) -> bool:
        """
        Calls the given recognition operation on the given frame.
        Returns True if the result of the operation was successful.
        """
        try:
            self.operations.detect_face(frame)
        except ValueError as error:
            print(
                "Error while handling the probe.",
                error,
                file=sys.stderr,
            )
            return False

        if operation == OPERATION_VERIFY_EMOTION:
            return self.operations.verify_emotion(frame, task)
        return self.operations.verify_gaze(frame, task)

    def do_speech_verification(self):
        return True, False


if __name__ == "__main__":
    app = App(load_config())

    print("Are you a real human?")
    opt = input("[y]/n: ")

    if opt in ("", "y"):
        verified = app.verify()
        if not verified:
            print("It looks like you are not.", file=sys.stderr)
            sys.exit(1)
        print("Welcome, fellow human.")
    else:
        sys.exit(1)
