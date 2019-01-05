import datetime

import zmq

import oscope.abstract_scope as abs_scope
import oscope.schema as schema

class TracePublisher:
    def __init__(self,
            pub: zmq.Socket,
            scope: abs_scope.AbstractOscilloscope,
            channel: int):
        self.pub = pub
        self.scope = scope
        self.channel = channel
        self.timeout = datetime.timedelta=datetime.timedelta(seconds=1)
        self.sequence = 0

    def push(self):
        self.scope.block_on_channel_ready(self.channel, timeout=self.timeout)
        trace_data = self.scope.read_channel(self.channel)

        meta = dict(
            device = schema.get_device_meta(self.scope.__class__.__name__, id(self.scope))
            trace = schema.get_trace_meta(self.scope.get_sample_rate(), self.scope.get_sample_count())
            sequence=self.sequence)
        self.sequence += 1

        