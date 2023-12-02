# sockets.py

import datetime as dt
import socket
from typing import Iterable, Callable, Any
from urllib.parse import urlparse

from looperator import Operator, ServiceInterface

from socketsio.server import Server
from socketsio.protocols import BCP, TCP, BaseProtocol

from dynamic_service.endpoints import BaseEndpoint, encode
from dynamic_service.service.base import EndpointsService

__all__ = [
    "SocketService"
]

Connection = socket.socket
Address = tuple[str, int]
Endpoints = dict[str, BaseEndpoint]
EndpointsContainer = Iterable[BaseEndpoint] | Endpoints
Time = float | dt.timedelta | dt.datetime
Action = Callable[[Connection, Address, BaseProtocol], Any]

class SocketService(ServiceInterface, EndpointsService):
    """
    A class to represent a service object.

    The BaseService is the parent class of service class.
    The service class creates a service object to deploy
    functionality of endpoint objects as a REST API, with sockets backend.

    data attributes:

    - endpoints:
        A set of endpoint objects to serve with the api.

    >>> from dynamic_service.endpoints import BaseEndpoint, GET
    >>> from dynamic_service.service.sockets import SocketService
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/my_endpoint", methods=[GET])
    >>>
    >>> service = SocketService(
    >>>     endpoints=[endpoint]
    >>> )
    >>>
    >>> service.run()
    """

    __slots__ = "endpoints", "server", 'host', 'port'

    def __init__(
            self,
            connection: Connection = None, *,
            host: str = None,
            port: int = None,
            protocol: BaseProtocol = None,
            endpoints: EndpointsContainer = None
    ) -> None:
        """
        Defines the server datasets for clients and client commands.

        :param connection: The connection socket.
        :param host: The ip address of the server.
        :param port: The port for the server connection.
        :param protocol: The protocol for the sockets.
        :param endpoints: The commands to run for specific requests of the clients.
        """

        if protocol is None:
            protocol = BCP(TCP())
        # end if

        self.server = Server(connection=connection, protocol=protocol)

        self.host = host
        self.port = port

        if None not in (self.host, self.port):
            self.connect()
        # end if

        ServiceInterface.__init__(self)
        EndpointsService.__init__(self, endpoints=endpoints)

        self._server_operator = Operator()
    # end __init__

    @property
    def serving(self) -> bool:
        """
        Checks if the service is currently serving.

        :return: The boolean value.
        """

        return self._server_operator.operating
    # end serving

    @property
    def built(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return self.server.bound
    # end built

    def connect(self, host: str = None, port: str = None) -> None:
        """
        Connects the server.

        :param host: The host.
        :param port: The port.
        """

        self.server.bind((host or self.host, port or self.port))
    # end connect

    def respond(self, address: Address, connection: Connection) -> None:
        """
        Sets or updates clients data in the clients' container .

        :param address: The ip address and port used for the sockets' connection.
        :param connection: The sockets object used for the connection.
        """

        url = self.server.receive(connection=connection)[0].decode()

        payload = urlparse(url)

        kwargs = {
            segment[:segment.find("=")]: segment[segment.find("=") + 1:]
            for segment in payload.query.split("&")
        }

        self.server.send(
            data=encode(self.endpoints[payload.path[1:]](**kwargs)).encode(),
            connection=connection, address=address
        )

        connection.close()
    # end respond

    def run(
            self,
            protocol: BaseProtocol = None,
            action: Action = None,
            sequential: bool = True,
            update: bool = False,
            block: bool = False,
            refresh: float | dt.timedelta = None,
            wait: Time = None,
            timeout: Time = None,
    ) -> None:
        """
        Runs the process of the service.

        :param action: The action to call.
        :param protocol: The protocol to use for sockets communication.
        :param sequential: The value to handle clients sequentially.
        :param update: The value to update the service.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        super().run(
            update=update, block=False, refresh=refresh,
            wait=wait, timeout=timeout
        )

        self._server_operator.operation = (
            lambda: self.server.handle(
                action=action, protocol=protocol,
                sequential=sequential
            )
        )

        self._server_operator.run(
            wait=wait, timeout=timeout, block=block
        )
    # end run

    def stop(self) -> None:
        """Stops the service."""

        super().stop()

        self.server.handling = False

        self._server_operator.stop_operation()
    # end stop
# end SocketService