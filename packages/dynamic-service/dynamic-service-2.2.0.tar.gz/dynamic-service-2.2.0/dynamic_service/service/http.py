# http.py

import os
import logging
import warnings
import pickle
from functools import partial
import datetime as dt
from typing import Any, Iterable, TypeVar, Self

import requests

from attr import define

from represent import Modifiers, represent

from looperator import Operator, ServiceInterface

from uvicorn import Server, Config as ServiceConfig
from fastapi import FastAPI, APIRouter
import fastapi

from dynamic_service.endpoints import (
    FileResponse, BaseEndpoint, POST, DELETE, PUT,
    GET, RedirectResponse, adjust_path,
    DocsEndpoint, FAVICON, DOCS, valid_endpoints
)
from dynamic_service.service.base import EndpointsService
from dynamic_service.endpoints.base import override_signature

__all__ = [
    "HTTPService",
    "HTTPClient",
    "HTTPRecordClient",
    "automate"
]

TimeDuration = float | dt.timedelta
TimeDestination = TimeDuration | dt.datetime
Endpoints = dict[str, BaseEndpoint]
EndpointsContainer = Iterable[BaseEndpoint] | Endpoints

class Endpoint(partial):
    """A class to wrap around an endpoint object."""

    __slots__ = ()
# end Endpoint

class HTTPService(ServiceInterface, EndpointsService):
    """
    A class to represent a service object.

    The BaseService is the parent class of service class.
    The service class creates a service object to deploy
    functionality of endpoint objects as a REST API.

    data attributes:

    - name:
        The name of the service.

    - endpoints:
        A set of endpoint objects to serve with the api.

    - root:
        A common root path to add to all endpoints.

    - icon:
        A path to an icon file to display in a web interface (*.ico).

    - home:
        The path to the home page of the web interface.

    - debug:
        The value to set the home page as the test page.

    >>> from dynamic_service.endpoints import BaseEndpoint, GET
    >>> from dynamic_service.service.http import HTTPService
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/my_endpoint", methods=[GET])
    >>>
    >>> service = HTTPService(
    >>>     name="service", path="<PATH TO THE SERVICE>",
    >>>     endpoints=[endpoint]
    >>> )
    >>>
    >>> service.run()
    """

    SILENT = False

    ICON = None
    VERSION = "0.0.0"
    DESCRIPTION = ""
    SUMMARY = ""
    NAME = "Dynamic-Service"

    __modifiers__ = Modifiers(excluded=["app", "server"])

    __slots__ = (
        "name", "version", "endpoints", "description", "icon",
        "home", "debug", "app", "service", "_root", "server",
        "_serving_process", "_running_parameters"
    )

    def __init__(
            self,
            endpoints: EndpointsContainer = None, *,
            name: str = None,
            version: str = None,
            root: str = None,
            summary: str = None,
            description: str = None,
            icon: str = None,
            home: str | bool = None,
            debug: bool = None
    ) -> None:
        """
        Defines the class attributes.

        :param name: The name of the service.
        :param version: The version of the service.
        :param endpoints: The service endpoints.
        :param description: The description of the object.
        :param summary: The summary of the object.
        :param icon: The icon path.
        :param root: The root to the path.
        :param home: The home endpoint.
        :param debug: The value to create the docs' endpoint for the home endpoint.
        """

        ServiceInterface.__init__(self)
        EndpointsService.__init__(self, endpoints=endpoints)

        if (home is True) or (debug and (home is None)):
            home = True
        # end if

        self.description = description or self.DESCRIPTION
        self.summary = summary or self.SUMMARY
        self.root = adjust_path(root or "")
        self.icon = icon or self.ICON
        self.home = home
        self.name = name or self.NAME
        self.version = version or self.VERSION

        self.endpoints: dict[str, BaseEndpoint[type[Self]]]

        self._running_parameters: dict[str, Any] | None = None

        self.app: FastAPI | None = None
        self.server: Server | None = None

        self._serving_process = Operator(
            termination=self.stop_serving, loop=False
        )
    # end __init__

    def __getstate__(self) -> dict[str, Any]:
        """
        Gets the state of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        data["app"] = None
        data["server"] = None

        return data
    # end __getstate__

    @staticmethod
    def valid_endpoints(endpoints: Any = None) -> Endpoints:
        """
        Process the endpoints' commands to validate and modify it.

        :param endpoints: The endpoints object to check.

        :return: The valid endpoints object.
        """

        return valid_endpoints(endpoints=endpoints)
    # end valid_endpoints

    @property
    def host(self) -> str | None:
        """
        Returns the host of the service.

        :return: The host.
        """

        if isinstance(self.server, Server):
            return self.server.config.host
        # end if
    # end host

    @property
    def port(self) -> int | None:
        """
        Returns the port of the service.

        :return: The port.
        """

        if isinstance(self.server, Server):
            return self.server.config.port
        # end if
    # end port

    @property
    def serving(self) -> bool:
        """
        Checks if the service is currently serving.

        :return: The boolean value.
        """

        return self._serving_process.operating
    # end serving

    @property
    def built(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return isinstance(self.app, FastAPI)
    # end built

    @property
    def created(self) -> bool:
        """
        Checks if the service was created.

        :return: The value for the service being created.
        """

        return self._serving_process.operation is not None
    # end created

    def build(self) -> None:
        """
        Builds the service endpoints.

        :returns: The app object.
        """

        self.app = FastAPI(
            title=self.name, description=self.description,
            version=self.version, docs_url=None
        )

        router = APIRouter(prefix=self.root)

        for endpoint in self.endpoints.values():
            path = adjust_path(endpoint.root + endpoint.path)

            command = override_signature(
                Endpoint(endpoint.__call__, endpoint),
                new=endpoint.endpoint, name=type(endpoint).__name__
            )

            try:
                router.add_api_route(
                    path, command, methods=endpoint.methods,
                    description=endpoint.description, **endpoint.options
                )

            except fastapi.exceptions.FastAPIError:
                endpoint.options.setdefault('response_model', None)

                router.add_api_route(
                    path, command, methods=endpoint.methods,
                    description=endpoint.description, **endpoint.options
                )
            # end try
        # end for

        if (self.icon is not None) and os.path.exists(self.icon):
            router.add_api_route(
                adjust_path(self.root + FAVICON),
                lambda: FileResponse(self.icon),
                methods=[GET], include_in_schema=False
            )
        # end if

        if isinstance(self.home, bool) and self.home:
            router.add_api_route(
                adjust_path(self.root + '/'),
                lambda: RedirectResponse(DOCS),
                methods=[GET], include_in_schema=False
            )
        # end if

        if DOCS not in self.endpoints:
            docs_path = adjust_path(self.root + DOCS)
            router.add_api_route(
                docs_path, DocsEndpoint(
                    icon=docs_path, methods=[GET], title=self.name
                ).endpoint, methods=[GET], include_in_schema=False
            )
        # end if

        self.app.include_router(router)
    # end build

    def create(
            self,
            host: str = None,
            port: int = None,
            silent: bool = None
    ) -> None:
        """
        Creates the process to run the api service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        """

        if silent is None:
            silent = self.SILENT
        # end if

        if not self.built:
            self.build()
        # end if

        self.server = Server(
            config=ServiceConfig(app=self.app, host=host, port=port)
        )

        self._serving_process.operation = lambda: (
            (logging.disable(logging.INFO) if silent else ()),
            self.server.run()
        )
    # end create

    def start_serving(
            self,
            host: str = None,
            port: int = None,
            silent: bool = None
    ) -> None:
        """
        Starts serving the service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        """

        if not self.created:
            self.create(host=host, port=port, silent=silent)
        # end if

        self._serving_process.start_operation()
    # end start_serving

    def run(
            self, /, *,
            serve: bool = True,
            host: str = None,
            port: int = None,
            silent: bool = None,
            block: bool = False,
            update: bool = True,
            refresh: TimeDuration = True,
            wait: TimeDestination = None,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the api service.

        :param serve: The value to start serving.
        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the system.
        :param update: The value to update the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        self._running_parameters = dict(
            host=host, port=port, serve=serve,
            silent=silent, wait=wait,
            update=update, refresh=refresh,
            timeout=timeout, block=block
        )

        if serve:
            self.start_serving(host=host, port=port, silent=silent)
        # end if

        super().run(
            update=update, refresh=refresh,
            block=block, wait=wait, timeout=timeout
        )
    # end run

    def rerun(
            self, /, *,
            serve: bool = True,
            host: str = None,
            port: int = None,
            silent: bool = None,
            block: bool = False,
            update: bool = True,
            refresh: TimeDuration = True,
            wait: TimeDestination = None,
            timeout: TimeDestination = None
    ) -> None:
        """
        Runs the api service.

        :param serve: The value to start serving.
        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the system.
        :param update: The value to update the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        self.stop()

        parameters = dict(
            host=host, port=port, serve=serve,
            silent=silent, wait=wait,
            update=update, refresh=refresh,
            timeout=timeout, block=block
        )

        parameters = {
            key: value for key, value in parameters.items()
            if value is not None
        }

        self._running_parameters.update(parameters)

        self.run(**self._running_parameters)
    # end rerun

    def stop_serving(self) -> None:
        """Stops the service process."""

        if self.created and self._serving_process.operating:
            self._serving_process.stop_operation()

            self.server.should_exit = True
            self.server = None

            self._serving_process.operation = None
        # end if
    # end stop_serving

    def stop(self) -> None:
        """Pauses the process of service."""

        super().stop()

        self.stop_serving()
    # end terminate
# end BaseService

_PRT = TypeVar("_PRT")

ClientEndpoint = BaseEndpoint, type[BaseEndpoint]

@define(repr=False)
@represent
class HTTPClient:
    """A class to represent a screener client."""

    url: str

    @staticmethod
    def process(response: requests.Response) -> Any:
        """
        Processes the response object.

        :param response: The response object.

        :return: The returned values.
        """

        return response.json()
    # end process

    def get_request(
            self, endpoint: str, parameters: dict[str, Any] = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param parameters: The parameters.

        :return: The returned values.
        """

        return self.process(
            requests.get(f"{self.url}{endpoint}", params=parameters)
        )
    # end get_request

    def delete_request(
            self, endpoint: str, parameters: dict[str, Any] = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param parameters: The parameters.

        :return: The returned values.
        """

        return self.process(
            requests.delete(f"{self.url}{endpoint}", params=parameters)
        )
    # end delete_request

    def post_request(
            self,
            endpoint: str,
            parameters: dict[str, Any] = None,
            data: Any = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param parameters: The parameters.
        :param data: The body of the request.

        :return: The returned values.
        """

        return self.process(
            requests.post(
                f"{self.url}{endpoint}",
                params=parameters, json=data
            )
        )
    # end post_request

    def put_request(
            self,
            endpoint: str,
            parameters: dict[str, Any] = None,
            data: Any = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param parameters: The parameters.
        :param data: The body of the request.

        :return: The returned values.
        """

        return self.process(
            requests.put(
                f"{self.url}{endpoint}",
                params=parameters, json=data
            )
        )
    # end put_request

    def request(
            self,
            endpoint: ClientEndpoint,
            path: str = None,
            parameters: dict[str, Any] = None,
            data: Any = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param parameters: The parameters.
        :param path: The path to the endpoint
        :param data: The body of the request.

        :return: The returned values.
        """

        method = GET

        request = self.get_request

        path = path or ""

        if issubclass(endpoint, BaseEndpoint):
            method = endpoint.METHODS[0]
            path = endpoint.PATH + path

        elif isinstance(endpoint, BaseEndpoint):
            method = endpoint.methods[0]
            path = endpoint.path + path
        # end if

        if method == GET:
            request = self.get_request

        elif method == POST:
            request = partial(self.post_request, data=data)

        elif method == DELETE:
            request = self.delete_request

        elif method == PUT:
            request = partial(self.put_request, data=data)
        # end if

        response: _PRT = request(endpoint=path, parameters=parameters)

        return response
    # end get_request
# end HTTPClient

Record = list[dict[str, Any]]

class HTTPRecordClient(HTTPClient):
    """A class to represent a control client."""

    __slots__ = ('record', '_responses')

    PAYLOAD = 'payload'
    RESPONSE = 'response'
    PATH = 'path'
    DATA = 'data'
    PARAMETERS = 'parameters'
    STATUS = 'status'
    METHOD = 'method'

    def __init__(self, url: str) -> None:
        """
        Defines the class attributes.

        :param url: The url for the requests.
        """

        super().__init__(url=url)

        self.record: Record = []
        self._responses: list[int] = []
    # end __init__

    def process(self, response: requests.Response) -> Any:
        """
        Processes the response object.

        :param response: The response object.

        :return: The returned values.
        """

        self._responses.append(response.status_code)

        return response.json()
    # end process

    def request(
            self,
            endpoint: ClientEndpoint = None, *,
            method: str = None,
            path: str = None,
            parameters: dict[str, Any] = None,
            data: Any = None
    ) -> Any:
        """
        Returns the response for the request.

        :param endpoint: The path to the endpoint.
        :param method: The request method.
        :param parameters: The parameters.
        :param path: The path to the endpoint
        :param data: The body of the request.

        :return: The returned values.
        """

        path = path or ""
        method = method or GET

        if issubclass(endpoint, BaseEndpoint):
            method = endpoint.METHODS[0]
            path = endpoint.PATH + path

        elif isinstance(endpoint, BaseEndpoint):
            method = endpoint.methods[0]
            path = endpoint.path + path
        # end if

        if method == GET:
            request = self.get_request

        elif method == POST:
            request = partial(self.post_request, data=data)

        elif method == DELETE:
            request = self.delete_request

        elif method == PUT:
            request = partial(self.put_request, data=data)

        else:
            raise ValueError(f"Unsupported method: {method}.")
        # end if

        response = request(endpoint=path, parameters=parameters)

        self.record.append(
            {
                self.PATH: path,
                self.METHOD: method,
                self.RESPONSE: response,
                self.STATUS: self._responses[-1],
                self.PAYLOAD: dict(
                    path=path, parameters=parameters,
                    data=data, method=method
                )
            }
        )

        return response
    # end request
# end HTTPRecordClient

def automate(
        client: HTTPRecordClient,
        record: Record, *,
        commit_successful: bool = None,
        save_successful: bool = None,
        continue_successful: bool = None,
        adjust: bool = None
) -> Record:
    """
    Automates the tasks in the record.

    :param client: The client to send the requests.
    :param record: The record of tasks to commit.
    :param commit_successful: The value to commit only successful requests.
    :param save_successful: The value to save only successful requests.
    :param continue_successful: The value to continue only after successful requests.
    :param adjust: The value to crush for request errors.

    :return: The new record from the tasks.
    """

    new_record: Record = []

    record = pickle.loads(pickle.dumps(record))

    for request in record:
        if commit_successful and (request[HTTPRecordClient.STATUS] != 200):
            continue
        # end if

        client.request(**request[HTTPRecordClient.PAYLOAD])

        commit = client.record[-1]

        if commit[HTTPRecordClient.STATUS] != 200:
            if not save_successful:
                new_record.append(commit)
            # end if

            if not continue_successful:
                error_data = ', '.join(
                    [f'{key} - {value}' for key, value in commit.items()]
                )

                error_message = (
                    f"Request Error: status code - "
                    f"{commit[HTTPRecordClient.STATUS]}, "
                    f"{error_data}"
                )

                if adjust:
                    warnings.warn(error_message)
                    warnings.warn(
                        "Request automation process is terminated "
                        "due to the request error below."
                    )

                    break

                else:
                    raise ValueError(error_message)
                # end if
            # end if
        # end if

        new_record.append(commit)
    # end for

    return new_record
# end automate