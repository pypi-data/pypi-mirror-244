"""
SMTP Server Context
"""

from typing import Tuple

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP


class SmtpServer(SMTP):
    """
    Simple SMTP Server class
    """

    def __init__(self, *args, bind: Tuple[str, int], **kwargs):
        """
        Build the server

        :param bind: Tuple of (hostname, port)
        """
        super().__init__(*args, hostname="{:s}:{:d}".format(*bind), **kwargs)  # pylint: disable=consider-using-f-string


class SmtpController(Controller):
    """
    Simple SMTP Controller class
    """

    def __init__(self, *args, bind_host: str, bind_port: int, **kwargs):
        """
        Build the Controller

        :param bind_host: Hostname to bind to
        :param bind_port: Port to bind to
        """
        super().__init__(*args, hostname=bind_host, port=bind_port, **kwargs)
        self.__bind_host = bind_host
        self.__bind_port = bind_port

    def factory(self) -> SmtpServer:
        """
        Build the Server

        :return: SMTP Server Instance
        """
        return SmtpServer(self.handler, bind=(self.__bind_host, self.__bind_port))
