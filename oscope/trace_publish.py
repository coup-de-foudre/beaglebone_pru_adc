import datetime

import zmq

import oscope.abstract_scope as abs_scope

class TracePublisher:
    def __init__(self,
            pub: zmq.Socket,
            scope: abs_scope.AbstractOscilloscope,
            channel: int):
        self.pub = pub
        self.scope = scope
        self.channel = channel
        self.timeout = datetime.timedelta=datetime.timedelta(seconds=1)

    def push(self):
        self.scope.block_on_channel_ready(self.channel, timeout=self.timeout)
        self.scope.

