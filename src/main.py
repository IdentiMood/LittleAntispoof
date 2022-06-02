#!/usr/bin/env python3

import random
import sys
from operations import Operations
from window import Window, WORDS
from utils import (
    load_config,
    get_random_emotion_task,
    get_random_gaze_task,
    get_speech_recognition_task,
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

        self.blinks_checks_count = 0
        self.blinks_count = 0

    def verify(self) -> bool:
        """
        Starts the antispoofing detection procedure.
        """
        passed_steps = 0
        for operation in self.operations_list:
            if operation in (OPERATION_VERIFY_EMOTION, OPERATION_VERIFY_GAZE):
                result, blink_check_passed, aborted = self.do_video_verification(
                    operation
                )
                if blink_check_passed:
                    passed_steps += result
                    if self.config["debug"]:
                        print("Blink check passed")
            else:
                result, blink_check_passed, aborted = self.do_speech_verification(
                    operation
                )
                if blink_check_passed:
                    passed_steps += result
                    if self.config["debug"]:
                        print("Blink check passed")

            if aborted:
                return False

        if self.config["debug"]:
            print(f"Passed steps: {passed_steps}")

        return passed_steps == len(self.operations_list)

    def do_video_verification(self, operation: int) -> tuple:
        """
        Shows a Window to shot the picture.
        Returns a triple (success, blink_check_passed, operation_has_been_aborted).
        """
        task = (
            get_random_emotion_task()
            if operation == OPERATION_VERIFY_EMOTION
            else get_random_gaze_task()
        )

        window = Window(operation, task, self.config, callback=self._count_blinks)
        blinks_check_passed = (
            self.operations.do_blinks_ratio_check(
                self.blinks_checks_count, self.blinks_count
            ),
        )

        return (
            self.handle_probe(operation, window.frame, task),
            blinks_check_passed,
            (not window.is_expired),
        )

    def _count_blinks(self, probe):
        self.blinks_checks_count += 1
        if self.operations.is_blinking(probe):
            self.blinks_count += 1

    def handle_probe(self, operation: int, frame, task: str) -> bool:
        """
        Calls the given recognition operation on the given frame.
        Returns True if the result of the operation was successful.
        """
        try:
            if operation < 2:
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
        elif operation == OPERATION_VERIFY_GAZE:
            return self.operations.verify_gaze(frame, task)
        else:
            return self.operations.verify_speech(WORDS)

    def do_speech_verification(self, operation: int):
        """
        TODO
        """
        task = get_speech_recognition_task()

        window = Window(operation, task, self.config, callback=self._count_blinks)
        blinks_check_passed = (
            self.operations.do_blinks_ratio_check(
                self.blinks_checks_count, self.blinks_count
            ),
        )

        return (
            self.handle_probe(operation, None, task),
            blinks_check_passed,
            (not window.is_expired),
        )


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
