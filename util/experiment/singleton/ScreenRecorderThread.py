import threading
import time

import cv2
import numpy as np
from PIL import Image
from mss import mss


def capture():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


class ScreenRecorderThread(threading.Thread):
    def __init__(self, experiment_id: str,
                 experimental_mode: str):
        threading.Thread.__init__(self, daemon=True)
        self.running = True
        self.fps = 20
        self.prev = 0
        self.experimental_mode = experimental_mode
        self.experiment_id = experiment_id
        self.screen_size = (None, None)
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.video_path = f'data/{self.experimental_mode.lower()}/screen/{self.experiment_id}-{time.strftime("%Y%m%d-%H:%M:%S")}.mp4'
        self.out = None
        self.images = []

    def run(self):
        self.running = True
        while self.running:
            self.images.append(capture())

    def stop(self):
        self.running = False
        self.screen_size = (self.images[0].width, self.images[0].height)
        self.out = cv2.VideoWriter(self.video_path, self.fourcc, self.fps, self.screen_size)
        for image in self.images:
            image_np = np.array(image)
            image_cv = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            self.out.write(np.array(image_cv))
        self.out.release()
        self._stop()
