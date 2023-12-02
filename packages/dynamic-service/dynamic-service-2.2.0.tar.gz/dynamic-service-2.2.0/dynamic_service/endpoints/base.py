# base.py

import copy
import types
import functools
from typing import Callable, TypeVar

__all__ = [
    "override_signature"
]

_RT = TypeVar("_RT")

def override_signature(
        command: Callable | types.FunctionType, /, *,
        new: Callable[..., _RT] | types.FunctionType,
        name: str = None
) -> Callable[..., _RT] | types.FunctionType:
    """
    Overrides the signature of a function.

    :param command: The function to override.
    :param new: The function wit the new signature.
    :param name: The new name for the function.

    :return: The old function with the new signature.
    """

    attributes = (
        '__module__', '__name__', '__qualname__',
        '__doc__', '__annotations__'
    )

    for attr in attributes:
        setattr(command, attr, getattr(new, attr))
    # end for

    command.__annotations__['return'] = (
        dict[str, int | new.__annotations__['return']]
    )

    command = functools.update_wrapper(command, new, assigned=attributes)

    command.__kwdefaults__ = copy.copy(new.__kwdefaults__)

    if isinstance(name, str):
        command.__name__ = name
    # end if

    return command
# end override_signature