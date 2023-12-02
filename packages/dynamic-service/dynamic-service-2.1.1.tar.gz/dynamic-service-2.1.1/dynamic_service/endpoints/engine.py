# engine.py

from functools import wraps
from typing import (
    Any, Callable, Iterable, TypeVar, Generic
)

from attrs import define, field

from fastapi.openapi.docs import get_swagger_ui_html, HTMLResponse

from represent import Modifiers, represent

from dynamic_service.endpoints.data import DOCS

__all__ = [
    "BaseEndpoint",
    "DocsEndpoint",
    "Record",
    "valid_endpoints",
    "build_endpoints",
    "adjust_path"
]

@define(repr=False)
@represent
class Record:
    """A class to represent a result object for commands and conditions calls."""

    args: tuple = field(factory=tuple),
    kwargs: dict[str, Any] = field(factory=dict),
    returns: Any = None

    def collect(
            self, *,
            args: tuple = None,
            kwargs: dict[str, Any] = None,
            returns: Any = None
    ) -> None:
        """
        Defines the class attributes.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :param returns: The returned values.
        """

        self.args = args
        self.kwargs.update(kwargs)
        self.returns = returns
    # end collect
# end Record

_ST = TypeVar("_ST")
_RT = TypeVar("_RT")
_PRT = TypeVar("_PRT")

def adjust_path(path: str) -> str:
    """
    adjusts the path of the endpoints.

    :param path: The path to adjust.

    :return: The adjusted path.
    """

    if (not path) or (path == "/"):
        return path
    # end if

    return (
        ("/" if not path.startswith("/") else '') + path
    ).replace("//", "/")
# end adjust_path

@represent
class BaseEndpoint(Generic[_ST, _RT, _PRT]):
    """
    A class to represent an endpoint.

    The BaseEndpoint is a command class that is the base of custom
    endpoint classes. Custom endpoint classes inherit from BaseEndpoint
    to add the command to execute when the endpoint is requested
    by a client, through the API of a service object.

    The endpoint method is implemented in child classes.

    All the returned values and parameters end endpoint collects through
    its lifetime are stored as AssistantResponse and Request objects at the internal
    record of the object.

    data attributes:

    - io:
        The configuration for saving and loading data and attributes
        that are none-mandatory to load and save. When given to False,
        The io object will have no keys inside it.

    - methods:
        A list of API endpoint methods that the endpoint should be
        able to operate with.

    - path:
        The path to the endpoint through the api.

    - root:
        The root of the path to the endpoint, when not ''.

    >>> from dynamic_service.endpoints import BaseEndpoint, GET
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/<ENDPOINT PATH IN URL>", methods=[GET])
    # end AnswerEndpoint
    """

    __modifiers__ = Modifiers(
        excluded=["options"], hidden=["record", "service"]
    )

    PATH: str
    METHODS: list[str]
    RECORD: bool = False

    __slots__ = (
        "path", "methods", "service", "description",
        "root", "options", "record", "recording"
    )

    def __init__(
            self,
            path: str = None,
            root: str = None,
            methods: Iterable[str] = None,
            service: _ST = None,
            record: bool = None,
            description: str = None,
            options: dict[str, Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param path: The path to the endpoint.
        :param root: The root to the endpoint.
        :param methods: The endpoint methods.
        :param record: The value to record the endpoint.
        :param description: The description of the object.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        if record is None:
            record = self.RECORD
        # end if

        self.recording = record

        self.record: list[Record] = []

        self.options = options or {}

        self.root = adjust_path(root or "")
        self.path = adjust_path(str(path or self.PATH))
        self.description = description

        self.methods = list(methods or self.METHODS)

        self.service = service
    # end __init__

    def __call__(self, *args: Any, **kwargs: Any) -> _PRT:
        """
        Returns the function to command the command.

        :param name: The intent that activated the command.
        :param message: The message for the intent.

        :return: The function to command the command.
        """

        record = None

        if self.recording:
            record = Record(args=args, kwargs=kwargs)
        # end if

        returns = self.wrap(self.endpoint)(*args, **kwargs)

        if record:
            record.returns = returns

            self.record.append(record)
        # end if

        return self.process(returns)
    # end __call__

    @staticmethod
    def call(instance) -> Callable[..., _RT]:
        """
        Returns the function to command the command.

        :param instance: An instance of the class.

        :return: The function to command the command.
        """

        return instance.__call__
    # end call

    def process(self, response: _RT) -> _PRT:
        """
        Processes the response of the endpoint.

        :param response: The endpoint response to process.

        :return: The processed response.
        """

        dir(self)

        return response
    # end process

    def wrap(self, endpoint: Callable[..., Any]) -> Callable[..., _RT]:
        """
        Processes the response of the endpoint.

        :param endpoint: The endpoint to process.

        :return: The processed response.
        """

        dir(self)

        @wraps(endpoint)
        def wrapper(*args: Any, **kwargs: Any) -> _RT:
            """
            Returns the response for the API endpoint.

            :param args: The positional arguments.
            :param kwargs: Any keyword argument.

            :return: The response from the function call.
            """

            return endpoint(*args[1:], **kwargs)
        # end wrapper

        return wrapper
    # end process

    def endpoint(self, *args: Any, **kwargs: Any) -> _RT:
        """
        Returns the response for the API endpoint.

        :param args: The positional arguments.
        :param kwargs: Any keyword argument.

        :return: The response from the function call.
        """
    # end endpoint
# end BaseEndpoint

class DocsEndpoint(BaseEndpoint):
    """A class to represent an endpoint."""

    __slots__ = "icon", "title"

    def __init__(
            self,
            methods: Iterable[str] = None,
            service: object = None,
            title: str = None,
            description: str = None,
            icon: str = None,
            options: dict[str, Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param methods: The endpoint methods.
        :param description: The description of the object.
        :param icon: The icon file path.
        :param title: The endpoint title.
        :param options: Any keyword arguments.
        :param service: The service object.
        """

        self.title = title
        self.icon = icon

        BaseEndpoint.__init__(
            self, path=DOCS, methods=methods, service=service,
            description=description, options=options
        )
    # end __init__

    def endpoint(self) -> HTMLResponse:
        """
        Returns the response for the API endpoint.

        :return: The response from the function call.
        """

        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=(
                self.title + " - Service Docs"
                if self.title is not None else "Service Docs"
            ),
            swagger_favicon_url=(
                self.icon if self.icon is not None else
                "https://fastapi.tiangolo.com/img/favicon.png"
            )
        )
    # end answer
# end DocsEndpoint

def valid_endpoints(endpoints: Any = None) -> dict[str, BaseEndpoint]:
    """
    Process the endpoints' commands to validate and modify it.

    :param endpoints: The endpoints object to check.

    :return: The valid endpoints object.
    """

    if endpoints is None:
        endpoints = {}

    elif isinstance(endpoints, dict):
        endpoints = {**endpoints}

    else:
        try:
            endpoints = {
                endpoint.path: endpoint for endpoint in endpoints
            }

        except ValueError:
            raise ValueError(
                f"Endpoints parameter must be either a dictionary "
                f"with paths as keys and endpoint objects with matching "
                f"paths as values, or an iterable object with endpoint objects, "
                f"not: {endpoints}"
            )
        # end try
    # end if

    return endpoints
# end valid_endpoints

def build_endpoints(
    endpoints: Iterable[BaseEndpoint | type[BaseEndpoint]],
    service: _ST = None
) -> list[BaseEndpoint[_ST, ..., ...]]:
    """
    Builds the endpoints for the service.

    :param service: The service for the endpoints.
    :param endpoints: The bases of endpoints for the service.

    :return: The built endpoints.
    """

    return [
        (
            endpoint(
                path=endpoint.PATH,
                methods=endpoint.METHODS,
                service=service,
                options=dict(response_model=None)
            ) if issubclass(endpoint, BaseEndpoint) else endpoint
        ) for endpoint in endpoints
    ]
# end build_endpoints