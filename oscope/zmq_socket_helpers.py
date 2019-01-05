import zmq

class PublishContext:
    """
    This is a context helper that creates and cleans up
    ZMQ Publish socket instances.

    >>> with socket as PublishContext(["ipc://endpoint"]):
    ...    pass
    ...    # Do stuff with socket

    """

    def __init__(self, binds: list):
        for element in binds:
            assert isinstance(element, str)

        self._binds = binds
        self._socket = None
        self._ctx = None
    
    def __enter__(self):
        self._ctx = zmq.Context()
        self._socket = self._ctx.socket(zmq.PUB)
        for b in self._binds:
            self._socket.bind(b)

        return self._socket

    def __exit__(self, *args):
        if self._socket is not None:
            self._socket.close(linger=0)
            self._socket = None

        if self._ctx is not None:
            self._ctx.term()
            self._ctx = None
