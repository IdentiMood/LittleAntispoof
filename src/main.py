#!/usr/bin/env python3

import random
import sys
import os
from playsound import playsound
from operations import Operations
from window import Window
from utils import (
    load_config,
    get_random_emotion_task,
    get_random_gaze_task,
    get_speech_recognition_task,
    generate_temporary_path,
    get_random_words,
    OPERATION_VERIFY_EMOTION,
    OPERATION_VERIFY_GAZE,
    OPERATION_VERIFY_SPEECH,
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

        self.blinks_count = 0
        self.were_previous_frame_eyes_closed = False

    def _reset_status(self):
        self.blinks_count = 0

    def verify(self) -> bool:
        """
        Starts the liveness detection procedure.
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
                result, blink_check_passed, aborted = self.do_speech_verification()
                if blink_check_passed:
                    passed_steps += result
                    if self.config["debug"]:
                        print("Blink check passed")

            self._reset_status()

            if aborted:
                return False

        if self.config["debug"]:
            print(f"Passed steps: {passed_steps}")

        return passed_steps == len(self.operations_list)

    def do_video_verification(self, operation: int) -> tuple:
        """
        Shows a Window to acquire the picture.
        Returns a triple (success, blink_check_passed, operation_has_been_aborted).
        """
        task = (
            get_random_emotion_task()
            if operation == OPERATION_VERIFY_EMOTION
            else get_random_gaze_task()
        )

        window = Window(operation, task, self.config, callback=self._count_blinks)
        blinks_check_passed = self.operations.do_blinks_ratio_check(self.blinks_count)

        return (
            self.handle_task(operation, window.frame, task),
            blinks_check_passed,
            (not window.is_expired),
        )

    def _count_blinks(self, probe):
        eyes_closed = self.operations.is_blinking(probe)
        if eyes_closed is None:
            if self.config["debug"]:
                print("Cannot localize eyes")
            return

        if eyes_closed and not self.were_previous_frame_eyes_closed:
            if self.config["debug"]:
                print("Blinking")
            self.blinks_count += 1

        self.were_previous_frame_eyes_closed = eyes_closed

    def handle_task(
        self, operation: int, frame, task: str, tmpfile=None, words=""
    ) -> bool:
        """
        Calls the given recognition operation.
        Depending on the operation type, the appropriate parameters are used.
        Returns True if the result of the operation was successful.
        """
        try:
            if operation in (OPERATION_VERIFY_EMOTION, OPERATION_VERIFY_GAZE):
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
        if operation == OPERATION_VERIFY_GAZE:
            return self.operations.verify_gaze(frame, task)

        return self.operations.verify_speech(
            words,
            tmpfile,
            self.config["speech"]["use_soundex_match"],
        )

    def do_speech_verification(self):
        """
        Calls the speech verification operation.
        Returns a tuple (speech verification passed, blink checks passed, operation complete).
        """
        task = get_speech_recognition_task()
        words = get_random_words(
            "./dictionary.txt", self.config["speech"]["words_to_display"]
        )

        tmpfile = generate_temporary_path()

        window = Window(
            OPERATION_VERIFY_SPEECH,
            task,
            self.config,
            callback=self._count_blinks,
            tmpfile=tmpfile,
            words=words,
        )
        blinks_check_passed = self.operations.do_blinks_ratio_check(self.blinks_count)

        result = (
            self.handle_task(
                OPERATION_VERIFY_SPEECH, None, task, tmpfile=tmpfile, words=words
            ),
            blinks_check_passed,
            (not window.is_expired),
        )
        os.remove(tmpfile)

        return result


if __name__ == "__main__":
    app = App(load_config())

    playsound(app.config["sounds"]["start"])
    verified = app.verify()
    if not verified:
        print("You are not a human", file=sys.stderr)
        sys.exit(1)

    print("Welcome, fellow human")
