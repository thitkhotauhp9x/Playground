from collections.abc import Iterator


def retry(max_retries: int) -> Iterator[int]:
    yield from range(0, max_retries)
