import sys
from operations import Operations
from utils import (
    load_config,
)


class App:
    """
    App is the main coordinator for the LittleAntispoof application.
    """

    def __init__(self, config):
        self.config = config
        self.operations = Operations(config)

    def verify(self) -> bool:
        """
        Starts the antispoofing detection procedure.
        """
        return True

    def show_photo_window(self, operation: int):
        """
        Shows a Window to shot the picture.
        Returns a tuple (success, operation_has_been_aborted).
        """


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
