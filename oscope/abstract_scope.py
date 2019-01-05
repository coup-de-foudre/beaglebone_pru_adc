import datetime
import time

import numpy as np


class AbstractOscilloscope():
    def is_channel_ready(self, channel: int) -> bool:
        raise NotImplementedError()

    def read_channel(self, channel: int) -> np.ndarray:
        raise NotImplementedError()

    def get_channel_sample_rate(self, channel: int) -> float:
        raise NotImplementedError()

    def get_channel_sample_count(self, channel: int) -> float:
        raise NotImplementedError()

    def block_on_channel_ready(self, channel: int, timeout: datetime.timedelta):
        if self.is_channel_ready(channel):
            return

        done_dt = datetime.datetime.now() + timeout
        while datetime.datetime.now() < done_dt:
            time.sleep(0.001)
            if self.is_channel_ready(channel):
                return
        
        error_message = "Channel {} did not become ready in {} seconds".format(
            channel, timeout.total_seconds())
        raise TimeoutError(error_message)