import numpy as np


class AbstractOscilloscope:
    def is_channel_ready(self, channel: int) -> bool:
        raise NotImplementedError()

    def read_channel(self, channel: int) -> np.ndarray:
        raise NotImplementedError()

    def get_channel_sample_rate(self, channel: int) -> float:
        raise NotImplementedError()

    def get_channel_sample_count(self, channel: int) -> float:
        raise NotImplementedError()
