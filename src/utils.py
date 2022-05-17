import random
import json

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
TASK_EMOTION_FEAR = "fear"

TASK_GAZE_RIGHT = "right"
TASK_GAZE_CENTER = "center"
TASK_GAZE_LEFT = "left"

EMOTION_TASKS = [TASK_EMOTION_HAPPY, TASK_EMOTION_SAD, TASK_EMOTION_FEAR]

GAZE_TASKS = [
    TASK_GAZE_RIGHT,
    TASK_GAZE_CENTER,
    TASK_GAZE_LEFT,
]


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