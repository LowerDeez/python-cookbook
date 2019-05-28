"""
Problem
You want to make your objects support the context-management protocol (the with
statement).
Solution
In order to make an object compatible with the with statement, you need to implement
__enter__() and __exit__() methods. For example, consider the following class,
which provides a network connection:
"""

from socket import socket, AF_INET, SOCK_STREAM


class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None


"""
The key feature of this class is that it represents a network connection, but it doesn’t
actually do anything initially (e.g., it doesn’t establish a connection). Instead, the con‐
nection is established and closed using the with statement (essentially on demand). For
example:

from functools import partial


conn = LazyConnection(('www.python.org', 80))

# Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
"""

"""
One subtle aspect of this recipe is whether or not the LazyConnection class allows nested
use of the connection with multiple with statements. As shown, only a single socket
connection at a time is allowed, and an exception is raised if a repeated with statement
is attempted when a socket is already in use. You can work around this limitation with
a slightly different implementation, as shown here:
"""

from socket import socket, AF_INET, SOCK_STREAM


class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()


# Example use
from functools import partial

conn = LazyConnection(('www.python.org', 80))

with conn as s1:
    ...
    with conn as s2:
        ...
        # s1 and s2 are independent sockets