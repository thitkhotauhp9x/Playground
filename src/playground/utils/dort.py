import functools
from typing import Callable


def dort[**P, R, R1](
    fn: Callable[[R], R1],
) -> Callable[[Callable[P, R]], Callable[P, R1]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R1]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R1:
            return fn(func(*args, **kwargs))

        return wrapper

    return decorator
