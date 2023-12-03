"""
Network related stuff
"""

import socket

from smtp_test_server.exceptions import NotALocalHostnameOrIPAddressToBindToError


def is_bind_host_is_local(bind_host: str) -> bool:
    """
    Find out if the given name is local

    :param bind_host: The host to bind to (ip or hostname)
    :return: True, if the host to bind is local, False otherwise
    """
    if bind_host in ("localhost", "127.0.0.1", "0.0.0.0", "::1", "::0", "0:0:0:0:0:0:0:1", "0:0:0:0:0:0:0:0"):
        return True
    local_host_name = socket.gethostname()
    local_addresses = socket.getaddrinfo(local_host_name, 1)
    try:
        remote_addresses = socket.getaddrinfo(bind_host, 1)
    except OSError:
        return False
    for _, _, _, _, local_socket_address in local_addresses:
        for _, _, _, _, remote_socket_address in remote_addresses:
            if remote_socket_address[0] == local_socket_address[0]:
                return True
    return False


def find_free_port(bind_host: str) -> int:
    """
    Find a free port on the bind host

    :param bind_host: Host to try the bind
    :return: A free port number
    :raises OSError: When no port could be allocated
    """
    with socket.socket() as sock:
        if not is_bind_host_is_local(bind_host):
            raise NotALocalHostnameOrIPAddressToBindToError(
                -1, f"'{bind_host}' is not a local host name / ip address to bind to"
            )
        sock.bind((bind_host, 0))
        return sock.getsockname()[1]
