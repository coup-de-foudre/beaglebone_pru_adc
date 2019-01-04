import zmq

import oscope.zmq_socket_helpers as socket_helpers

def test_ctx_manager():
    with socket_helpers.PublishContext(("ipc://foo", "ipc://bar")) as pub_socket:
        assert isinstance(pub_socket, zmq.Socket)
