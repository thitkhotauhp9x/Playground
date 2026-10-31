import functools
from collections.abc import Callable


def dort[R1, R2](
    fn: Callable[[R1], R2],
) -> Callable[[Callable[..., R1]], Callable[..., R2]]:
    def decorator[**P](func: Callable[P, R1]) -> Callable[P, R2]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R2:
            return fn(func(*args, **kwargs))

        return wrapper

    return decorator
