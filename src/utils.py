import json

KEY_ESC = 27
KEY_ENTER = 32
KEY_SPACE = 13

OPERATION_VERIFY_EMOTION = 0
OPERATION_VERIFY_GAZE = 1
OPERATION_VERIFY_SPEECH = 2

OPERATIONS_WINDOW_LABELS = []
OPERATIONS_WINDOW_TITLES = [
    "[LittleAntispoof] Emotion verification",
    "[LittleAntispoof] Gaze verification",
    "[LittleAntispoof] Speech verification",
]


def load_config():
    """
    Loads the configuration from the ./config.json file
    """
    with open("./config.json", "r", encoding="utf8") as f:
        config = json.load(f)
    return config
