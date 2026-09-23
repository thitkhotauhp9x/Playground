from typing import Iterator


def retry(max_retries: int) -> Iterator[int]:
    for counter in range(0, max_retries):
        yield counter
