import threading
import time

import UnicornPy
import numpy as np


class EEGRecorderThread(threading.Thread):
    def __init__(self,
                 experiment_id: str,
                 experimental_mode: str):
        threading.Thread.__init__(self, daemon=True)
        self.experiment_id = experiment_id
        self.experimental_mode = experimental_mode
        self.running = True
        self.data_path = f'data/{self.experimental_mode.lower()}/screen/{self.experiment_id}-{time.strftime("%Y%m%d-%H:%M:%S")}.csv'
        device_list = UnicornPy.GetAvailableDevices(True)

        if len(device_list) <= 0 or device_list is None:
            raise Exception("No device available. Please pair with a Unicorn first.")
        if len(device_list) > 1:
            raise Exception(
                "Multiple devices available. Please disconnect all the devices that are not meant to be a part of this experiment. Multiple devices not supported.")

        self.device = UnicornPy.Unicorn(device_list[0])
        self.file = open(self.data_path, "wb")

        self.test_signal_enabled = False
        self.frame_length = 1
        self.num_acquired_channels = self.device.GetNumberOfAcquiredChannels()
        self.configuration = self.device.GetConfiguration()

        # Allocate memory for the acquisition buffer.
        self.buffer_length = self.frame_length * self.num_acquired_channels * 4
        self.receive_buffer = bytearray(self.buffer_length)

    def start(self):
        self.running = True
        self.device.StartAcquisition(self.test_signal_enabled)

        while self.running:
            self.device.GetData(self.frame_length, self.receive_buffer, self.buffer_length)

            # Convert receive buffer to numpy float array
            data = np.frombuffer(self.receive_buffer,
                                 dtype=np.float32,
                                 count=self.num_acquired_channels * self.frame_length)
            data = np.reshape(data, (self.frame_length, self.num_acquired_channels))
            np.savetxt(self.file, data, delimiter=',', fmt='%.3f', newline='\n')

    def stop(self):
        self.running = False
        self.device.StopAcquisition()
        del self.receive_buffer
        self.file.close()
        del self.device
