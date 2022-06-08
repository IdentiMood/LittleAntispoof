import tkinter as tk
import time
import threading
import cv2
from playsound import playsound
from PIL import Image, ImageTk
from utils import (
    OPERATIONS_WINDOW_TITLES,
    SAMPLING_RATE,
    OPERATION_VERIFY_SPEECH,
    make_text_prompt,
)
import sounddevice as sd
from scipy.io.wavfile import write


class Window:
    """
    Window is the LittleAntispoof class that creates and handles Tkinter windows,
    in order to acquire pictures of the user from the webcam.
    Window automatically creates and configures the appropriate widgets.
    """

    def __init__(
        self,
        operation: int,
        task: str,
        config: dict,
        callback: callable,
        tmpfile=None,
        words="",
    ):
        self.current_countdown = config["window_duration_secs"]
        self.closing_sound = (
            config["sounds"]["mic_stop"]
            if operation == OPERATION_VERIFY_SPEECH
            else config["sounds"]["camera_shot"]
        )

        self.is_debug = config["debug"]
        self.records_secs = config["speech"]["record_duration_secs"]

        self.callback = callback
        self.tmpfile = tmpfile

        self.window = tk.Tk()
        self.window.title(OPERATIONS_WINDOW_TITLES[operation])

        self.label = tk.Label(
            self.window,
            text=make_text_prompt(task),
            pady=20,
            font=("sans-serif", 24),
        )
        self.canvas = tk.Label(self.window)
        self.countdown_label = tk.Label(
            self.window,
            text=self.current_countdown,
            pady=20,
            font=("sans-serif", 24),
        )

        self.label.pack()
        self.canvas.pack()
        # self.countdown_label.pack()

        self.is_expired = False

        self.capture = cv2.VideoCapture(0)
        self.frame = None
        if operation == OPERATION_VERIFY_SPEECH:
            self.words_label = tk.Label(
                self.window,
                text=words,
                pady=20,
                font=("sans-serif", 18),
            )
            self.words_label.pack()
            speech_thread = threading.Thread(target=self.record_audio)
            speech_thread.start()

        threading.Thread(target=self._countdown).start()

        if operation == OPERATION_VERIFY_SPEECH:
            self.start_speech_loop()
        else:
            self.start_video_loop()

        self.countdown_label.pack()
        self.window.mainloop()

        if operation == OPERATION_VERIFY_SPEECH:
            # wait for thread end
            speech_thread.join()

    def start_speech_loop(self):
        _, self.frame = self.capture.read()

        self.callback(self.frame)
        self.window.after(10, self.start_speech_loop)

        if self.is_expired:
            self._destroy_with_success()

    def start_video_loop(self):
        """
        Starts the video capture from OpenCV and displays each frame on the canvas
        """
        _, self.frame = self.capture.read()

        self.callback(self.frame)

        decorated_frame = self._decorate_frame()

        image = cv2.cvtColor(decorated_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image=image)

        self.canvas.imgtk = image
        self.canvas.configure(image=image)
        self.window.after(10, self.start_video_loop)

        if self.is_expired:
            self._destroy_with_success()

    def _countdown(self) -> bool:
        while self.current_countdown != 0:
            time.sleep(1)
            self.current_countdown -= 1
            self.countdown_label.config(text=self.current_countdown)
            self.is_expired = self.current_countdown == 0

    def _destroy_with_success(self):
        """
        Closes the current Window with a "success" state,
        meaning that the user has clicked the "shot" button.
        """
        playsound(self.closing_sound)
        self.is_expired = True
        self.window.destroy()

    def _decorate_frame(self):
        """
        Draws an ellipse at the center and puts a dark overlay on the outside,
        in order to guide the user into an acceptable position to perform the acquisition.
        """
        height = len(self.frame)
        width = len(self.frame[0])

        ellipse_mask = cv2.numpy.zeros_like(self.frame)
        ellipse_mask = cv2.ellipse(
            ellipse_mask,
            (int(width / 2), int(height / 2)),
            (int(width / 3), int(height / 2)),
            0,
            0,
            360,
            (255, 255, 255),
            -1,
        )

        outer_mask = cv2.bitwise_not(ellipse_mask)
        outer_image = cv2.bitwise_and(self.frame, outer_mask)
        ellipse_image = cv2.bitwise_and(self.frame, ellipse_mask)
        return cv2.addWeighted(ellipse_image, 1.0, outer_image, 0.5, 1)

    def record_audio(self):
        """
        TODO
        """
        fs = SAMPLING_RATE

        if self.is_debug:
            print(f"Start recording to temporary file {self.tmpfile}")
        my_recording = sd.rec(int(self.records_secs * fs), samplerate=fs, channels=1)
        sd.wait()
        write(self.tmpfile, fs, my_recording)
        if self.is_debug:
            print("End recording")
