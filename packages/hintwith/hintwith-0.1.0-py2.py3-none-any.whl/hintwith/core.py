"""
Contains the core of hintwith: hintwith(), hintwithmethod(), etc.

NOTE: this module is private. All functions and objects are available in the main
`hintwith` namespace - use that instead.

"""
from typing import Callable, TypeVar

from typing_extensions import Concatenate, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
U = TypeVar("U")
S = TypeVar("S")

__all__ = ["hintwith", "hintwithmethod"]


def hintwith(__func: Callable[P, T]) -> Callable[[Callable[..., U]], Callable[P, U]]:
    """
    This decorator does literally NOTHING to your function, but can annotate it
    with an existing one's annotations. This means that nothing inside the
    function (including attributes like `__doc__` and `__annotations__`) are
    modified, but the annotations may SEEM to be changed in your IDE's type hints.

    Parameters
    ----------
    __func : Callable[P, T]
        The function whose annotations you want to annotate with.

    Returns
    -------
    Callable[[Callable[..., U]], Callable[P, U]]
        A decorator which does nothing to the function.

    """

    def decorator(a: Callable[..., U]) -> Callable[P, U]:
        return a  # See? We do nothing to your function

    return decorator


def hintwithmethod(
    __method: Callable[Concatenate[S, P], T]
) -> Callable[[Callable[..., U]], Callable[P, U]]:
    """
    Behaves like `hintwith()` except that it is designed to annotate your function
    with a method rather than another function.

    Parameters
    ----------
    __method : Callable[Concatenate[S, P], T]
        The method whose annotations you want to copy.

    Returns
    -------
    Callable[[Callable[..., U]], Callable[P, U]]
        A decorator which does nothing to the function.

    """

    def decorator(a: Callable[..., U]) -> Callable[P, U]:
        return a  # See? We do nothing to your function

    return decorator
