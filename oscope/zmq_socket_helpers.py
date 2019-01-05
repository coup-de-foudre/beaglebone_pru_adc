import tempfile
import os

import zmq

IPC_PATH_MAX_LEN = 107


class IPCTemp:
    """
    This class provides unique and sanitary IPC addresses
    on the local filesystem.  It is designed to be used
    as a context manager in the following pattern:

    >>> with IPCTemp(["foo", "bar"]) as (foo_path, bar_path):
    >>>    socket1.bind(foo_path)
    >>>    socket2.bind(bar_path)

    On exit of the block, the context manager will ensure deletion
    of the root folder as well as any sockets found within it.
    Each path from a particular invocation has a unique
    directory prefix, so this context manager can be used in a
    nested fashion without fear of name collision.
    """
    def __init__(self, ipc_names: list):
        self._ipc_names = ipc_names
        assert len(ipc_names) == len(set(ipc_names)), \
            "All ipc names must be unique:" + repr(ipc_names)

    def __enter__(self):
        self._td = tempfile.TemporaryDirectory(prefix="ipc_temp")
        self._td.__enter__()
        names = ["ipc://" + os.path.join(self._td.name, ipc_name) for ipc_name in self._ipc_names]

        for name in names:
            if len(name) >= IPC_PATH_MAX_LEN:
                self._td.cleanup()
                kesm.base.raise_error(
                    'IPC Address name "{}" is too long: ({} chars, max is {})',
                    name, len(name), IPC_PATH_MAX_LEN,
                    exception_class=AssertionError
                )
        return names

    def __exit__(self, *args):
        self._td.__exit__(*args)



class PublishContext:
    """
    This is a context helper that creates and cleans up
    ZMQ Publish socket instances.

    >>> with socket as PublishContext(["ipc://endpoint"]):
    >>>    # Do stuff with socket
    >>> # Socket and context cleaned up w/o hassle
    """

    @staticmethod
    def sanity_check_bind_list(binds: list):
        for bind in binds:
            assert isinstance(bind, str)
            assert ":" in bind, "Invalid endpoint specified:" + bind

    def __init__(self, binds: list):
        self.sanity_check_bind_list(binds)
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

class TestPublishContext(PublishContext):
    def __init__(self, binds):
        self.sanity_check_bind_list(binds)
    
