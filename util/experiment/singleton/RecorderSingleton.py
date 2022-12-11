from datetime import datetime

from util.experiment.singleton.EEGRecorderThread import EEGRecorderThread
from util.experiment.singleton.ScreenRecorderThread import ScreenRecorderThread


class RecorderSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RecorderSingleton(metaclass=RecorderSingletonMeta):
    def __init__(self):
        self.screen_recorder_thread = None
        self.eeg_recorder_thread = None
        self.experimental_mode = None
        self.experiment_id = None

    def set_experiment_id(self, experiment_id: str):
        self.experiment_id = experiment_id

    def set_experimental_mode(self, experimental_mode: str):
        self.experimental_mode = experimental_mode

    def start_recording(self):
        self.eeg_recorder_thread = EEGRecorderThread(experiment_id=self.experiment_id,
                                                     experimental_mode=self.experimental_mode)
        self.screen_recorder_thread = ScreenRecorderThread(experiment_id=self.experiment_id,
                                                           experimental_mode=self.experimental_mode)

        self.eeg_recorder_thread.start()
        self.screen_recorder_thread.start()

    def end_recording(self):
        self.eeg_recorder_thread.stop()
        self.screen_recorder_thread.stop()
