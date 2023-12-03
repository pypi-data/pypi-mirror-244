"""
Pytest Mock SMTP Server for testing
"""
from email.message import Message as EmailMessage
from typing import List, Optional

from aiosmtpd.handlers import Message

from smtp_test_server.exceptions import AlreadyStartedError, NotProperlyInitializedError, NotStartedError
from smtp_test_server.mock import SmtpController
from smtp_test_server.net import find_free_port


class MessageKeeper(Message):
    """
    Message keeping class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize with an empty message list
        """
        super().__init__(*args, **kwargs)
        self.__messages: List[EmailMessage] = []

    def handle_message(self, message: EmailMessage) -> None:
        """
        Handle an incoming message
        """
        self.__messages.append(message)

    @property
    def messages(self) -> List[EmailMessage]:
        """
        Access the messages list
        """
        return self.__messages


class SmtpMockServer:
    """
    Server that runs for a test and saves incoming mails for later evaluation
    """

    def __init__(self, bind_host: Optional[str] = None, bind_port: Optional[int] = None):
        """
        Initialize the server

        :param bind_host: Hostname, IP or `None` for default "127.0.0.1"
        :param bind_port: Port number, or `None` for a random free port
        :raises OSError: When no free port could be found
        """
        self.__bind_host = bind_host if bind_host is not None else "127.0.0.1"
        self.__bind_port = bind_port if bind_port is not None else find_free_port(self.__bind_host)
        self.__controller = None  # type: Optional[SmtpController]
        self.__keeper = None  # type: Optional[MessageKeeper]

    def __enter__(self) -> "SmtpMockServer":
        """
        Start the Server

        :return: The mock server
        """
        if self.__controller is not None:
            raise AlreadyStartedError("SMTP server already started")
        self.__keeper = MessageKeeper()
        self.__controller = SmtpController(self.__keeper, bind_host=self.__bind_host, bind_port=self.__bind_port)
        self.__controller.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Shutdown the server
        """
        if self.__controller is None:
            raise NotStartedError("SMTP server not started")
        self.__controller.stop()
        self.__controller = None

    @property
    def host(self) -> str:
        """
        Get the host name where the bind should happen
        """
        return self.__bind_host

    @property
    def port(self) -> int:
        """
        Get the port number where the bind should happen
        """
        return self.__bind_port

    @property
    def messages(self) -> List[EmailMessage]:
        """
        Access the messages
        """
        if self.__keeper is None:
            raise NotProperlyInitializedError("accessed messages without starting the server")
        return self.__keeper.messages
