import random
import json
import os
import tempfile
from dotenv import load_dotenv

KEY_ESC = 27
KEY_ENTER = 32
KEY_SPACE = 13

OPERATION_VERIFY_EMOTION = 0
OPERATION_VERIFY_GAZE = 1
OPERATION_VERIFY_SPEECH = 2

OPERATIONS_LIST = [
    OPERATION_VERIFY_EMOTION,
    OPERATION_VERIFY_GAZE,
    OPERATION_VERIFY_SPEECH,
]

OPERATIONS_WINDOW_TITLES = {
    OPERATION_VERIFY_EMOTION: "[LittleAntispoof] Emotion verification",
    OPERATION_VERIFY_GAZE: "[LittleAntispoof] Gaze verification",
    OPERATION_VERIFY_SPEECH: "[LittleAntispoof] Speech verification",
}

TASK_EMOTION_HAPPY = "happy"
TASK_EMOTION_SAD = "sad"
TASK_EMOTION_NEUTRAL = "neutral"

TASK_GAZE_RIGHT = "right"
TASK_GAZE_CENTER = "center"
TASK_GAZE_LEFT = "left"
CLOSED_EYES = "closed_eyes"

SPEECH_RECOGNITION_HELP = "Say these words out loud"

EMOTION_TASKS = [
    TASK_EMOTION_HAPPY,
    TASK_EMOTION_SAD,
    TASK_EMOTION_NEUTRAL,
]

GAZE_TASKS = [
    TASK_GAZE_RIGHT,
    TASK_GAZE_CENTER,
    TASK_GAZE_LEFT,
]

SAMPLING_RATE = 48000


def load_config():
    """
    Loads the configuration from the ./config.json file
    """
    with open("./config.json", "r", encoding="utf8") as f:
        config = json.load(f)
    return config


def get_random_emotion_task() -> str:
    return EMOTION_TASKS[random.randint(0, len(EMOTION_TASKS) - 1)]


def get_random_gaze_task() -> str:
    return GAZE_TASKS[random.randint(0, len(GAZE_TASKS) - 1)]


def get_speech_recognition_task() -> str:
    return SPEECH_RECOGNITION_HELP


def get_random_words(dictionary_path: str, number_of_words: int) -> str:
    words_list = ""
    lines = open(dictionary_path, encoding="utf8").read().splitlines()
    random_indexes = random.sample(range(0, len(lines)), number_of_words)
    for index in random_indexes:
        words_list += f"{lines[index]} "
    return words_list


def get_azure_api_key() -> str:
    load_dotenv(".env")
    return os.environ.get("AZURE_API_KEY")


def get_azure_region() -> str:
    load_dotenv(".env")
    return os.environ.get("AZURE_REGION")


def generate_temporary_path() -> str:
    return f"{tempfile._get_default_tempdir()}/{tempfile._get_candidate_names().__next__()}"


def make_text_prompt(task: str) -> str:
    """
    Returns an embelished string describing the given task, based on its type
    """
    if task in GAZE_TASKS:
        return f"Look {task}"
    if task in EMOTION_TASKS:
        return f"Make a {task} face"
    return task
