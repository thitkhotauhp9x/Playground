import functools
import pickle
import shelve
from typing import Callable


def encode[T](data: T) -> bytes:
    return pickle.dumps(data)


def decode[T](data: bytes) -> T:
    return pickle.loads(data)


def cache[**P, R](
    db_name: str,
    key_factory: Callable[[Callable[P, R], P], str],
    encoder: Callable[[R], bytes] = encode,
    decoder: Callable[[bytes], R] = decode,
):
    with shelve.open(db_name) as db:

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key: str = key_factory(func, *args, **kwargs)

                if key not in db:
                    db[key] = encoder(func(*args, **kwargs))

                return decoder(db[key])

            return wrapper

        return decorator
