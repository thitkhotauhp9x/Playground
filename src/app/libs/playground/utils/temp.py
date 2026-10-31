from tempfile import NamedTemporaryFile
from pathlib import Path
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def temp_file(suffix: str | None = None) -> Generator[Path, None, None]:
    with NamedTemporaryFile(suffix=suffix) as tf:
        yield Path(tf.name)
